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

function openItineraryBuilder({ mountEl } = {}) {
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
         finalizeItinerary(
            {
               animals: selectedAnimals,
               attractions: selectedAttractions,
               guardiansTalks: selectedGuardiansTalks,
               wildEncounters: selectedWildEncounters,
            },
            mountEl
         );
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
         finalizeItinerary(
            {
               animals: selectedAnimals,
               attractions: selectedAttractions,
               guardiansTalks: selectedGuardiansTalks,
               wildEncounters: selectedWildEncounters,
            },
            mountEl
         );
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
         finalizeItinerary(
            {
               animals: selectedAnimals,
               attractions: selectedAttractions,
               guardiansTalks: selectedGuardiansTalks,
               wildEncounters: selectedWildEncounters,
            },
            mountEl
         );
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
         finalizeItinerary(
            {
               animals: selectedAnimals,
               attractions: selectedAttractions,
               guardiansTalks: selectedGuardiansTalks,
               wildEncounters: selectedWildEncounters,
            },
            mountEl
         );
      },
   });

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onSave: () => {
         animalSelector.show();
      },
      onFinish: () => {
         finalizeItinerary(
            {
               animals: selectedAnimals,
               attractions: selectedAttractions,
               guardiansTalks: selectedGuardiansTalks,
               wildEncounters: selectedWildEncounters,
            },
            mountEl
         );
      },
   });

   dateSelector.show();
}

export function initItineraryWizardPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

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