import { DraftStorage } from './draftStorage.js';
import { VisitDateEarliest } from './visitDateEarliest.js';

export class ItinerarySearchContextHelpers {
   static async resolveItinerarySearchDate(dateOverride = '') {
      if (dateOverride) {
         return dateOverride;
      }

      const stored = DraftStorage.getStoredItineraryDate()?.trim?.();

      if (stored) {
         return stored;
      }

      return VisitDateEarliest.resolveEffectiveItineraryHoursDateIso();
   }
}
