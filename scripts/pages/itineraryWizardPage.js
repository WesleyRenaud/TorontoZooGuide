// scripts/pages/itineraryWizardPage.js
import { createItineraryDateSelectorController } from '../itinerary/dateSelector.js';
import { createItineraryAnimalSelectorController } from '../itinerary/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../itinerary/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../itinerary/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../itinerary/wildEncounterSelector.js';
import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import { initItineraryPage } from './itineraryPage.js';

import { createMapStore } from '../map/store.js';
import { createDataSources } from '../map/sources.js';

import {
   parseItineraryIncludes,
   dateISOToMonthDay
} from '../itinerary/itineraryHelpers.js';

const ITIN_KEY = 'tzg.itinerary';
const DATE_KEY = 'tzg.itineraryDateISO';
const ANIMALS_KEY = 'tzg.itineraryAnimals';
const ATTRACTIONS_KEY = 'tzg.itineraryAttractions';
const TALKS_KEY = 'tzg.itineraryGuardiansTalks';
const WILD_KEY = 'tzg.itineraryWildEncounters';

function loadArray(key) {
   try {
      const raw = localStorage.getItem(key);
      const arr = JSON.parse(raw || '[]');
      return Array.isArray(arr) ? arr : [];
   } catch {
      return [];
   }
}

function isScrollable(el) {
   if (!el) return false;
   const style = window.getComputedStyle(el);
   const overflowY = style.overflowY;

   if (overflowY !== 'auto' && overflowY !== 'scroll') return false;

   return el.scrollHeight > el.clientHeight;
}

function findScrollableAncestor(startEl, stopEl) {
   let el = startEl;
   while (el && el !== stopEl && el !== document.body) {
      if (isScrollable(el)) return el;
      el = el.parentElement;
   }
   return null;
}

function blockMapWheelWhileWizardOpen(mountEl) {
   if (!mountEl) return;

   mountEl.addEventListener(
      'wheel',
      (e) => {
         const overlay = mountEl.querySelector('.itin-overlay');
         if (!overlay) return;

         // Only care about wheel events occurring inside the overlay UI
         if (!overlay.contains(e.target)) return;

         const scroller = findScrollableAncestor(e.target, overlay);

         if (scroller) {
            // ✅ Allow normal scrolling, but stop the map from seeing the wheel event
            e.stopPropagation();
            return;
         }

         // ✅ Not over a scrollable area: block it so the map can't zoom
         e.preventDefault();
         e.stopPropagation();
      },
      { capture: true, passive: false }
   );
}

