import { ItinerarySearchContextHelpers } from './itinerarySearchContextHelpers.js';
import { SearchContext } from '../search/searchContext.js';

export class ItinerarySearchContext {
   static async getItineraryDateSearchContext({
      includeTemp = true,
      date: dateOverride = '',
   } = {}) {
      const date = await ItinerarySearchContextHelpers.resolveItinerarySearchDate(dateOverride);
      return SearchContext.buildDateSearchContext(date, { includeTemp });
   }
}
