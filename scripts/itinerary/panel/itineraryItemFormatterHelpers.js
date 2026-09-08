import { ValueNormalizer } from '../../api/valueNormalizer.js';

export class ItineraryItemFormatterHelpers {

   static normalizeMaximumDuration(value) {
      const maximumDuration = ValueNormalizer.normalizeNumber(value);
      return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
   }

   static normalizeItineraryNameForSave(value) {
      if (typeof value === 'string') {
         return ValueNormalizer.asTrimmedString(value);
      }

      return ValueNormalizer.asTrimmedString(ValueNormalizer.asObject(value).name);
   }
}
