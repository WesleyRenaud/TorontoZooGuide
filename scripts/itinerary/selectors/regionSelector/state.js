import { loadArray, saveArray } from '../../panel/localStorage.js';
import { ANIMALS_KEY } from '../../storageKeys.js';
import { getAnimalsByExhibit } from '../../../api/itinerarySelectorApi.js';

import {
   normalizeRegion,
   normalizeSelectedAnimal,
   makeSelectedAnimal,
   buildSelectedAnimalKey,
   mergeAnimals,
   isRegionFullySelected,
   syncRegionSelection,
} from './regionSelection.js';

import {
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
   loadSelectedNames,
   saveSelectedNames,
} from './regionStorage.js';

export function createRegionSelectorState() {
   let regions = [];

   const selectedRegionNames = new Set();
   const selectedExhibitNames = new Set();

   function persistSelectionState() {
      saveSelectedNames(SELECTED_EXHIBITS_KEY, selectedExhibitNames);
      saveSelectedNames(SELECTED_REGIONS_KEY, selectedRegionNames);
   }

   function syncAllRegionSelections() {
      selectedRegionNames.clear();

      regions.forEach((region) => {
         if (isRegionFullySelected(region, selectedExhibitNames)) {
            selectedRegionNames.add(region.name);
         }
      });
   }

   function findRegion(regionName) {
      return regions.find((region) => region.name === regionName) ?? null;
   }

   function setRegions(nextRegions) {
      regions = (Array.isArray(nextRegions) ? nextRegions : [])
         .map(normalizeRegion)
         .filter((region) => region.name);

      return regions.slice();
   }

   function hydrateSelectionsFromStorage() {
      selectedExhibitNames.clear();
      selectedRegionNames.clear();

      const storedExhibits = new Set(loadSelectedNames(SELECTED_EXHIBITS_KEY));

      regions.forEach((region) => {
         const exhibits = Array.isArray(region.exhibits) ? region.exhibits : [];

         exhibits.forEach((exhibitName) => {
            if (storedExhibits.has(exhibitName)) {
               selectedExhibitNames.add(exhibitName);
            }
         });
      });

      syncAllRegionSelections();
      persistSelectionState();
   }

   function toggleRegion(regionName) {
      const region = findRegion(regionName);
      const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

      if (!region?.name || !exhibits.length) {
         return false;
      }

      const shouldSelect = !isRegionFullySelected(region, selectedExhibitNames);

      exhibits.forEach((exhibitName) => {
         if (shouldSelect) {
            selectedExhibitNames.add(exhibitName);
         } else {
            selectedExhibitNames.delete(exhibitName);
         }
      });

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      persistSelectionState();

      return true;
   }

   function toggleExhibit(regionName, exhibitName) {
      const region = findRegion(regionName);

      if (!region || !exhibitName) {
         return false;
      }

      if (selectedExhibitNames.has(exhibitName)) {
         selectedExhibitNames.delete(exhibitName);
      } else {
         selectedExhibitNames.add(exhibitName);
      }

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      persistSelectionState();

      return true;
   }

   async function buildUpdatedAnimalsFromSelection() {
      const selectedExhibits = Array.from(selectedExhibitNames);
      const currentAnimals = loadArray(ANIMALS_KEY)
         .map(normalizeSelectedAnimal)
         .filter(Boolean);

      if (!selectedExhibits.length) {
         saveArray(ANIMALS_KEY, []);
         return [];
      }

      const fullAnimals = await getAnimalsByExhibit(selectedExhibits);
      const selectedAnimals = fullAnimals
         .map(makeSelectedAnimal)
         .filter(Boolean);

      const selectedAnimalKeys = new Set(
         selectedAnimals.map(buildSelectedAnimalKey).filter(Boolean)
      );

      const selectedExhibitSet = new Set(
         selectedExhibits.map((exhibitName) => String(exhibitName).trim().toLowerCase())
      );

      const preservedAnimals = currentAnimals.filter((animal) => {
         const exhibit = animal.exhibit.trim().toLowerCase();

         if (!exhibit) {
            return true;
         }

         if (selectedExhibitSet.has(exhibit)) {
            return selectedAnimalKeys.has(buildSelectedAnimalKey(animal));
         }

         return false;
      });

      const mergedAnimals = mergeAnimals(preservedAnimals, selectedAnimals);
      saveArray(ANIMALS_KEY, mergedAnimals);

      return mergedAnimals;
   }

   function getRegions() {
      return regions.slice();
   }

   function getSelectedRegions() {
      return Array.from(selectedRegionNames);
   }

   function getSelectedExhibits() {
      return Array.from(selectedExhibitNames);
   }

   return {
      setRegions,
      hydrateSelectionsFromStorage,
      toggleRegion,
      toggleExhibit,
      buildUpdatedAnimalsFromSelection,
      getRegions,
      getSelectedRegions,
      getSelectedExhibits,
      getSelectedExhibitNamesSet: () => selectedExhibitNames,
   };
}
