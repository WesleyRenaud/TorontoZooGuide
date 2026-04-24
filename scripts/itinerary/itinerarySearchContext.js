import { buildDateSearchContext } from '../search/searchContext.js';
import { getStoredItineraryDate } from './draftStorage.js';

export async function getItineraryDateSearchContext({ includeTemp = true } = {}) {
   const date = getStoredItineraryDate();
   return await buildDateSearchContext(date, { includeTemp });
}
