import { ValueNormalizer } from '../api/valueNormalizer.js';

export class ZooClockTimeHelper {
   static parseMinutes(timeValue) {
      const normalizedTimeValue = ValueNormalizer.asTrimmedString(timeValue);
      const timeParts = normalizedTimeValue.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?$/);

      if (timeParts) {
         const hours = Number(timeParts[1]);
         const minutes = Number(timeParts[2]);
         const seconds = timeParts[3] == null ? 0 : Number(timeParts[3]);

         if (
            hours < 0
            || hours > 23
            || minutes < 0
            || minutes > 59
            || seconds < 0
            || seconds > 59
         ) {
            return null;
         }

         return (hours * 60) + minutes + (seconds / 60);
      }

      const displayTimeParts = normalizedTimeValue.match(
         /^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i
      );

      if (!displayTimeParts) {
         return null;
      }

      const displayHours = Number(displayTimeParts[1]);
      const displayMinutes = Number(displayTimeParts[2]);
      const displaySeconds = displayTimeParts[3] == null
         ? 0
         : Number(displayTimeParts[3]);
      const period = displayTimeParts[4].toUpperCase();

      if (
         displayHours < 1
         || displayHours > 12
         || displayMinutes < 0
         || displayMinutes > 59
         || displaySeconds < 0
         || displaySeconds > 59
      ) {
         return null;
      }

      const hours = (displayHours % 12) + (period === 'PM' ? 12 : 0);

      return (hours * 60) + displayMinutes + (displaySeconds / 60);
   }

   static formatDisplay(timeValue) {
      const minutes = ZooClockTimeHelper.parseMinutes(timeValue);

      if (minutes == null) {
         return null;
      }

      const totalMinutes = Math.floor(minutes);
      const hours24 = Math.floor(totalMinutes / 60);
      const mins = totalMinutes % 60;
      const period = hours24 >= 12 ? 'PM' : 'AM';
      const hours12 = hours24 % 12 || 12;

      return `${hours12}:${String(mins).padStart(2, '0')} ${period}`;
   }

   static normalizeScheduleTime(timeValue) {
      return ZooClockTimeHelper.formatDisplay(timeValue);
   }

   static formatClockTime(timeValue, fallback = '') {
      const trimmedTimeValue = ValueNormalizer.asTrimmedString(timeValue);

      if (!trimmedTimeValue) {
         return fallback;
      }

      const timeParts = trimmedTimeValue.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?$/);

      if (!timeParts) {
         return trimmedTimeValue;
      }

      const hours = Number(timeParts[1]);
      const minutes = Number(timeParts[2]);
      const seconds = timeParts[3] == null ? 0 : Number(timeParts[3]);
      const period = hours >= 12 ? 'PM' : 'AM';
      const displayHours = hours % 12 || 12;
      const secondsLabel = seconds > 0
         ? `:${String(seconds).padStart(2, '0')}`
         : '';

      return `${displayHours}:${String(minutes).padStart(2, '0')}${secondsLabel} ${period}`;
   }
}
