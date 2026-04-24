import { initFlatpickr } from './flatpickr.js';

const DATE_PICKER_OPTIONS = {
   enableTime: false,
   dateFormat: 'Y-m-d',
};

const TIME_PICKER_OPTIONS = {
   enableTime: true,
   noCalendar: true,
   dateFormat: 'h:i K',
   time_24hr: false,
};

function initDatePicker(inputEl, options = {}) {
   return initFlatpickr(inputEl, {
      ...DATE_PICKER_OPTIONS,
      ...options,
   });
}

function initTimePicker(inputEl, options = {}) {
   return initFlatpickr(inputEl, {
      ...TIME_PICKER_OPTIONS,
      ...options,
   });
}

function bindEndDateMinDate(
   startDateEl,
   endDatePicker,
   {
      emptyMinDate = null,
   } = {}
) {
   if (!startDateEl || !endDatePicker) {
      return;
   }

   function syncMinDate() {
      const startValue = startDateEl.value?.trim() ?? '';

      endDatePicker.set('minDate', startValue || emptyMinDate);
   }

   startDateEl.addEventListener('change', syncMinDate);
   syncMinDate();
}

export function initDateRangePickers(
   startDateEl,
   endDateEl,
   {
      minDate = 'today',
   } = {}
) {
   const startPicker = initDatePicker(startDateEl, {
      minDate,
   });

   const endPicker = initDatePicker(endDateEl, {
      minDate,
   });

   bindEndDateMinDate(startDateEl, endPicker, {
      emptyMinDate: minDate,
   });

   return {
      startPicker,
      endPicker,
   };
}

export function initScheduleDateTimePickers(
   startDateEl,
   endDateEl,
   dailyStartTimeEl,
   dailyEndTimeEl
) {
   const startDatePicker = initDatePicker(startDateEl);

   const endDatePicker = initDatePicker(endDateEl);

   const dailyStartTimePicker = initTimePicker(dailyStartTimeEl);

   const dailyEndTimePicker = initTimePicker(dailyEndTimeEl);

   bindEndDateMinDate(startDateEl, endDatePicker);

   return {
      startDatePicker,
      endDatePicker,
      dailyStartTimePicker,
      dailyEndTimePicker,
   };
}
