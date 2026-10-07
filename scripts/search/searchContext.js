import { VisitDateValidator } from '../visitDates/visitDateValidator.js';
import { DailyHighTemperatureResolver } from '../weather/dailyHighTemperatureResolver.js';

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

      const month = date ? VisitDateValidator.getMonth(date) : null;
      const day = date ? VisitDateValidator.getDay(date) : null;
      const year = date ? VisitDateValidator.getYear(date) : null;

      const dayOfWeek = date ? VisitDateValidator.isoDateToMonFirstDow(date) : null;

      if (!includeTemp || !date) {
         return { date, month, day, year, dayOfWeek, temp: null };
      }

      if (!VisitDateValidator.isWithinNextNDays(date, 7)) {
         return { date, month, day, year, dayOfWeek, temp: null };
      }

      try {
         const temp = await DailyHighTemperatureResolver.resolve(date);
         return { date, month, day, year, dayOfWeek, temp };
      } catch {
         return { date, month, day, year, dayOfWeek, temp: null };
      }
   }
}