function safeParseJSON(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

function isItineraryEmpty(itin) {
   if (!itin || typeof itin !== 'object') return true;

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [];
   const wildEncounters = Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [];

   return !animals.length && !attractions.length && !guardiansTalks.length && !wildEncounters.length;
}

function showItineraryPopup({ mountEl, title = 'Heads up', message = '', buttonText = 'OK' }) {
   if (!mountEl) return;

   // remove any existing popup
   mountEl.querySelector('.tzg-popup')?.remove();

   const wrap = document.createElement('div');
   wrap.className = 'tzg-popup';

   wrap.innerHTML = `
      <div class="itin-overlay">
         <section class="itin-card tzg-popup-card" role="dialog" aria-modal="true">
            <div class="itin-card-topbar">
               <div class="itin-top-title">${title}</div>
            </div>

            <div class="itin-card-body tzg-popup-body">
               <div class="tzg-popup-message">${message}</div>
            </div>

            <div class="itin-card-actions">
               <div class="itin-actions-right">
                  <button type="button" class="itin-next tzg-popup-ok">${buttonText}</button>
               </div>
            </div>
         </section>
      </div>
   `;

   const close = () => wrap.remove();

   // click backdrop closes (but not the card)
   wrap.querySelector('.itin-overlay')?.addEventListener('click', (e) => {
      if (e.target === e.currentTarget) close();
   });

   wrap.querySelector('.tzg-popup-ok')?.addEventListener('click', close);

   // Esc closes
   const onKey = (e) => {
      if (e.key === 'Escape') {
         close();
         document.removeEventListener('keydown', onKey);
      }
   };
   document.addEventListener('keydown', onKey);

   mountEl.appendChild(wrap);

   // focus OK button
   setTimeout(() => wrap.querySelector('.tzg-popup-ok')?.focus?.(), 0);
}

function buildFinalItinerary({ dateISO, animals, attractions, guardiansTalks, wildEncounters }) {
   return { dateISO, animals, attractions, guardiansTalks, wildEncounters };
}

function saveFinalItinerary(itin) {
   localStorage.setItem(ITIN_KEY, JSON.stringify(itin));
   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated'));
}

function closeItineraryFlow(mountEl) {
   if (!mountEl) return;
   mountEl.innerHTML = '';
}

async function finalizeItinerary(
   { animals, attractions, guardiansTalks, wildEncounters } = {},
   mountEl
) {
   const dateISO = localStorage.getItem(DATE_KEY) || '';

   const finalItin = buildFinalItinerary({
      dateISO,
      animals: animals ?? loadArray(ANIMALS_KEY),
      attractions: attractions ?? loadArray(ATTRACTIONS_KEY),
      guardiansTalks: guardiansTalks ?? loadArray(TALKS_KEY),
      wildEncounters: wildEncounters ?? loadArray(WILD_KEY),
   });

   // ✅ Block finishing if empty
   if (isItineraryEmpty(finalItin)) {
      showItineraryPopup({
         mountEl,
         title: 'No Items Selected',
         message: 'Please add at least one Animal, Attraction, Meet the Guardians talk, or Wild Encounter before finishing.',
         buttonText: 'OK'
      });
      return;
   }

   const { month, day } = dateISOToMonthDay(dateISO);

   const inc = parseItineraryIncludes(finalItin);

   const payload = {
      month,
      day,
      temp: null,
      animals: inc.speciesToInclude,
      attractions: inc.attractionsToInclude,
      meetTheGuardiansTalks: inc.guardiansTalksToInclude,
      wildEncounters: inc.wildEncountersToInclude,
   };

   try {
      const store = createMapStore();
      const sources = createDataSources(store);

      if (!sources?.buildItinerary?.fetch) {
         console.warn('sources.buildItinerary is missing (add it in scripts/map/sources.js)');
      } else {
         await sources.buildItinerary.fetch(payload);
      }
   } catch (err) {
      console.error('Error calling sources.buildItinerary:', err);
   }

   saveFinalItinerary(finalItin);
   closeItineraryFlow(mountEl);
   renderItineraryPanel();
}

function openItineraryBuilder({ mountEl, startAt = 'date' } = {}) {
   if (!mountEl) return;

   const existing = safeParseJSON(localStorage.getItem(ITIN_KEY) || '', null) || {};
   let selectedAnimals = Array.isArray(existing.animals) ? existing.animals : [];
   let selectedAttractions = Array.isArray(existing.attractions) ? existing.attractions : [];
   let selectedGuardiansTalks = Array.isArray(existing.guardiansTalks) ? existing.guardiansTalks : [];
   let selectedWildEncounters = Array.isArray(existing.wildEncounters) ? existing.wildEncounters : [];

   const wildEncounterSelector = createItineraryWildEncounterSelectorController({
      mountEl,
      onPrev: () => guardiansTalkSelector.show(),
      onFinish: (wildEncounters) => {
         selectedWildEncounters = Array.isArray(wildEncounters) ? wildEncounters : [];
         finalizeItinerary({ animals: selectedAnimals, attractions: selectedAttractions, guardiansTalks: selectedGuardiansTalks, wildEncounters: selectedWildEncounters }, mountEl);
      },
   });

   const guardiansTalkSelector = createItineraryGuardiansTalkSelectorController({
      mountEl,
      onPrev: () => attractionSelector.show(),
      onNext: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         wildEncounterSelector.show();
      },
      onFinish: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         finalizeItinerary({ animals: selectedAnimals, attractions: selectedAttractions, guardiansTalks: selectedGuardiansTalks, wildEncounters: selectedWildEncounters }, mountEl);
      },
   });

   const attractionSelector = createItineraryAttractionSelectorController({
      mountEl,
      onPrev: () => animalSelector.show(),
      onNext: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         guardiansTalkSelector.show();
      },
      onFinish: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         finalizeItinerary({ animals: selectedAnimals, attractions: selectedAttractions, guardiansTalks: selectedGuardiansTalks, wildEncounters: selectedWildEncounters }, mountEl);
      },
   });

   const animalSelector = createItineraryAnimalSelectorController({
      mountEl,
      onPrev: () => dateSelector.show(),
      onNext: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         attractionSelector.show();
      },
      onFinish: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         finalizeItinerary({ animals: selectedAnimals, attractions: selectedAttractions, guardiansTalks: selectedGuardiansTalks, wildEncounters: selectedWildEncounters }, mountEl);
      },
   });

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onSave: () => animalSelector.show(),
      onFinish: () => {
         finalizeItinerary({ animals: selectedAnimals, attractions: selectedAttractions, guardiansTalks: selectedGuardiansTalks, wildEncounters: selectedWildEncounters }, mountEl);
      },
   });

   // ✅ Start on the requested step
   const showStart = () => {
      switch (startAt) {
         case 'animals': return animalSelector.show();
         case 'attractions': return attractionSelector.show();
         case 'guardiansTalks': return guardiansTalkSelector.show();
         case 'wildEncounters': return wildEncounterSelector.show();
         case 'date':
         default: return dateSelector.show();
      }
   };

   showStart();
}

export function initItineraryWizardPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

   window.addEventListener('tzg:editItinerarySection', (e) => {
      const step = e?.detail?.step || 'date';
      openItineraryBuilder({ mountEl, startAt: step });
   });

   blockMapWheelWhileWizardOpen(mountEl);

   if (document.getElementById('mapInner')) {
      try {
         initItineraryPage();
      } catch (err) {
         console.warn('initItineraryPage() failed:', err);
      }
   }

   renderItineraryPanel();

   const itin = safeParseJSON(localStorage.getItem(ITIN_KEY) || '', null);
   const shouldAutoOpen = !itin || isItineraryEmpty(itin);

   if (shouldAutoOpen) {
      openItineraryBuilder({ mountEl });
   }

   window.addEventListener('tzg:editItinerary', () => {
      openItineraryBuilder({ mountEl });
   });

   window.addEventListener('tzg:buildItinerary', () => {
      openItineraryBuilder({ mountEl });
   });

   window.addEventListener('tzg:itineraryUpdated', () => {
      renderItineraryPanel();
   });
}