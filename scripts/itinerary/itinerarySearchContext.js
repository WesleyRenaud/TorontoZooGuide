import { DraftStorage } from './draftStorage.js';
import { SearchContext } from '../search/searchContext.js';
import { VisitDateEarliest } from './visitDateEarliest.js';

async function resolveItinerarySearchDate(dateOverride = '') {
   if (dateOverride) {
      return dateOverride;
   }

   const stored = DraftStorage.getStoredItineraryDate()?.trim?.();

   if (stored) {
      return stored;
   }

   return VisitDateEarliest.resolveEffectiveItineraryHoursDateIso();
}

export class ItinerarySearchContext {
   static async getItineraryDateSearchContext({
      includeTemp = true,
      date: dateOverride = '',
   } = {}) {
      const date = await resolveItinerarySearchDate(dateOverride);
      return SearchContext.buildDateSearchContext(date, { includeTemp });
   }
}
