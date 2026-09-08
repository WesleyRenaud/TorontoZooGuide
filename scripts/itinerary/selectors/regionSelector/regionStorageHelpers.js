import { StoredSelection } from '../base/storedSelection.js';

export class RegionStorageHelpers {
   static normalizeStoredAnimalKey(key) {
      return StoredSelection.normalizeStoredString(key).toLowerCase();
   }
}
