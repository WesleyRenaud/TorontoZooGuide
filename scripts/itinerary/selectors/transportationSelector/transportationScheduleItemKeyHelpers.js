import { StoredSelection } from '../base/storedSelection.js';

export class TransportationScheduleItemKeyHelpers {
   static addedAsAttractionFromWire(part) {
      const wire = StoredSelection.normalizeStoredString(part);

      if (wire === '1') {
         return true;
      }

      if (wire === '0') {
         return false;
      }

      return null;
   }
}
