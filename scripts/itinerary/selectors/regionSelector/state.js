import { getAnimalsByExhibit } from '../../../api/itinerarySelectorApi.js';
import {
   loadArray,
   saveArray,
} from '../../draftStorage.js';
import { getItineraryDateSearchContext } from '../../itinerarySearchContext.js';
import {
   getRegionExhibits,
   isRegionFullySelected,
   makeSelectedAnimal,
   mergeAnimals,
   normalizeRegions,
   normalizeSelectedAnimal,
   omitRemovedAnimals,
   syncRegionSelection,
} from './regionSelection.js';
import {
   clearRemovedAnimalKeysForExhibit,
   loadRemovedAnimalKeys,
   loadSelectedNames,
   saveSelectedNames,
} from './regionStorage.js';
import { buildDateSearchContext } from '../../../search/searchContext.js';
import { buildSpeciesExhibitKey } from '../../speciesExhibitKey.js';
import {
   ANIMALS_KEY,
   SELECTED_EXHIBITS_KEY,
   SELECTED_REGIONS_KEY,
} from '../../storageKeys.js';
import {
   getToday,
   toISODate,
} from '../../../visitDates/visitDateRules.js';

async function resolveAnimalsByExhibitQueryContext() {
   let context = await getItineraryDateSearchContext();

   if (!context.month || context.day == null) {
      context = await buildDateSearchContext(toISODate(getToday()));
   }

   return context;
}

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
         syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      });
   }

   function findRegion(regionName) {
      return regions.find((region) => region.name === regionName) ?? null;
   }

   function setRegions(nextRegions = []) {
      regions = normalizeRegions(nextRegions);

      return regions.slice();
   }

   function hydrateSelectionsFromStorage() {
      selectedExhibitNames.clear();
      selectedRegionNames.clear();

      const storedExhibits = new Set(loadSelectedNames(SELECTED_EXHIBITS_KEY));

      regions.forEach((region) => {
         const exhibits = getRegionExhibits(region);

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
      if (!region) {
         return false;
      }

      const exhibits = getRegionExhibits(region);

      if (!exhibits.length) {
         return false;
      }

      const shouldSelect = !isRegionFullySelected(region, selectedExhibitNames);

      exhibits.forEach((exhibitName) => {
         if (shouldSelect) {
            selectedExhibitNames.add(exhibitName);
            clearRemovedAnimalKeysForExhibit(exhibitName);
         }
         else {
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
      }
      else {
         selectedExhibitNames.add(exhibitName);
         clearRemovedAnimalKeysForExhibit(exhibitName);
      }

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      persistSelectionState();

      return true;
   }

   async function buildUpdatedAnimalsFromSelection() {
      const selectedExhibits = Array.from(selectedExhibitNames);

      if (!selectedExhibits.length) {
         saveArray(ANIMALS_KEY, []);
         return [];
      }

      const currentAnimals = loadArray(ANIMALS_KEY)
         .map(normalizeSelectedAnimal)
         .filter(Boolean);

      const { month, day, temp } = await resolveAnimalsByExhibitQueryContext();
      const fullAnimals = await getAnimalsByExhibit(selectedExhibits, {
         month,
         day,
         temp,
      });
      const selectedAnimals = omitRemovedAnimals(
         fullAnimals.map(makeSelectedAnimal).filter(Boolean),
         loadRemovedAnimalKeys()
      );

      const selectedExhibitSet = new Set(
         selectedExhibits.map((exhibitName) => String(exhibitName).trim().toLowerCase())
      );
      const rebuiltSpeciesExhibitKeys = new Set(
         selectedAnimals.map((animal) => buildSpeciesExhibitKey(animal))
      );

      const preservedAnimals = currentAnimals.filter((animal) => {
         const exhibit = animal.exhibit.trim().toLowerCase();

         if (!exhibit) {
            return true;
         }

         if (!selectedExhibitSet.has(exhibit)) {
            return true;
         }

         return !rebuiltSpeciesExhibitKeys.has(buildSpeciesExhibitKey(animal));
      });

      const mergedAnimals = mergeAnimals(preservedAnimals, selectedAnimals);
      saveArray(ANIMALS_KEY, mergedAnimals);

      return mergedAnimals;
   }

   function getRegions() {
      return regions.slice();
   }

   return {
      setRegions,
      hydrateSelectionsFromStorage,
      toggleRegion,
      toggleExhibit,
      buildUpdatedAnimalsFromSelection,
      getRegions,
      getSelectedExhibitNamesSet: () => selectedExhibitNames,
   };
}
