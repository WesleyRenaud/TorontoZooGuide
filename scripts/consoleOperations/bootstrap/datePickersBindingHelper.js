import { ConsoleDateFactory } from '../../datePickers/consoleDateFactory.js';

export class DatePickersBindingHelper {
   static getNestedValue(source, path = []) {
      return path.reduce(
         (currentValue, key) => currentValue?.[key],
         source
      );
   }

   static initDateRangePickerBinding(refs, path) {
      const binding = DatePickersBindingHelper.getNestedValue(refs, path);

      ConsoleDateFactory.initDateRangePickers(
         binding?.startDateEl,
         binding?.endDateEl
      );
   }

   static initSingleDatePickerBinding(refs, path) {
      ConsoleDateFactory.initDateRangePickers(
         DatePickersBindingHelper.getNestedValue(refs, path),
         null
      );
   }

   static initDateTimePickerBinding(refs, {
      path,
      startTimeKey,
      endTimeKey = null,
      timeFieldKeys = [],
   } = {}) {
      const binding = DatePickersBindingHelper.getNestedValue(refs, path);

      if (timeFieldKeys.length) {
         timeFieldKeys.forEach((fieldKey) => {
            ConsoleDateFactory.initTimePicker(binding?.[fieldKey]);
         });
         return;
      }

      ConsoleDateFactory.initScheduleDateTimePickers(
         binding?.startDateEl,
         binding?.endDateEl,
         binding?.[startTimeKey],
         endTimeKey ? binding?.[endTimeKey] : null
      );
   }
}
