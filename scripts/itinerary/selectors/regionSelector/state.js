import { normalizeAnimalIdentitySearchFields } from '../../animalIdentity.js';
import { getAnimalsByExhibit } from '../../../api/itinerarySelectorApi.js';
import {
   loadArray,
   saveArray,
} from '../../draftStorage.js';
import { getItineraryDateSearchContext } from '../../itinerarySearchContext.js';
import {
   draftAnimalsCoverCatalogAnimals,
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
   const bulkManagedExhibitNames = new Set();

   function markExhibitBulkManaged(exhibitName) {
      const { exhibit: normalizedExhibitName } = normalizeAnimalIdentitySearchFields({
         exhibit: exhibitName,
      });

      if (normalizedExhibitName) {
         bulkManagedExhibitNames.add(normalizedExhibitName);
      }
   }

   function isBulkManagedExhibit(exhibitName) {
      return bulkManagedExhibitNames.has(
         normalizeAnimalIdentitySearchFields({ exhibit: exhibitName }).exhibit
      );
   }

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

   async function hydrateSelectionsFromStorage() {
      selectedExhibitNames.clear();
      selectedRegionNames.clear();
      bulkManagedExhibitNames.clear();

      const storedExhibits = new Set(loadSelectedNames(SELECTED_EXHIBITS_KEY));

      regions.forEach((region) => {
         const exhibits = getRegionExhibits(region);

         exhibits.forEach((exhibitName) => {
            if (storedExhibits.has(exhibitName)) {
               selectedExhibitNames.add(exhibitName);
            }
         });
      });

      await pruneIncompleteSelectedExhibits();

      selectedExhibitNames.forEach((exhibitName) => {
         markExhibitBulkManaged(exhibitName);
      });

      syncAllRegionSelections();
      persistSelectionState();
   }

   async function pruneIncompleteSelectedExhibits() {
      if (!selectedExhibitNames.size) {
         return;
      }

      const selectedExhibits = Array.from(selectedExhibitNames);
      const draftAnimals = loadArray(ANIMALS_KEY)
         .map(normalizeSelectedAnimal)
         .filter(Boolean);
      const { month, day, temp } = await resolveAnimalsByExhibitQueryContext();
      const catalogAnimals = await getAnimalsByExhibit(selectedExhibits, {
         month,
         day,
         temp,
         forItinerary: true,
      });

      for (const exhibitName of selectedExhibits) {
         const exhibitKey = normalizeAnimalIdentitySearchFields({
            exhibit: exhibitName,
         }).exhibit;
         const catalogForExhibit = catalogAnimals.filter((animal) => (
            normalizeAnimalIdentitySearchFields(animal).exhibit === exhibitKey
         ));

         if (!draftAnimalsCoverCatalogAnimals(draftAnimals, catalogForExhibit)) {
            selectedExhibitNames.delete(exhibitName);
         }
      }
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
            markExhibitBulkManaged(exhibitName);
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
         markExhibitBulkManaged(exhibitName);
         clearRemovedAnimalKeysForExhibit(exhibitName);
      }

      syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      persistSelectionState();

      return true;
   }

   function preserveAnimalsOutsideBulkManagedExhibits(currentAnimals = []) {
      const remainingAnimals = currentAnimals.filter((animal) => {
         const { exhibit } = normalizeAnimalIdentitySearchFields(animal);

         if (!exhibit) {
            return true;
         }

         return !isBulkManagedExhibit(exhibit);
      });

      saveArray(ANIMALS_KEY, remainingAnimals);

      return remainingAnimals;
   }

   async function buildUpdatedAnimalsFromSelection() {
      const selectedExhibits = Array.from(selectedExhibitNames);

      const currentAnimals = loadArray(ANIMALS_KEY)
         .map(normalizeSelectedAnimal)
         .filter(Boolean);

      if (!selectedExhibits.length) {
         return preserveAnimalsOutsideBulkManagedExhibits(currentAnimals);
      }

      const { month, day, temp } = await resolveAnimalsByExhibitQueryContext();
      const fullAnimals = await getAnimalsByExhibit(selectedExhibits, {
         month,
         day,
         temp,
         forItinerary: true,
      });
      const selectedAnimals = omitRemovedAnimals(
         fullAnimals.map(makeSelectedAnimal).filter(Boolean),
         loadRemovedAnimalKeys()
      );

      const selectedExhibitSet = new Set(
         selectedExhibits.map(
            (exhibitName) => normalizeAnimalIdentitySearchFields({
               exhibit: exhibitName,
            }).exhibit
         )
      );
      const rebuiltSpeciesExhibitKeys = new Set(
         selectedAnimals.map((animal) => buildSpeciesExhibitKey(animal))
      );

      const preservedAnimals = currentAnimals.filter((animal) => {
         const { exhibit } = normalizeAnimalIdentitySearchFields(animal);

         if (!exhibit) {
            return true;
         }

         if (!selectedExhibitSet.has(exhibit)) {
            return !isBulkManagedExhibit(exhibit);
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
