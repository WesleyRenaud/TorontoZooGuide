import { loadArray, saveArray } from '../panel/localStorage.js';
import { ANIMALS_KEY } from '../../pages/itineraryWizard/keys.js';

import {
   getExhibitsByRegion,
   getAnimalsByExhibit,
} from './regionSelector/regionApi.js';

import {
   normalizeRegion,
   getExhibit,
   makeSelectedAnimal,
   buildSelectedAnimalKey,
   mergeAnimals,
   isRegionFullySelected,
   syncRegionSelection,
} from './regionSelector/regionSelection.js';

import { buildRegionRows } from './regionSelector/regionRenderer.js';

import {
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
   loadSelectedNames,
   saveSelectedNames,
} from './regionSelector/regionStorage.js';

export function createItineraryRegionSelectorController({
   mountEl,
   onPrev,
   onNext,
   onFinish,
   onClose,
} = {}) {
   let root = null;
   let regions = [];

   const selectedRegionNames = new Set();
   const selectedExhibitNames = new Set();

   function persistSelectionState() {
      saveSelectedNames(SELECTED_EXHIBITS_KEY, selectedExhibitNames);
      saveSelectedNames(SELECTED_REGIONS_KEY, selectedRegionNames);
   }

   function commitSelectionChanges() {
      persistSelectionState();
      renderRegions();
   }

   function syncAllRegionSelections() {
      selectedRegionNames.clear();

      regions.forEach((region) => {
         if (isRegionFullySelected(region, selectedExhibitNames)) {
            selectedRegionNames.add(region.name);
         }
      });
   }

   function hydrateSelectionsFromStorage() {
      selectedExhibitNames.clear();
      selectedRegionNames.clear();

      const storedExhibits = new Set(loadSelectedNames(SELECTED_EXHIBITS_KEY));

      regions.forEach((region) => {
         const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

         exhibits.forEach((exhibit) => {
            if (storedExhibits.has(exhibit)) {
               selectedExhibitNames.add(exhibit);
            }
         });
      });

      syncAllRegionSelections();
      persistSelectionState();
   }

   function toggleRegion(region) {
      const regionName = region?.name;
      const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

      if (!regionName || !exhibits.length) return;

      const shouldSelect = !isRegionFullySelected(region, selectedExhibitNames);

      exhibits.forEach((exhibit) => {
         if (shouldSelect) {
            selectedExhibitNames.add(exhibit);
         } else {
            selectedExhibitNames.delete(exhibit);
         }
      });

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      commitSelectionChanges();
   }

   function toggleExhibit(region, exhibitName) {
      if (!exhibitName) return;

      if (selectedExhibitNames.has(exhibitName)) {
         selectedExhibitNames.delete(exhibitName);
      } else {
         selectedExhibitNames.add(exhibitName);
      }

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      commitSelectionChanges();
   }

   function getSelectedExhibitsForFetch() {
      return Array.from(selectedExhibitNames);
   }

   async function buildUpdatedAnimalsFromSelection() {
      const selectedExhibits = getSelectedExhibitsForFetch();
      const currentAnimals = loadArray(ANIMALS_KEY);

      if (!selectedExhibits.length) {
         saveArray(ANIMALS_KEY, []);
         return [];
      }

      const fullAnimals = await getAnimalsByExhibit(selectedExhibits);
      const selectedAnimals = fullAnimals.map(makeSelectedAnimal);

      const selectedAnimalKeys = new Set(
         selectedAnimals.map(buildSelectedAnimalKey).filter(Boolean)
      );

      const selectedExhibitSet = new Set(
         selectedExhibits.map((exhibit) => String(exhibit).trim().toLowerCase())
      );

      const preservedAnimals = currentAnimals.filter((animal) => {
         const exhibit = getExhibit(animal).trim().toLowerCase();

         if (!exhibit) return true;

         if (selectedExhibitSet.has(exhibit)) {
            return selectedAnimalKeys.has(buildSelectedAnimalKey(animal));
         }

         return false;
      });

      const mergedAnimals = mergeAnimals(preservedAnimals, selectedAnimals);
      saveArray(ANIMALS_KEY, mergedAnimals);

      return mergedAnimals;
   }

   function bindRegionEvents(container) {
      container.querySelectorAll('[data-action="toggle-region"]').forEach((btn) => {
         btn.addEventListener('click', () => {
            const regionName = btn.dataset.region;
            const region = regions.find((r) => r.name === regionName);

            if (region) {
               toggleRegion(region);
            }
         });
      });

      container.querySelectorAll('[data-action="toggle-exhibit"]').forEach((btn) => {
         btn.addEventListener('click', () => {
            const regionName = btn.dataset.region;
            const exhibitName = btn.dataset.exhibit;
            const region = regions.find((r) => r.name === regionName);

            if (region && exhibitName) {
               toggleExhibit(region, exhibitName);
            }
         });
      });
   }

   function renderRegions() {
      if (!root) return;

      const container = root.querySelector('.itin-region-results');
      if (!container) return;

      if (!regions.length) {
         container.innerHTML = `
            <div class="itin-empty">No regions available right now.</div>
         `;
         return;
      }

      container.innerHTML = regions
         .map((region) => buildRegionRows(region, selectedExhibitNames))
         .join('');

      bindRegionEvents(container);
   }

   async function loadRegions() {
      const fetchedRegions = await getExhibitsByRegion();

      regions = fetchedRegions
         .map(normalizeRegion)
         .filter((region) => region.name);
   }

   function bindShellEvents() {
      root.querySelector('.itin-close')?.addEventListener('click', () => {
         onClose?.();
      });

      root.querySelector('.itin-prev')?.addEventListener('click', () => {
         onPrev?.();
      });

      root.querySelector('.itin-next')?.addEventListener('click', async () => {
         const animals = await buildUpdatedAnimalsFromSelection();
         onNext?.(animals);
      });

      root.querySelector('.itin-finish')?.addEventListener('click', async () => {
         const animals = await buildUpdatedAnimalsFromSelection();
         onFinish?.(animals);
      });
   }

   function build() {
      root = document.createElement('div');
      root.className = 'itin-overlay';
      root.innerHTML = `
         <section class="itin-card itin-card-tall" role="dialog" aria-modal="true" aria-label="Select regions and exhibits">
            <div class="itin-card-topbar itin-card-topbar-with-close">
               <div class="itin-top-title">Itinerary Builder</div>
               <button class="itin-close" type="button" aria-label="Close itinerary builder">×</button>
            </div>

            <div class="itin-card-body itin-card-body-tall">
               <h1 class="itin-h1">Add Animals by Region</h1>
               <div class="itin-region-results itin-results"></div>
            </div>

            <div class="itin-card-actions-dual">
               <button class="itin-prev" type="button">Back</button>

               <div class="itin-actions-right">
                  <button class="itin-next" type="button">Next</button>
                  <button class="itin-next itin-finish" type="button">Finish</button>
               </div>
            </div>
         </section>
      `;

      bindShellEvents();
   }

   async function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      await loadRegions();
      hydrateSelectionsFromStorage();
      renderRegions();

      mountEl.innerHTML = '';
      mountEl.appendChild(root);
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   function getSelectedRegions() {
      return Array.from(selectedRegionNames);
   }

   function getSelectedExhibits() {
      return Array.from(selectedExhibitNames);
   }

   return {
      show,
      hide,
      getSelectedRegions,
      getSelectedExhibits,
   };
}