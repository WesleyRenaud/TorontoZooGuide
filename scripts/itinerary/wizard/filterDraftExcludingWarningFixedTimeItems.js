import { Format } from '../panel/format.js';
import { ITINERARY_PANEL_SECTION_KEYS } from '../panel/sectionConfigs.js';
import { ScheduleConflictCompatibility } from './scheduleConflictCompatibility.js';

function fixedTimeOccurrenceKey(row = {}) {
   const name = Format.normalizeText(row.name).toLowerCase();
   const startTime = Format.formatClockTime(row.start_time);

   if (!name) {
      return '';
   }

   return startTime
      ? `${name}\0${startTime}`
      : `name:${name}`;
}

function rejectedOccurrenceKeys(items, isItemType) {
   return new Set(
      items
         .filter(isItemType)
         .map(fixedTimeOccurrenceKey)
         .filter(Boolean)
   );
}

function keepDraftItem(row, rejectedKeys) {
   const key = fixedTimeOccurrenceKey(row);

   if (key && rejectedKeys.has(key)) {
      return false;
   }

   const nameKey = `name:${Format.normalizeText(row.name).toLowerCase()}`;

   return !rejectedKeys.has(nameKey);
}

export class FilterDraftExcludingWarningFixedTimeItems {
   static filterDraftExcludingWarningFixedTimeItems(draft = {}, issues = []) {
      const warningItems = issues.flatMap((issue) => issue.items ?? []);
      const rejectedTalkKeys = rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictCompatibility.isGuardiansTalkConflictItem
      );
      const rejectedEncounterKeys = rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictCompatibility.isWildEncounterConflictItem
      );

      return {
         [ITINERARY_PANEL_SECTION_KEYS.guardiansTalks]: (
            draft[ITINERARY_PANEL_SECTION_KEYS.guardiansTalks] ?? []
         ).filter((talk) => keepDraftItem(talk, rejectedTalkKeys)),
         [ITINERARY_PANEL_SECTION_KEYS.wildEncounters]: (
            draft[ITINERARY_PANEL_SECTION_KEYS.wildEncounters] ?? []
         ).filter((encounter) => (
            keepDraftItem(encounter, rejectedEncounterKeys)
         )),
      };
   }
}
