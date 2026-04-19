import { buildDateSearchContext } from '../search/searchContext.js';

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

export async function buildMapDateContext(preset, dateStr) {
   const presetKey = String(preset || '').trim().toLowerCase();
   const presetDateCtx = PRESET_DATE_CONTEXTS[presetKey];

   if (presetDateCtx) {
      return {
         preset: presetKey,
         ...presetDateCtx,
      };
   }

   return {
      preset: presetKey,
      ...(await buildDateSearchContext(dateStr)),
   };
}
