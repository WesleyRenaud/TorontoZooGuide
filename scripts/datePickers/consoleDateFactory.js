import { ConsoleDatePickersHelper } from './consoleDatePickersHelper.js';
import { FlatpickrAdapter } from './flatpickrAdapter.js';
import { TimePickerEnterHandler } from './timePickerEnterHandler.js';

export class ConsoleDateFactory {
   static CONSOLE_TIME_PICKER_OPTIONS = {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'h:i K',
      time_24hr: false,
   };

   static initTimePicker(inputEl, options = {}, initFlatpickrFn = FlatpickrAdapter.initFlatpickr) {
      if (!inputEl) {
         return null;
      }

      const {
         onEnterCommit = (time, instance) => TimePickerEnterHandler.commitTimeToInput(
            time,
            instance,
            inputEl
         ),
         onReady,
         ...flatpickrOptions
      } = options;

      function wireEnterCommit(instance) {
         TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, onEnterCommit);
      }

      const picker = initFlatpickrFn(inputEl, {
         ...ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS,
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
         initFlatpickrFn = FlatpickrAdapter.initFlatpickr,
      } = {}
   ) {
      const startPicker = ConsoleDatePickersHelper.initDatePicker(startDateEl, {
         minDate,
      }, initFlatpickrFn);

      const endPicker = ConsoleDatePickersHelper.initDatePicker(endDateEl, {
         minDate,
      }, initFlatpickrFn);

      ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, endPicker, {
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
         initFlatpickrFn = FlatpickrAdapter.initFlatpickr,
      } = {}
   ) {
      const startDatePicker = ConsoleDatePickersHelper.initDatePicker(startDateEl, {}, initFlatpickrFn);

      const endDatePicker = ConsoleDatePickersHelper.initDatePicker(endDateEl, {}, initFlatpickrFn);

      const dailyStartTimePicker = ConsoleDateFactory.initTimePicker(
         dailyStartTimeEl,
         {},
         initFlatpickrFn
      );

      const dailyEndTimePicker = ConsoleDateFactory.initTimePicker(
         dailyEndTimeEl,
         {},
         initFlatpickrFn
      );

      ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, endDatePicker);

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
      initFlatpickrFn = FlatpickrAdapter.initFlatpickr,
   } = {}) {
      const { startPicker, endPicker } = ConsoleDateFactory.initDateRangePickers(
         startDateEl,
         endDateEl,
         { initFlatpickrFn }
      );

      return {
         startPicker,
         endPicker,
         weekdayStartTimePicker: ConsoleDateFactory.initTimePicker(
            weekdayStartTimeEl,
            {},
            initFlatpickrFn
         ),
         weekdayEndTimePicker: ConsoleDateFactory.initTimePicker(
            weekdayEndTimeEl,
            {},
            initFlatpickrFn
         ),
         weekendHolidayStartTimePicker: ConsoleDateFactory.initTimePicker(
            weekendHolidayStartTimeEl,
            {},
            initFlatpickrFn
         ),
         weekendHolidayEndTimePicker: ConsoleDateFactory.initTimePicker(
            weekendHolidayEndTimeEl,
            {},
            initFlatpickrFn
         ),
      };
   }
}
