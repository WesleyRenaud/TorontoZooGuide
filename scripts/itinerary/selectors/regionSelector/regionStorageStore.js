import { AnimalIdentity } from '../../animalIdentity.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { DraftStore } from '../../draftStore.js';
import { StorageKeys } from '../../storageKeys.js';

export class RegionStorageStore {
   static loadSelectedNames(storageKey) {
      return DraftStore.loadArray(storageKey)
         .map((name) => ValueNormalizer.asTrimmedString(name))
         .filter(Boolean);
   }

   static saveSelectedNames(storageKey, names) {
      DraftStore.saveArray(
         storageKey,
         Array.from(names)
            .map((name) => ValueNormalizer.asTrimmedString(name))
            .filter(Boolean)
      );
   }

   static loadRemovedAnimalKeys() {
      return new Set(
         DraftStore.loadArray(StorageKeys.REMOVED_ANIMALS_KEY)
            .map((key) => ValueNormalizer.asTrimmedString(key).toLowerCase())
            .filter(Boolean)
      );
   }

   static addRemovedAnimalKey(key) {
      const normalizedKey = ValueNormalizer.asTrimmedString(key).toLowerCase();

      if (!normalizedKey) {
         return;
      }

      const removedKeys = RegionStorageStore.loadRemovedAnimalKeys();
      removedKeys.add(normalizedKey);
      DraftStore.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static restoreRemovedAnimalKey(key) {
      const normalizedKey = ValueNormalizer.asTrimmedString(key).toLowerCase();
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
