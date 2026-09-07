import { ConsoleDatePickers } from '../../datePickers/consoleDatePickers.js';

export class DatePickersBindingHelpers {
   static getNestedValue(source, path = []) {
      return path.reduce(
         (currentValue, key) => currentValue?.[key],
         source
      );
   }

   static initDateRangePickerBinding(refs, path) {
      const binding = DatePickersBindingHelpers.getNestedValue(refs, path);

      ConsoleDatePickers.initDateRangePickers(
         binding?.startDateEl,
         binding?.endDateEl
      );
   }

   static initSingleDatePickerBinding(refs, path) {
      ConsoleDatePickers.initDateRangePickers(
         DatePickersBindingHelpers.getNestedValue(refs, path),
         null
      );
   }

   static initDateTimePickerBinding(refs, {
      path,
      startTimeKey,
      endTimeKey = null,
      timeFieldKeys = [],
   } = {}) {
      const binding = DatePickersBindingHelpers.getNestedValue(refs, path);

      if (timeFieldKeys.length) {
         timeFieldKeys.forEach((fieldKey) => {
            ConsoleDatePickers.initTimePicker(binding?.[fieldKey]);
         });
         return;
      }

      ConsoleDatePickers.initScheduleDateTimePickers(
         binding?.startDateEl,
         binding?.endDateEl,
         binding?.[startTimeKey],
         endTimeKey ? binding?.[endTimeKey] : null
      );
   }
}
