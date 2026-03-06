import { getMonth, getDay, isWithinNextNDays } from '../utils/dates.js';
import { fetchForecastTemp } from '../map/weather.js';
import { isoDateToMonFirstDow } from '../itinerary/itineraryHelpers.js';

/**
 * Build the shared date context used across search + itinerary + map.
 *
 * @param {string} iso - 'YYYY-MM-DD' (or '')
 * @param {object} opts
 * @param {boolean} opts.includeTemp - if true, fetch forecast temp when applicable
 * @returns {Promise<{dateISO:string, month:string|null, day:number|null, dayOfWeek:number|null, temp:number|null}>}
 */
export async function buildDateSearchContext(iso, { includeTemp = true } = {}) {
   const dateISO = typeof iso === 'string' ? iso : '';

   const month = dateISO ? getMonth(dateISO) : null;
   const day = dateISO ? getDay(dateISO) : null;

   const dayOfWeek = dateISO ? isoDateToMonFirstDow(dateISO) : null;

   if (!includeTemp || !dateISO) {
      return { dateISO, month, day, dayOfWeek, temp: null };
   }

   if (!isWithinNextNDays(dateISO, 7)) {
      return { dateISO, month, day, dayOfWeek, temp: null };
   }

   try {
      const temp = await fetchForecastTemp(dateISO);
      return { dateISO, month, day, dayOfWeek, temp };
   } catch {
      return { dateISO, month, day, dayOfWeek, temp: null };
   }
}