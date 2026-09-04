import { AnimalIdentity } from '../../animalIdentity.js';
import { StoredSelection } from '../base/storedSelection.js';
import { DraftStorage } from '../../draftStorage.js';
import { StorageKeys } from '../../storageKeys.js';

function normalizeStoredAnimalKey(key) {
   return StoredSelection.normalizeStoredString(key).toLowerCase();
}

export class RegionStorage {
   static loadSelectedNames(storageKey) {
      return DraftStorage.loadArray(storageKey)
         .map((name) => StoredSelection.normalizeStoredString(name))
         .filter(Boolean);
   }

   static saveSelectedNames(storageKey, names) {
      DraftStorage.saveArray(
         storageKey,
         Array.from(names)
            .map((name) => StoredSelection.normalizeStoredString(name))
            .filter(Boolean)
      );
   }

   static loadRemovedAnimalKeys() {
      return new Set(
         DraftStorage.loadArray(StorageKeys.REMOVED_ANIMALS_KEY)
            .map(normalizeStoredAnimalKey)
            .filter(Boolean)
      );
   }

   static addRemovedAnimalKey(key) {
      const normalizedKey = normalizeStoredAnimalKey(key);

      if (!normalizedKey) {
         return;
      }

      const removedKeys = RegionStorage.loadRemovedAnimalKeys();
      removedKeys.add(normalizedKey);
      DraftStorage.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static restoreRemovedAnimalKey(key) {
      const normalizedKey = normalizeStoredAnimalKey(key);
      const removedKeys = RegionStorage.loadRemovedAnimalKeys();

      if (!removedKeys.delete(normalizedKey)) {
         return;
      }

      DraftStorage.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static clearRemovedAnimalKeys() {
      DraftStorage.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, []);
   }

   static clearRemovedAnimalKeysForExhibit(exhibitName) {
      const normalizedExhibit = AnimalIdentity.normalizeAnimalIdentitySearchFields({
         exhibit: exhibitName,
      }).exhibit;

      if (!normalizedExhibit) {
         return;
      }

      const exhibitSuffix = `||${normalizedExhibit}`;
      const removedKeys = RegionStorage.loadRemovedAnimalKeys();
      const nextKeys = [...removedKeys].filter((key) => !key.endsWith(exhibitSuffix));

      if (nextKeys.length === removedKeys.size) {
         return;
      }

      DraftStorage.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, nextKeys);
   }
}
