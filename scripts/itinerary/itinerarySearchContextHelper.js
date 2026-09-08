import { DraftStore } from './draftStore.js';
import { VisitDateResolver } from './visitDateResolver.js';

export class ItinerarySearchContextHelper {
   static async resolveItinerarySearchDate(dateOverride = '') {
      if (dateOverride) {
         return dateOverride;
      }

      const stored = DraftStore.getStoredItineraryDate()?.trim?.();

      if (stored) {
         return stored;
      }

      return VisitDateResolver.resolveEffectiveItineraryHoursDateIso();
   }
}
