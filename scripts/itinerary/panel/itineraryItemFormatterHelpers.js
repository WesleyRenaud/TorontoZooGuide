import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { ItineraryItemFormatter } from './itineraryItemFormatter.js';

export class ItineraryItemFormatterHelpers {
   static asObject(value) {
      return value && typeof value === 'object'
         ? value
         : {};
   }

   static normalizeOptionalText(value) {
      const text = ItineraryItemFormatter.normalizeText(value);
      return text || null;
   }

   static normalizeMaximumDuration(value) {
      const maximumDuration = ValueNormalizer.normalizeNumber(value);
      return maximumDuration && maximumDuration > 0 ? maximumDuration : null;
   }

   static normalizeItineraryNameForSave(value) {
      if (typeof value === 'string') {
         return ItineraryItemFormatter.normalizeText(value);
      }

      return ItineraryItemFormatter.normalizeText(ItineraryItemFormatterHelpers.asObject(value).name);
   }
}
