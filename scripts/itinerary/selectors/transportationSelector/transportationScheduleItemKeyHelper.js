import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';

export class TransportationScheduleItemKeyHelper {
   static addedAsAttractionFromWire(part) {
      const wire = StoredSelectionNormalizer.normalizeStoredString(part);

      if (wire === '1') {
         return true;
      }

      if (wire === '0') {
         return false;
      }

      return null;
   }
}
