import { buildDateSearchContext } from '../search/searchContext.js';
import { DATE_KEY } from './storageKeys.js';

export async function getItineraryDateSearchContext({ includeTemp = true } = {}) {
   const date = localStorage.getItem(DATE_KEY) || '';
   return await buildDateSearchContext(date, { includeTemp });
}
