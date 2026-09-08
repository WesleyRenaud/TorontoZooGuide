import { ValueNormalizer } from '../api/valueNormalizer.js';
import { SearchContext } from '../search/searchContext.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

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
      const presetKey = ValueNormalizer.asTrimmedString(preset).toLowerCase();
      const presetDateCtx = DateContext.PRESET_DATE_CONTEXTS[presetKey];

      if (presetDateCtx) {
         const trimmed = ValueNormalizer.asTrimmedString(dateStr);
         const anchorIso = VisitDateRules.getYear(trimmed) != null ? trimmed : VisitDateRules.toISODate(VisitDateRules.getToday());

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
