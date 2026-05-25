import { getStoredItineraryDate } from './draftStorage.js';
import { buildDateSearchContext } from '../search/searchContext.js';

export async function getItineraryDateSearchContext({
   includeTemp = true,
   date: dateOverride = '',
} = {}) {
   const date = dateOverride || getStoredItineraryDate();
   return await buildDateSearchContext(date, { includeTemp });
}
