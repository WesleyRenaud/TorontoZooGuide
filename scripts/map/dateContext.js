import { SearchContext } from '../search/searchContext.js';
import { VisitDateValidator } from '../visitDates/visitDateValidator.js';

export class DateContext {
   static PRESET_DATE_CONTEXTS = {
      summer: {
         date: '',
         month: 'JUL',
         day: 20,
         dayOfWeek: null,
         temp: null,
      },
      winter: {
         date: '',
         month: 'JAN',
         day: 30,
         dayOfWeek: null,
         temp: null,
      },
   };

   static async buildMapDateContext(preset, dateStr) {
      const presetKey = String(preset || '').trim().toLowerCase();
      const presetDateCtx = DateContext.PRESET_DATE_CONTEXTS[presetKey];

      if (presetDateCtx) {
         const trimmed = typeof dateStr === 'string' ? dateStr.trim() : '';
         const anchorIso = VisitDateValidator.getYear(trimmed) != null ? trimmed : VisitDateValidator.toISODate(VisitDateValidator.getToday());

         const anchorCtx = await SearchContext.buildDateSearchContext(anchorIso, { includeTemp: false });

         return {
            preset: presetKey,
            ...presetDateCtx,
            year: anchorCtx.year,
         };
      }

      return {
         preset: presetKey,
         ...(await SearchContext.buildDateSearchContext(dateStr)),
      };
   }
}
