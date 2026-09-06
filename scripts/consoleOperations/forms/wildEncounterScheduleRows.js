import { Strings } from '../../strings.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export class WildEncounterScheduleRows {
   static WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS = [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
      'saturday',
      'sunday',
   ];

   static normalizeWildEncounterScheduleRow(row = {}) {
      const normalized = {
         time: VisitDateRules.formatZooDisplayClockTime(row.time?.trim?.() ?? row.time ?? '') ?? '',
      };

      WildEncounterScheduleRows.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((day) => {
         normalized[day] = Boolean(row[day]);
      });

      return normalized;
   }

   static validateWildEncounterScheduleRows(rows = []) {
      if (!rows.length) {
         return Strings.validation.entityRequired(Strings.labels.encounterTimes);
      }

      const seenTimes = new Set();

      for (const row of rows) {
         const normalized = WildEncounterScheduleRows.normalizeWildEncounterScheduleRow(row);

         if (!normalized.time) {
            return Strings.validation.entityRequired(Strings.labels.encounterTime);
         }

         if (!WildEncounterScheduleRows.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.some(
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
