import { DayPlannerSchedule } from '../panel/dayPlannerSchedule.js';
import { ScheduleConflictBlockerAnalyzer } from './scheduleConflictBlockerAnalyzer.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';

export class ScheduleConflictCompatibility {
   static isWildEncounterConflictItem(item) {
      return item.item_type === ItinerarySaveIssueItemType.wildEncounter;
   }

   static isGuardiansTalkConflictItem(item) {
      return item.item_type === ItinerarySaveIssueItemType.guardiansTalk;
   }

   static scheduleTimesOverlap(first, second) {
      const firstStart = DayPlannerSchedule.parseClockTimeMinutes(first.start_time);
      const firstEnd = DayPlannerSchedule.parseClockTimeMinutes(first.end_time);
      const secondStart = DayPlannerSchedule.parseClockTimeMinutes(second.start_time);
      const secondEnd = DayPlannerSchedule.parseClockTimeMinutes(second.end_time);

      return firstStart < secondEnd && secondStart < firstEnd;
   }

   static createConflictSelection() {
      return { items: [] };
   }

   static isConflictItemSelected(selection, item) {
      const key = ScheduleConflictBlockerAnalyzer.conflictItemKey(item);

      return selection.items.some(
         (selectedItem) => ScheduleConflictBlockerAnalyzer.conflictItemKey(selectedItem) === key
      );
   }

   static canSelectConflictItem(selection, item) {
      if (ScheduleConflictCompatibility.isConflictItemSelected(selection, item)) {
         return true;
      }

      if (ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)) {
         return !ScheduleConflictBlockerAnalyzer.isGuardiansTalkFullyCoveredByBlockers(
            item,
            ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(selection, item)
         );
      }

      const overlapsSelectedWildEncounter = selection.items.some(
         (selectedItem) => (
            ScheduleConflictCompatibility.isWildEncounterConflictItem(selectedItem)
            && ScheduleConflictCompatibility.scheduleTimesOverlap(selectedItem, item)
         )
      );

      if (overlapsSelectedWildEncounter) {
         return false;
      }

      const wouldFullyCoverSelectedTalk = selection.items.some(
         (selectedItem) => (
            ScheduleConflictCompatibility.isGuardiansTalkConflictItem(selectedItem)
            && ScheduleConflictCompatibility.scheduleTimesOverlap(selectedItem, item)
            && ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
               selectedItem,
               ScheduleConflictBlockerAnalyzer.getGuardiansTalkTrimBlockers(selection, selectedItem, item)
            ) == null
         )
      );

      return !wouldFullyCoverSelectedTalk;
   }

   static conflictItemRequiresTrimOverride(selection, item) {
      if (ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)) {
         if (
            !ScheduleConflictCompatibility.isConflictItemSelected(selection, item)
            && !ScheduleConflictCompatibility.canSelectConflictItem(selection, item)
         ) {
            return false;
         }

         return ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
            item,
            ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(selection, item)
         );
      }

      if (ScheduleConflictCompatibility.isWildEncounterConflictItem(item)) {
         if (!ScheduleConflictCompatibility.canSelectConflictItem(selection, item)) {
            return false;
         }

         return ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(selection, item);
      }

      return false;
   }

   static hasAdditionalSelectableConflictItems(items, selection) {
      if (!selection.items.length) {
         return false;
      }

      return items.some(
         (item) => (
            !ScheduleConflictCompatibility.isConflictItemSelected(selection, item)
            && ScheduleConflictCompatibility.canSelectConflictItem(selection, item)
         )
      );
   }

   static hasAnyAdditionalSelectableConflictItems(conflictGroups = []) {
      return conflictGroups.some(
         (group) => ScheduleConflictCompatibility.hasAdditionalSelectableConflictItems(
            group.items,
            group.selection
         )
      );
   }

   static toggleConflictItemSelection(selection, item) {
      if (ScheduleConflictCompatibility.isConflictItemSelected(selection, item)) {
         const key = ScheduleConflictBlockerAnalyzer.conflictItemKey(item);

         selection.items = selection.items.filter(
            (selectedItem) => ScheduleConflictBlockerAnalyzer.conflictItemKey(selectedItem) !== key
         );

         return;
      }

      if (!ScheduleConflictCompatibility.canSelectConflictItem(selection, item)) {
         return;
      }

      selection.items.push(item);
   }
}
