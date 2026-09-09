import { DayPlannerScheduleController } from '../panel/dayPlannerScheduleController.js';
import { ScheduleConflictBlockerAnalyzer } from './scheduleConflictBlockerAnalyzer.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';

export class ScheduleConflictChecker {
   static isWildEncounterConflictItem(item) {
      return item.item_type === ItinerarySaveIssueItemType.WILD_ENCOUNTER;
   }

   static isGuardiansTalkConflictItem(item) {
      return item.item_type === ItinerarySaveIssueItemType.GUARDIANS_TALK;
   }

   static scheduleTimesOverlap(first, second) {
      const firstStart = DayPlannerScheduleController.parseClockTimeMinutes(first.start_time);
      const firstEnd = DayPlannerScheduleController.parseClockTimeMinutes(first.end_time);
      const secondStart = DayPlannerScheduleController.parseClockTimeMinutes(second.start_time);
      const secondEnd = DayPlannerScheduleController.parseClockTimeMinutes(second.end_time);

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
      if (ScheduleConflictChecker.isConflictItemSelected(selection, item)) {
         return true;
      }

      if (ScheduleConflictChecker.isGuardiansTalkConflictItem(item)) {
         return !ScheduleConflictBlockerAnalyzer.isGuardiansTalkFullyCoveredByBlockers(
            item,
            ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(selection, item)
         );
      }

      const overlapsSelectedWildEncounter = selection.items.some(
         (selectedItem) => (
            ScheduleConflictChecker.isWildEncounterConflictItem(selectedItem)
            && ScheduleConflictChecker.scheduleTimesOverlap(selectedItem, item)
         )
      );

      if (overlapsSelectedWildEncounter) {
         return false;
      }

      const wouldFullyCoverSelectedTalk = selection.items.some(
         (selectedItem) => (
            ScheduleConflictChecker.isGuardiansTalkConflictItem(selectedItem)
            && ScheduleConflictChecker.scheduleTimesOverlap(selectedItem, item)
            && ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
               selectedItem,
               ScheduleConflictBlockerAnalyzer.getGuardiansTalkTrimBlockers(selection, selectedItem, item)
            ) == null
         )
      );

      return !wouldFullyCoverSelectedTalk;
   }

   static conflictItemRequiresTrimOverride(selection, item) {
      if (ScheduleConflictChecker.isGuardiansTalkConflictItem(item)) {
         if (
            !ScheduleConflictChecker.isConflictItemSelected(selection, item)
            && !ScheduleConflictChecker.canSelectConflictItem(selection, item)
         ) {
            return false;
         }

         return ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
            item,
            ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(selection, item)
         );
      }

      if (ScheduleConflictChecker.isWildEncounterConflictItem(item)) {
         if (!ScheduleConflictChecker.canSelectConflictItem(selection, item)) {
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
            !ScheduleConflictChecker.isConflictItemSelected(selection, item)
            && ScheduleConflictChecker.canSelectConflictItem(selection, item)
         )
      );
   }

   static hasAnyAdditionalSelectableConflictItems(conflictGroups = []) {
      return conflictGroups.some(
         (group) => ScheduleConflictChecker.hasAdditionalSelectableConflictItems(
            group.items,
            group.selection
         )
      );
   }

   static toggleConflictItemSelection(selection, item) {
      if (ScheduleConflictChecker.isConflictItemSelected(selection, item)) {
         const key = ScheduleConflictBlockerAnalyzer.conflictItemKey(item);

         selection.items = selection.items.filter(
            (selectedItem) => ScheduleConflictBlockerAnalyzer.conflictItemKey(selectedItem) !== key
         );

         return;
      }

      if (!ScheduleConflictChecker.canSelectConflictItem(selection, item)) {
         return;
      }

      selection.items.push(item);
   }
}
