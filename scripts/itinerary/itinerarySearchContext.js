import { getStoredItineraryDate } from './draftStorage.js';
import { buildDateSearchContext } from '../search/searchContext.js';
import { resolveEffectiveItineraryHoursDateIso } from './visitDateEarliest.js';

async function resolveItinerarySearchDate(dateOverride = '') {
   if (dateOverride) {
      return dateOverride;
   }

   const stored = getStoredItineraryDate()?.trim?.();

   if (stored) {
      return stored;
   }

   return resolveEffectiveItineraryHoursDateIso();
}

export class ItinerarySearchContext {
   static async getItineraryDateSearchContext({
      includeTemp = true,
      date: dateOverride = '',
   } = {}) {
      const date = await resolveItinerarySearchDate(dateOverride);
      return buildDateSearchContext(date, { includeTemp });
   }
}
