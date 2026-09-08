import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class TransportationScheduleItemKeyHelpers {
   static addedAsAttractionFromWire(part) {
      const wire = ValueNormalizer.asTrimmedString(part);

      if (wire === '1') {
         return true;
      }

      if (wire === '0') {
         return false;
      }

      return null;
   }
}
