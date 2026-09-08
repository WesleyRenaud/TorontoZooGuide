import { AnimalIdentity } from '../../animalIdentity.js';
import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { DraftStore } from '../../draftStore.js';
import { RegionStorageHelper } from './regionStorageHelper.js';
import { StorageKeys } from '../../storageKeys.js';

export class RegionStorageStore {
   static loadSelectedNames(storageKey) {
      return DraftStore.loadArray(storageKey)
         .map((name) => StoredSelectionNormalizer.normalizeStoredString(name))
         .filter(Boolean);
   }

   static saveSelectedNames(storageKey, names) {
      DraftStore.saveArray(
         storageKey,
         Array.from(names)
            .map((name) => StoredSelectionNormalizer.normalizeStoredString(name))
            .filter(Boolean)
      );
   }

   static loadRemovedAnimalKeys() {
      return new Set(
         DraftStore.loadArray(StorageKeys.REMOVED_ANIMALS_KEY)
            .map(RegionStorageHelper.normalizeStoredAnimalKey)
            .filter(Boolean)
      );
   }

   static addRemovedAnimalKey(key) {
      const normalizedKey = RegionStorageHelper.normalizeStoredAnimalKey(key);

      if (!normalizedKey) {
         return;
      }

      const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();
      removedKeys.add(normalizedKey);
      DraftStore.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static restoreRemovedAnimalKey(key) {
      const normalizedKey = RegionStorageHelper.normalizeStoredAnimalKey(key);
      const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();

      if (!removedKeys.delete(normalizedKey)) {
         return;
      }

      DraftStore.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static clearRemovedAnimalKeys() {
      DraftStore.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, []);
   }

   static clearRemovedAnimalKeysForExhibit(exhibitName) {
      const normalizedExhibit = AnimalIdentity.normalizeAnimalIdentitySearchFields({
         exhibit: exhibitName,
      }).exhibit;

      if (!normalizedExhibit) {
         return;
      }

      const exhibitSuffix = `||${normalizedExhibit}`;
      const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();
      const nextKeys = [...removedKeys].filter((key) => !key.endsWith(exhibitSuffix));

      if (nextKeys.length === removedKeys.size) {
         return;
      }

      DraftStore.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, nextKeys);
   }
}
