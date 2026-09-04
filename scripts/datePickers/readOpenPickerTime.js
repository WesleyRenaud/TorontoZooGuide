import { ConsoleDatePickers } from './consoleDatePickers.js';

function getPickerDateFormat(instance) {
   return instance.config?.dateFormat ?? ConsoleDatePickers.CONSOLE_TIME_PICKER_OPTIONS.dateFormat;
}

function formatPickerDate(instance, date, dateFormat) {
   return instance.formatDate(date, dateFormat);
}

function to24HourClock(hour, ampmText) {
   const ampm = ampmText.trim().toUpperCase();

   if (ampm.includes('PM') && hour < 12) {
      return hour + 12;
   }

   if (ampm.includes('AM') && hour === 12) {
      return 0;
   }

   return hour;
}

function readTimeFromPickerControls(instance, dateFormat) {
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
      hour = to24HourClock(hour, instance.amPM?.textContent ?? '');
   }

   const date = new Date();
   date.setHours(hour, minute, 0, 0);
   return formatPickerDate(instance, date, dateFormat);
}

export class ReadOpenPickerTime {
   static readOpenPickerTime(instance) {
      if (!instance?.isOpen) {
         return '';
      }

      const dateFormat = getPickerDateFormat(instance);

      if (instance.selectedDates?.length) {
         return formatPickerDate(instance, instance.selectedDates[0], dateFormat);
      }

      const controlTime = readTimeFromPickerControls(instance, dateFormat);

      if (controlTime) {
         return controlTime;
      }

      return instance.latestSelectedDateObj
         ? formatPickerDate(instance, instance.latestSelectedDateObj, dateFormat)
         : '';
   }
}
