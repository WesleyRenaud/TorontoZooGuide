import { getStoredItineraryDate } from './draftStorage.js';
import { buildDateSearchContext } from '../search/searchContext.js';

export async function getItineraryDateSearchContext({ includeTemp = true } = {}) {
   const date = getStoredItineraryDate();
   return await buildDateSearchContext(date, { includeTemp });
}
