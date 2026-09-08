import { AnimalIdentity } from '../../animalIdentity.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { DraftStorage } from '../../draftStorage.js';
import { StorageKeys } from '../../storageKeys.js';

export class RegionStorage {
   static loadSelectedNames(storageKey) {
      return DraftStorage.loadArray(storageKey)
         .map((name) => ValueNormalizer.asTrimmedString(name))
         .filter(Boolean);
   }

   static saveSelectedNames(storageKey, names) {
      DraftStorage.saveArray(
         storageKey,
         Array.from(names)
            .map((name) => ValueNormalizer.asTrimmedString(name))
            .filter(Boolean)
      );
   }

   static loadRemovedAnimalKeys() {
      return new Set(
         DraftStorage.loadArray(StorageKeys.REMOVED_ANIMALS_KEY)
            .map((key) => ValueNormalizer.asTrimmedString(key).toLowerCase())
            .filter(Boolean)
      );
   }

   static addRemovedAnimalKey(key) {
      const normalizedKey = ValueNormalizer.asTrimmedString(key).toLowerCase();

      if (!normalizedKey) {
         return;
      }

      const removedKeys = RegionStorage.loadRemovedAnimalKeys();
      removedKeys.add(normalizedKey);
      DraftStorage.saveArray(StorageKeys.REMOVED_ANIMALS_KEY, [...removedKeys]);
   }

   static restoreRemovedAnimalKey(key) {
      const normalizedKey = ValueNormalizer.asTrimmedString(key).toLowerCase();
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
