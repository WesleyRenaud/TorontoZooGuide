import { ConsoleDatePickers } from './consoleDatePickers.js';

export class OpenPickerTimeHelpers {
   static getPickerDateFormat(instance) {
      return instance.config?.dateFormat ?? ConsoleDatePickers.CONSOLE_TIME_PICKER_OPTIONS.dateFormat;
   }

   static formatPickerDate(instance, date, dateFormat) {
      return instance.formatDate(date, dateFormat);
   }

   static to24HourClock(hour, ampmText) {
      const ampm = ampmText.trim().toUpperCase();

      if (ampm.includes('PM') && hour < 12) {
         return hour + 12;
      }

      if (ampm.includes('AM') && hour === 12) {
         return 0;
      }

      return hour;
   }

   static readTimeFromPickerControls(instance, dateFormat) {
      const { hourElement, minuteElement } = instance;

      if (!hourElement || !minuteElement || minuteElement.value === '') {
         return '';
      }

      let hour = parseInt(hourElement.value, 10);
      const minute = parseInt(minuteElement.value, 10);

      if (Number.isNaN(hour) || Number.isNaN(minute)) {
         return '';
      }

      if (!instance.config?.time_24hr) {
         hour = OpenPickerTimeHelpers.to24HourClock(hour, instance.amPM?.textContent ?? '');
      }

      const date = new Date();
      date.setHours(hour, minute, 0, 0);
      return OpenPickerTimeHelpers.formatPickerDate(instance, date, dateFormat);
   }
}
