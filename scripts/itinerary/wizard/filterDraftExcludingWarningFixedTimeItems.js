import { SectionConfigs } from '../panel/sectionConfigs.js';
import { ScheduleConflictCompatibility } from './scheduleConflictCompatibility.js';
import { WarningFixedTimeDraftFilter } from './warningFixedTimeDraftFilter.js';

export class FilterDraftExcludingWarningFixedTimeItems {
   static filterDraftExcludingWarningFixedTimeItems(draft = {}, issues = []) {
      const warningItems = issues.flatMap((issue) => issue.items ?? []);
      const rejectedTalkKeys = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictCompatibility.isGuardiansTalkConflictItem
      );
      const rejectedEncounterKeys = WarningFixedTimeDraftFilter.rejectedOccurrenceKeys(
         warningItems,
         ScheduleConflictCompatibility.isWildEncounterConflictItem
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
