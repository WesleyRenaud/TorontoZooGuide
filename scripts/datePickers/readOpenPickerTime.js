import { OpenPickerTimeHelpers } from './openPickerTimeHelpers.js';

export class ReadOpenPickerTime {
   static readOpenPickerTime(instance) {
      if (!instance?.isOpen) {
         return '';
      }

      const dateFormat = OpenPickerTimeHelpers.getPickerDateFormat(instance);

      if (instance.selectedDates?.length) {
         return OpenPickerTimeHelpers.formatPickerDate(instance, instance.selectedDates[0], dateFormat);
      }

      const controlTime = OpenPickerTimeHelpers.readTimeFromPickerControls(instance, dateFormat);

      if (controlTime) {
         return controlTime;
      }

      return instance.latestSelectedDateObj
         ? OpenPickerTimeHelpers.formatPickerDate(instance, instance.latestSelectedDateObj, dateFormat)
         : '';
   }
}
