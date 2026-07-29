import { initFlatpickr } from './flatpickr.js';

const DATE_PICKER_OPTIONS = {
   enableTime: false,
   dateFormat: 'Y-m-d',
};

export const CONSOLE_TIME_PICKER_OPTIONS = {
   enableTime: true,
   noCalendar: true,
   dateFormat: 'h:i K',
   time_24hr: false,
};

function initDatePicker(inputEl, options = {}, initFlatpickrFn = initFlatpickr) {
   return initFlatpickrFn(inputEl, {
      ...DATE_PICKER_OPTIONS,
      ...options,
   });
}

export function initTimePicker(inputEl, options = {}, initFlatpickrFn = initFlatpickr) {
   return initFlatpickrFn(inputEl, {
      ...CONSOLE_TIME_PICKER_OPTIONS,
      ...options,
   });
}

export function applyScheduleTimePickerBounds(picker, bounds = null) {
   if (!picker) {
      return;
   }

   if (!bounds?.openTime || !bounds?.closeTime) {
      picker.set('minTime', null);
      picker.set('maxTime', null);
      return;
   }

   picker.set('minTime', bounds.openTime);
   picker.set('maxTime', bounds.closeTime);
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
      initFlatpickrFn = initFlatpickr,
   } = {}
) {
   const startPicker = initDatePicker(startDateEl, {
      minDate,
   }, initFlatpickrFn);

   const endPicker = initDatePicker(endDateEl, {
      minDate,
   }, initFlatpickrFn);

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
   dailyEndTimeEl,
   {
      initFlatpickrFn = initFlatpickr,
   } = {}
) {
   const startDatePicker = initDatePicker(startDateEl, {}, initFlatpickrFn);

   const endDatePicker = initDatePicker(endDateEl, {}, initFlatpickrFn);

   const dailyStartTimePicker = initTimePicker(dailyStartTimeEl, {}, initFlatpickrFn);

   const dailyEndTimePicker = initTimePicker(dailyEndTimeEl, {}, initFlatpickrFn);

   bindEndDateMinDate(startDateEl, endDatePicker);

   return {
      startDatePicker,
      endDatePicker,
      dailyStartTimePicker,
      dailyEndTimePicker,
   };
}

export function initAttractionHoursSchedulePickers({
   startDateEl,
   endDateEl,
   weekdayStartTimeEl,
   weekdayEndTimeEl,
   weekendHolidayStartTimeEl,
   weekendHolidayEndTimeEl,
} = {}, {
   initFlatpickrFn = initFlatpickr,
} = {}) {
   const { startPicker, endPicker } = initDateRangePickers(
      startDateEl,
      endDateEl,
      { initFlatpickrFn }
   );

   return {
      startPicker,
      endPicker,
      weekdayStartTimePicker: initTimePicker(
         weekdayStartTimeEl,
         {},
         initFlatpickrFn
      ),
      weekdayEndTimePicker: initTimePicker(
         weekdayEndTimeEl,
         {},
         initFlatpickrFn
      ),
      weekendHolidayStartTimePicker: initTimePicker(
         weekendHolidayStartTimeEl,
         {},
         initFlatpickrFn
      ),
      weekendHolidayEndTimePicker: initTimePicker(
         weekendHolidayEndTimeEl,
         {},
         initFlatpickrFn
      ),
   };
}
