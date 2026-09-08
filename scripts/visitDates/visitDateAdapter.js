import { FlatpickrAdapter } from '../datePickers/flatpickrAdapter.js';
import { VisitDateValidator } from './visitDateValidator.js';

export class VisitDateAdapter {
   static initVisitDateFlatpickr(
      inputEl,
      {
         defaultDate = null,
         daysAhead = VisitDateValidator.DEFAULT_DAYS_AHEAD,
         earliestNoon = null,
         clickOpens = true,
         onChange = null,
         onReady = null,
         onClose = null,
         initFlatpickr: initFlatpickrFn = FlatpickrAdapter.initFlatpickr,
         getTodayFn = VisitDateValidator.getToday,
         getMaxDateFn = null,
      } = {}
   ) {
      if (!inputEl) return null;

      inputEl.setAttribute('readonly', 'true');

      const floor = earliestNoon ?? getTodayFn();
      const resolveMaxDate = getMaxDateFn
         ?? ((ahead) => VisitDateValidator.addLocalCalendarDays(getTodayFn(), ahead));

      const safeDefault = VisitDateValidator.clampToAllowedVisitDate(
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
            const safeDate = VisitDateValidator.clampToAllowedVisitDate(
               selected,
               daysAhead,
               floor,
               getTodayFn()
            );

            instance.setDate(safeDate, false);

            onReady?.(
               safeDate,
               VisitDateValidator.toISODate(safeDate),
               instance,
               selectedDates,
               dateStr
            );
         },
         onChange: (selectedDates, dateStr, instance) => {
            const selected = selectedDates?.[0] || safeDefault;
            const safeDate = VisitDateValidator.clampToAllowedVisitDate(
               selected,
               daysAhead,
               floor,
               getTodayFn()
            );

            instance.setDate(safeDate, false);

            onChange?.(
               safeDate,
               VisitDateValidator.toISODate(safeDate),
               instance,
               selectedDates,
               dateStr
            );
         },
         onClose: (selectedDates, dateStr, instance) => {
            inputEl.blur();
            document.activeElement?.blur?.();
            onClose?.(selectedDates, dateStr, instance);
         },
      });

      return fp;
   }
}
