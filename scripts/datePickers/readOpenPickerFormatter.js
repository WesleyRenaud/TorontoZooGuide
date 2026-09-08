import { OpenPickerTimeHelper } from './openPickerTimeHelper.js';

export class ReadOpenPickerFormatter {
   static readOpenPickerTime(instance) {
      if (!instance?.isOpen) {
         return '';
      }

      const dateFormat = OpenPickerTimeHelper.getPickerDateFormat(instance);

      if (instance.selectedDates?.length) {
         return OpenPickerTimeHelper.formatPickerDate(instance, instance.selectedDates[0], dateFormat);
      }

      const controlTime = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

      if (controlTime) {
         return controlTime;
      }

      return instance.latestSelectedDateObj
         ? OpenPickerTimeHelper.formatPickerDate(instance, instance.latestSelectedDateObj, dateFormat)
         : '';
   }
}
