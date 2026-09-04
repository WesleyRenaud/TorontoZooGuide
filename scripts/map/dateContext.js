import { SearchContext } from '../search/searchContext.js';
import { VisitDateRules } from '../visitDates/visitDateRules.js';

const PRESET_DATE_CONTEXTS = {
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

export class DateContext {
   static async buildMapDateContext(preset, dateStr) {
      const presetKey = String(preset || '').trim().toLowerCase();
      const presetDateCtx = PRESET_DATE_CONTEXTS[presetKey];

      if (presetDateCtx) {
         const trimmed = typeof dateStr === 'string' ? dateStr.trim() : '';
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
