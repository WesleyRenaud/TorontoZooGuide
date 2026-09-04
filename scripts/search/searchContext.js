import { WeatherApi } from '../api/weatherApi.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

export class SearchContext {
   /**
    * Build the shared date context used across search + itinerary + map.
    *
    * @param {string} iso - 'YYYY-MM-DD' (or '')
    * @param {object} opts
    * @param {boolean} opts.includeTemp - if true, fetch forecast temp when applicable
    * @returns {Promise<{date:string, month:string|null, day:number|null, year:number|null, dayOfWeek:number|null, temp:number|null}>}
    */
   static async buildDateSearchContext(iso, { includeTemp = true } = {}) {
      const date = typeof iso === 'string' ? iso : '';

      const month = date ? VisitDateRules.getMonth(date) : null;
      const day = date ? VisitDateRules.getDay(date) : null;
      const year = date ? VisitDateRules.getYear(date) : null;

      const dayOfWeek = date ? VisitDateRules.isoDateToMonFirstDow(date) : null;

      if (!includeTemp || !date) {
         return { date, month, day, year, dayOfWeek, temp: null };
      }

      if (!VisitDateRules.isWithinNextNDays(date, 7)) {
         return { date, month, day, year, dayOfWeek, temp: null };
      }

      try {
         const temp = await WeatherApi.fetchWeatherTempForDate(date);
         return { date, month, day, year, dayOfWeek, temp };
      } catch {
         return { date, month, day, year, dayOfWeek, temp: null };
      }
   }
}
