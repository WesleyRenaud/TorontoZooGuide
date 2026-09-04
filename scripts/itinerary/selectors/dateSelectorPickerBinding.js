import { formatVisitDateLong } from './dateSelectionModel.js';
import { initVisitDateFlatpickr } from '../../visitDates/visitDateFlatpickr.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export function createDatePickerBinding({
   inputEl,
   getDate,
   setDate,
   syncInputValue,
   earliestDateFloor = null,
   initFlatpickr = initVisitDateFlatpickr,
   getTodayFn = VisitDateRules.getToday,
   getMaxDateFn = null,
   daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
} = {}) {
   const floor = earliestDateFloor ?? getTodayFn();
   const resolveMaxDate = getMaxDateFn
      ?? ((ahead) => VisitDateRules.addLocalCalendarDays(getTodayFn(), ahead));
   let flatpickrInstance = null;

   function applyPickerDate(date, instance) {
      setDate(date, { updateInput: true, persist: false });
      instance.input.value = formatVisitDateLong(date);
   }

   function close() {
      flatpickrInstance?.close();
      inputEl?.blur();
   }

   function syncBounds() {
      const currentDate = getDate();

      if (!flatpickrInstance || !currentDate) {
         return;
      }

      flatpickrInstance.set('minDate', floor);
      flatpickrInstance.set('maxDate', resolveMaxDate(daysAhead));
      flatpickrInstance.setDate(currentDate, false);
      syncInputValue(currentDate);
      close();
   }

   function init() {
      flatpickrInstance = initFlatpickr(inputEl, {
         defaultDate: getDate() || floor,
         earliestNoon: floor,
         daysAhead,
         clickOpens: true,
         getTodayFn,
         getMaxDateFn: resolveMaxDate,
         onReady: (safeDate, _isoDate, instance) => {
            applyPickerDate(safeDate, instance);
         },
         onChange: (safeDate, _isoDate, instance) => {
            applyPickerDate(safeDate, instance);
            instance.close();
            inputEl?.blur();
         },
         onClose: () => {
            inputEl?.blur();
         },
      });
   }

   return {
      init,
      close,
      syncBounds,
   };
}
