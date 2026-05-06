import { fetchForecastTemp } from '../api/weatherApi.js';
import {
   getDay,
   getMonth,
   isoDateToMonFirstDow,
   isWithinNextNDays,
} from '../visitDates/visitDateRules.js';

/**
 * Build the shared date context used across search + itinerary + map.
 *
 * @param {string} iso - 'YYYY-MM-DD' (or '')
 * @param {object} opts
 * @param {boolean} opts.includeTemp - if true, fetch forecast temp when applicable
 * @returns {Promise<{date:string, month:string|null, day:number|null, dayOfWeek:number|null, temp:number|null}>}
 */
export async function buildDateSearchContext(iso, { includeTemp = true } = {}) {
   const date = typeof iso === 'string' ? iso : '';

   const month = date ? getMonth(date) : null;
   const day = date ? getDay(date) : null;

   const dayOfWeek = date ? isoDateToMonFirstDow(date) : null;

   if (!includeTemp || !date) {
      return { date, month, day, dayOfWeek, temp: null };
   }

   if (!isWithinNextNDays(date, 7)) {
      return { date, month, day, dayOfWeek, temp: null };
   }

   try {
      const temp = await fetchForecastTemp(date);
      return { date, month, day, dayOfWeek, temp };
   } catch {
      return { date, month, day, dayOfWeek, temp: null };
   }
}
