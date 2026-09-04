import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Flatpickr } from './flatpickr.js';
import { TimePickerEnterCommit } from './timePickerEnterCommit.js';

const DATE_PICKER_OPTIONS = {
   enableTime: false,
   dateFormat: 'Y-m-d',
};

function initDatePicker(inputEl, options = {}, initFlatpickrFn = Flatpickr.initFlatpickr) {
   return initFlatpickrFn(inputEl, {
      ...DATE_PICKER_OPTIONS,
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
      const startValue = ValueNormalizer.asTrimmedString(startDateEl.value);

      endDatePicker.set('minDate', startValue || emptyMinDate);
   }

   startDateEl.addEventListener('change', syncMinDate);
   syncMinDate();
}

export class ConsoleDatePickers {
   static CONSOLE_TIME_PICKER_OPTIONS = {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'h:i K',
      time_24hr: false,
   };

   static initTimePicker(inputEl, options = {}, initFlatpickrFn = Flatpickr.initFlatpickr) {
      if (!inputEl) {
         return null;
      }

      const {
         onEnterCommit = (time, instance) => TimePickerEnterCommit.commitTimeToInput(
            time,
            instance,
            inputEl
         ),
         onReady,
         ...flatpickrOptions
      } = options;

      function wireEnterCommit(instance) {
         TimePickerEnterCommit.wireTimePickerEnterCommit(inputEl, instance, onEnterCommit);
      }

      const picker = initFlatpickrFn(inputEl, {
         ...ConsoleDatePickers.CONSOLE_TIME_PICKER_OPTIONS,
         ...flatpickrOptions,
         onReady(selectedDates, dateStr, instance) {
            wireEnterCommit(instance);
            onReady?.(selectedDates, dateStr, instance);
         },
      });

      wireEnterCommit(picker);

      return picker;
   }

   static applyScheduleTimePickerBounds(picker, bounds = null) {
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

   static initDateRangePickers(
      startDateEl,
      endDateEl,
      {
         minDate = 'today',
         initFlatpickrFn = Flatpickr.initFlatpickr,
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

   static initScheduleDateTimePickers(
      startDateEl,
      endDateEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      {
         initFlatpickrFn = Flatpickr.initFlatpickr,
      } = {}
   ) {
      const startDatePicker = initDatePicker(startDateEl, {}, initFlatpickrFn);

      const endDatePicker = initDatePicker(endDateEl, {}, initFlatpickrFn);

      const dailyStartTimePicker = ConsoleDatePickers.initTimePicker(
         dailyStartTimeEl,
         {},
         initFlatpickrFn
      );

      const dailyEndTimePicker = ConsoleDatePickers.initTimePicker(
         dailyEndTimeEl,
         {},
         initFlatpickrFn
      );

      bindEndDateMinDate(startDateEl, endDatePicker);

      return {
         startDatePicker,
         endDatePicker,
         dailyStartTimePicker,
         dailyEndTimePicker,
      };
   }

   static initAttractionHoursSchedulePickers({
      startDateEl,
      endDateEl,
      weekdayStartTimeEl,
      weekdayEndTimeEl,
      weekendHolidayStartTimeEl,
      weekendHolidayEndTimeEl,
   } = {}, {
      initFlatpickrFn = Flatpickr.initFlatpickr,
   } = {}) {
      const { startPicker, endPicker } = ConsoleDatePickers.initDateRangePickers(
         startDateEl,
         endDateEl,
         { initFlatpickrFn }
      );

      return {
         startPicker,
         endPicker,
         weekdayStartTimePicker: ConsoleDatePickers.initTimePicker(
            weekdayStartTimeEl,
            {},
            initFlatpickrFn
         ),
         weekdayEndTimePicker: ConsoleDatePickers.initTimePicker(
            weekdayEndTimeEl,
            {},
            initFlatpickrFn
         ),
         weekendHolidayStartTimePicker: ConsoleDatePickers.initTimePicker(
            weekendHolidayStartTimeEl,
            {},
            initFlatpickrFn
         ),
         weekendHolidayEndTimePicker: ConsoleDatePickers.initTimePicker(
            weekendHolidayEndTimeEl,
            {},
            initFlatpickrFn
         ),
      };
   }
}
