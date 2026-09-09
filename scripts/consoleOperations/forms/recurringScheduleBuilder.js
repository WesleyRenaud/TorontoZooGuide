import { Strings } from '../../strings.js';
import { VisitDateValidator } from '../../visitDates/visitDateValidator.js';

export class RecurringScheduleBuilder {
   static RECURRING_SCHEDULE_WEEKDAY_KEYS = [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
      'saturday',
      'sunday',
   ];

   static normalizeRecurringScheduleRow(row = {}) {
      const normalized = {
         time: VisitDateValidator.formatZooDisplayClockTime(row.time?.trim?.() ?? row.time ?? '') ?? '',
      };

      RecurringScheduleBuilder.RECURRING_SCHEDULE_WEEKDAY_KEYS.forEach((day) => {
         normalized[day] = Boolean(row[day]);
      });

      return normalized;
   }

   static validateRecurringScheduleRows(rows = []) {
      if (!rows.length) {
         return Strings.validation.entityRequired(Strings.labels.encounterTimes);
      }

      const seenTimes = new Set();

      for (const row of rows) {
         const normalized = RecurringScheduleBuilder.normalizeRecurringScheduleRow(row);

         if (!normalized.time) {
            return Strings.validation.entityRequired(Strings.labels.encounterTime);
         }

         if (!RecurringScheduleBuilder.RECURRING_SCHEDULE_WEEKDAY_KEYS.some(
            (day) => normalized[day]
         )) {
            return Strings.validation.encounterScheduleRowNeedsDay;
         }

         if (seenTimes.has(normalized.time)) {
            return Strings.validation.duplicateEncounterTime;
         }

         seenTimes.add(normalized.time);
      }

      return null;
   }
}
