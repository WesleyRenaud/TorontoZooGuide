import {
   formatClockTime,
   normalizeText,
} from '../panel/format.js';
import { ITINERARY_PANEL_SECTION_KEYS } from '../panel/sectionConfigs.js';
import {
   isGuardiansTalkConflictItem,
   isWildEncounterConflictItem,
} from './scheduleConflictCompatibility.js';

function fixedTimeOccurrenceKey(row = {}) {
   const name = normalizeText(row.name).toLowerCase();
   const startTime = formatClockTime(row.start_time);

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

   const nameKey = `name:${normalizeText(row.name).toLowerCase()}`;

   return !rejectedKeys.has(nameKey);
}

export function filterDraftExcludingWarningFixedTimeItems(draft = {}, issues = []) {
   const warningItems = issues.flatMap((issue) => issue.items ?? []);
   const rejectedTalkKeys = rejectedOccurrenceKeys(
      warningItems,
      isGuardiansTalkConflictItem
   );
   const rejectedEncounterKeys = rejectedOccurrenceKeys(
      warningItems,
      isWildEncounterConflictItem
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
