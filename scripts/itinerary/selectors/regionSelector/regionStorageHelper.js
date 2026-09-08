import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';

export class RegionStorageHelper {
   static normalizeStoredAnimalKey(key) {
      return StoredSelectionNormalizer.normalizeStoredString(key).toLowerCase();
   }
}
