import { AnimalIdentity } from '../../animalIdentity.js';
import { ItinerarySelectorApi } from '../../../api/itinerarySelectorApi.js';
import { DraftStorage } from '../../draftStorage.js';
import { ItinerarySearchContext } from '../../itinerarySearchContext.js';
import { RegionSelection } from './regionSelection.js';
import { RegionStorage } from './regionStorage.js';
import { buildDateSearchContext } from '../../../search/searchContext.js';
import { SpeciesExhibitKey } from '../../speciesExhibitKey.js';
import { StorageKeys } from '../../storageKeys.js';
import { VisitDateRules } from '../../../visitDates/visitDateRules.js';

async function resolveAnimalsByExhibitQueryContext() {
   let context = await ItinerarySearchContext.getItineraryDateSearchContext();

   if (!context.month || context.day == null) {
      context = await buildDateSearchContext(VisitDateRules.toISODate(VisitDateRules.getToday()));
   }

   return context;
}

export function createRegionSelectorState() {
   let regions = [];

   const selectedRegionNames = new Set();
   const selectedExhibitNames = new Set();
   const bulkManagedExhibitNames = new Set();
   let selectedExhibitsNeedCatalogRebuild = false;

   function markExhibitBulkManaged(exhibitName) {
      const { exhibit: normalizedExhibitName } = AnimalIdentity.normalizeAnimalIdentitySearchFields({
         exhibit: exhibitName,
      });

      if (normalizedExhibitName) {
         bulkManagedExhibitNames.add(normalizedExhibitName);
      }
   }

   function isBulkManagedExhibit(exhibitName) {
      return bulkManagedExhibitNames.has(
         AnimalIdentity.normalizeAnimalIdentitySearchFields({ exhibit: exhibitName }).exhibit
      );
   }

   function persistSelectionState() {
      RegionStorage.saveSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY, selectedExhibitNames);
      RegionStorage.saveSelectedNames(StorageKeys.SELECTED_REGIONS_KEY, selectedRegionNames);
   }

   function syncAllRegionSelections() {
      selectedRegionNames.clear();

      regions.forEach((region) => {
         RegionSelection.syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      });
   }

   function findRegion(regionName) {
      return regions.find((region) => region.name === regionName) ?? null;
   }

   function setRegions(nextRegions = []) {
      regions = RegionSelection.normalizeRegions(nextRegions);

      return regions.slice();
   }

   async function hydrateSelectionsFromStorage() {
      selectedExhibitNames.clear();
      selectedRegionNames.clear();
      bulkManagedExhibitNames.clear();

      const storedExhibits = new Set(RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY));

      regions.forEach((region) => {
         const exhibits = RegionSelection.getRegionExhibits(region);

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
      selectedExhibitsNeedCatalogRebuild = false;

      if (!selectedExhibitNames.size) {
         return;
      }

      const selectedExhibits = Array.from(selectedExhibitNames);
      const draftAnimals = DraftStorage.loadArray(StorageKeys.ANIMALS_KEY)
         .map(RegionSelection.normalizeSelectedAnimal)
         .filter(Boolean);
      const removedKeys = RegionStorage.loadRemovedAnimalKeys();
      const { month, day, temp } = await resolveAnimalsByExhibitQueryContext();
      const catalogAnimals = await ItinerarySelectorApi.getAnimalsByExhibit(selectedExhibits, {
         month,
         day,
         temp,
         forItinerary: true,
      });

      for (const exhibitName of selectedExhibits) {
         const exhibitKey = AnimalIdentity.normalizeAnimalIdentitySearchFields({
            exhibit: exhibitName,
         }).exhibit;
         const catalogForExhibit = catalogAnimals.filter((animal) => (
            AnimalIdentity.normalizeAnimalIdentitySearchFields(animal).exhibit === exhibitKey
         ));

         if (RegionSelection.draftAnimalsCoverCatalogAnimals(draftAnimals, catalogForExhibit)) {
            continue;
         }

         const catalogHasRemovedAnimal = catalogForExhibit.some((animal) => {
            const animalKey = RegionSelection.buildSelectedAnimalKey(animal);

            return animalKey && removedKeys.has(animalKey);
         });

         if (catalogHasRemovedAnimal) {
            // User removed animals from a bulk-selected exhibit.
            selectedExhibitNames.delete(exhibitName);
            continue;
         }

         // Catalog grew (e.g. visit date changed) while the exhibit stayed
         // selected — keep the toggle and rebuild animals before leaving.
         selectedExhibitsNeedCatalogRebuild = true;
      }
   }

   function toggleRegion(regionName) {
      const region = findRegion(regionName);
      if (!region) {
         return false;
      }

      const exhibits = RegionSelection.getRegionExhibits(region);

      if (!exhibits.length) {
         return false;
      }

      const shouldSelect = !RegionSelection.isRegionFullySelected(region, selectedExhibitNames);

      exhibits.forEach((exhibitName) => {
         if (shouldSelect) {
            selectedExhibitNames.add(exhibitName);
            markExhibitBulkManaged(exhibitName);
            RegionStorage.clearRemovedAnimalKeysForExhibit(exhibitName);
         }
         else {
            selectedExhibitNames.delete(exhibitName);
         }
      });

      RegionSelection.syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
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
         RegionStorage.clearRemovedAnimalKeysForExhibit(exhibitName);
      }

      RegionSelection.syncRegionSelection(region, selectedRegionNames, selectedExhibitNames);
      persistSelectionState();

      return true;
   }

   function preserveAnimalsOutsideBulkManagedExhibits(currentAnimals = []) {
      const remainingAnimals = currentAnimals.filter((animal) => {
         const { exhibit } = AnimalIdentity.normalizeAnimalIdentitySearchFields(animal);

         if (!exhibit) {
            return true;
         }

         return !isBulkManagedExhibit(exhibit);
      });

      DraftStorage.saveArray(StorageKeys.ANIMALS_KEY, remainingAnimals);

      return remainingAnimals;
   }

   async function buildUpdatedAnimalsFromSelection() {
      const selectedExhibits = Array.from(selectedExhibitNames);

      const currentAnimals = DraftStorage.loadArray(StorageKeys.ANIMALS_KEY)
         .map(RegionSelection.normalizeSelectedAnimal)
         .filter(Boolean);

      if (!selectedExhibits.length) {
         selectedExhibitsNeedCatalogRebuild = false;
         return preserveAnimalsOutsideBulkManagedExhibits(currentAnimals);
      }

      const { month, day, temp } = await resolveAnimalsByExhibitQueryContext();
      const fullAnimals = await ItinerarySelectorApi.getAnimalsByExhibit(selectedExhibits, {
         month,
         day,
         temp,
         forItinerary: true,
      });
      const selectedAnimals = RegionSelection.omitRemovedAnimals(
         fullAnimals.map(RegionSelection.makeSelectedAnimal).filter(Boolean),
         RegionStorage.loadRemovedAnimalKeys()
      );

      const selectedExhibitSet = new Set(
         selectedExhibits.map(
            (exhibitName) => AnimalIdentity.normalizeAnimalIdentitySearchFields({
               exhibit: exhibitName,
            }).exhibit
         )
      );
      const rebuiltSpeciesExhibitKeys = new Set(
         selectedAnimals.map((animal) => SpeciesExhibitKey.buildSpeciesExhibitKey(animal))
      );

      const preservedAnimals = currentAnimals.filter((animal) => {
         const { exhibit } = AnimalIdentity.normalizeAnimalIdentitySearchFields(animal);

         if (!exhibit) {
            return true;
         }

         if (!selectedExhibitSet.has(exhibit)) {
            return !isBulkManagedExhibit(exhibit);
         }

         return !rebuiltSpeciesExhibitKeys.has(SpeciesExhibitKey.buildSpeciesExhibitKey(animal));
      });

      const mergedAnimals = RegionSelection.mergeAnimals(preservedAnimals, selectedAnimals);
      DraftStorage.saveArray(StorageKeys.ANIMALS_KEY, mergedAnimals);
      selectedExhibitsNeedCatalogRebuild = false;

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
      selectedExhibitsNeedCatalogRebuild: () => selectedExhibitsNeedCatalogRebuild,
   };
}
