import { SectionConfigs } from '../panel/sectionConfigs.js';
import { ScheduleConflictChecker } from './scheduleConflictChecker.js';
import { WarningFixedTimeDraftFilter } from './warningFixedTimeDraftFilter.js';

export class FilterDraftExcludingWarningFixedTimeItems {
   static filterDraftExcludingWarningFixedTimeItems(draft = {}, issues = []) {
      const warningItems = issues.flatMap((issue) => issue.items ?? []);
      const rejectedTalkKeys = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictChecker.isGuardiansTalkConflictItem
      );
      const rejectedEncounterKeys = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictChecker.isWildEncounterConflictItem
      );

      return {
         [SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks]: (
            draft[SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks] ?? []
         ).filter((talk) => WarningFixedTimeDraftFilter.keepDraftItem(talk, rejectedTalkKeys)),
         [SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters]: (
            draft[SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters] ?? []
         ).filter((encounter) => (
            WarningFixedTimeDraftFilter.keepDraftItem(encounter, rejectedEncounterKeys)
         )),
      };
   }
}
