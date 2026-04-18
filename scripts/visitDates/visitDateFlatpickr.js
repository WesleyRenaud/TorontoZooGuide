import { initFlatpickr } from '../datePickers/flatpickr.js';
import {
   DEFAULT_DAYS_AHEAD,
   getToday,
   getMaxDate,
   clampToAllowedVisitDate,
   toISODate,
} from './visitDateRules.js';

export function initVisitDateFlatpickr(
   inputEl,
   {
      defaultDate = null,
      daysAhead = DEFAULT_DAYS_AHEAD,
      clickOpens = true,
      onChange = null,
      onReady = null,
      onClose = null,
   } = {}
) {
   if (!inputEl) return null;

   inputEl.setAttribute('readonly', 'true');

   const safeDefault = clampToAllowedVisitDate(
      defaultDate || new Date(),
      daysAhead
   );

   const fp = initFlatpickr(inputEl, {
      defaultDate: safeDefault,
      dateFormat: 'Y-m-d',
      minDate: getToday(),
      maxDate: getMaxDate(daysAhead),
      clickOpens,
      allowInput: false,
      monthSelectorType: 'static',
      onReady: (selectedDates, dateStr, instance) => {
         const selected = selectedDates?.[0] || safeDefault;
         const safeDate = clampToAllowedVisitDate(selected, daysAhead);

         instance.setDate(safeDate, false);

         onReady?.(safeDate, toISODate(safeDate), instance, selectedDates, dateStr);
      },
      onChange: (selectedDates, dateStr, instance) => {
         const selected = selectedDates?.[0] || safeDefault;
         const safeDate = clampToAllowedVisitDate(selected, daysAhead);

         instance.setDate(safeDate, false);

         onChange?.(safeDate, toISODate(safeDate), instance, selectedDates, dateStr);
      },
      onClose: (selectedDates, dateStr, instance) => {
         inputEl.blur();
         document.activeElement?.blur?.();
         onClose?.(selectedDates, dateStr, instance);
      },
   });

   return fp;
}
