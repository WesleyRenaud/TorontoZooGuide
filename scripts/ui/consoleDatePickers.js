import { initFlatpickr } from './flatpickr.js';

/* ============================================================
   OFF DISPLAY DATE PICKERS
============================================================ */

export function initOffDisplayDatePickers(
   offDisplayStartDateEl,
   offDisplayEndDateEl
) {

   const startPicker = initFlatpickr(offDisplayStartDateEl, {
      enableTime: false,
      dateFormat: 'Y-m-d',
      minDate: 'today'
   });

   const endPicker = initFlatpickr(offDisplayEndDateEl, {
      enableTime: false,
      dateFormat: 'Y-m-d',
      minDate: 'today'
   });

   if (offDisplayStartDateEl && endPicker) {
      offDisplayStartDateEl.addEventListener('change', () => {

         const startValue = offDisplayStartDateEl.value?.trim();

         if (startValue) {
            endPicker.set('minDate', startValue);
         }
         else {
            endPicker.set('minDate', 'today');
         }
      });
   }

   return { startPicker, endPicker };
}


/* ============================================================
   VISIBILITY SCHEDULE PICKERS
============================================================ */

export function initVisibilityScheduleDateTimePickers(
   startDateEl,
   endDateEl,
   dailyStartTimeEl,
   dailyEndTimeEl
) {
   const startDatePicker = initFlatpickr(startDateEl, {
      enableTime: false,
      dateFormat: 'Y-m-d'
   });

   const endDatePicker = initFlatpickr(endDateEl, {
      enableTime: false,
      dateFormat: 'Y-m-d'
   });

   const dailyStartTimePicker = initFlatpickr(dailyStartTimeEl, {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'h:i K',
      time_24hr: false
   });

   const dailyEndTimePicker = initFlatpickr(dailyEndTimeEl, {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'h:i K',
      time_24hr: false
   });

   if (startDateEl && endDatePicker) {
      startDateEl.addEventListener('change', () => {
         const startValue = startDateEl.value?.trim();

         if (startValue) {
            endDatePicker.set('minDate', startValue);
         }
         else {
            endDatePicker.set('minDate', null);
         }
      });
   }

   return {
      startDatePicker,
      endDatePicker,
      dailyStartTimePicker,
      dailyEndTimePicker
   };
}