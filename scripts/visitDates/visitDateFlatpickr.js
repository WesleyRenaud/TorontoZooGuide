import { initFlatpickr } from '../datePickers/flatpickr.js';
import { VisitDateRules } from './visitDateRules.js';

export function initVisitDateFlatpickr(
   inputEl,
   {
      defaultDate = null,
      daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
      earliestNoon = null,
      clickOpens = true,
      onChange = null,
      onReady = null,
      onClose = null,
      initFlatpickr: initFlatpickrFn = initFlatpickr,
      getTodayFn = VisitDateRules.getToday,
      getMaxDateFn = null,
   } = {}
) {
   if (!inputEl) return null;

   inputEl.setAttribute('readonly', 'true');

   const floor = earliestNoon ?? getTodayFn();
   const resolveMaxDate = getMaxDateFn
      ?? ((ahead) => VisitDateRules.addLocalCalendarDays(getTodayFn(), ahead));

   const safeDefault = VisitDateRules.clampToAllowedVisitDate(
      defaultDate || new Date(),
      daysAhead,
      floor,
      getTodayFn()
   );

   const fp = initFlatpickrFn(inputEl, {
      defaultDate: safeDefault,
      dateFormat: 'Y-m-d',
      minDate: floor,
      maxDate: resolveMaxDate(daysAhead),
      clickOpens,
      allowInput: false,
      monthSelectorType: 'static',
      onReady: (selectedDates, dateStr, instance) => {
         const selected = selectedDates?.[0] || safeDefault;
         const safeDate = VisitDateRules.clampToAllowedVisitDate(selected, daysAhead, floor, getTodayFn());

         instance.setDate(safeDate, false);

         onReady?.(safeDate, VisitDateRules.toISODate(safeDate), instance, selectedDates, dateStr);
      },
      onChange: (selectedDates, dateStr, instance) => {
         const selected = selectedDates?.[0] || safeDefault;
         const safeDate = VisitDateRules.clampToAllowedVisitDate(selected, daysAhead, floor, getTodayFn());

         instance.setDate(safeDate, false);

         onChange?.(safeDate, VisitDateRules.toISODate(safeDate), instance, selectedDates, dateStr);
      },
      onClose: (selectedDates, dateStr, instance) => {
         inputEl.blur();
         document.activeElement?.blur?.();
         onClose?.(selectedDates, dateStr, instance);
      },
   });

   return fp;
}
