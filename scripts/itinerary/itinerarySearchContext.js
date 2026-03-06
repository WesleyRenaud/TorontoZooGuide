import { buildDateSearchContext } from '../search/searchContext.js';

const DATE_KEY = 'tzg.itineraryDateISO';

export async function getItineraryDateSearchContext({ includeTemp = true } = {}) {
   const iso = localStorage.getItem(DATE_KEY) || '';
   return await buildDateSearchContext(iso, { includeTemp });
}