import { DayPlannerSchedule } from '../panel/dayPlannerSchedule.js';
import { ScheduleConflictCompatibility } from './scheduleConflictCompatibility.js';

export class ScheduleConflictBlockerAnalyzer {
   static trimRangeAgainstBlocker(start, end, blockerStart, blockerEnd) {
      if (blockerEnd <= start || blockerStart >= end) {
         return { start, end };
      }

      if (blockerStart <= start && blockerEnd >= end) {
         return null;
      }

      if (blockerStart <= start && blockerEnd < end) {
         return { start: blockerEnd, end };
      }

      if (blockerStart > start && blockerEnd >= end) {
         return { start, end: blockerStart };
      }

      if (blockerStart > start && blockerEnd < end) {
         return { start: blockerEnd, end };
      }

      return null;
   }

   static getTrimmedGuardiansTalkMinutes(talk, blockers = []) {
      let start = DayPlannerSchedule.parseClockTimeMinutes(talk.start_time);
      let end = DayPlannerSchedule.parseClockTimeMinutes(talk.end_time);

      for (const blocker of blockers) {
         const blockerStart = DayPlannerSchedule.parseClockTimeMinutes(blocker.start_time);
         const blockerEnd = DayPlannerSchedule.parseClockTimeMinutes(blocker.end_time);
         const trimmedRange = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
            start,
            end,
            blockerStart,
            blockerEnd
         );

         if (trimmedRange == null) {
            return null;
         }

         start = trimmedRange.start;
         end = trimmedRange.end;
      }

      return { start, end };
   }

   static isGuardiansTalkFullyCoveredByBlockers(talk, blockers = []) {
      const trimmedRange = ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(talk, blockers);

      if (trimmedRange == null) {
         return true;
      }

      return trimmedRange.start >= trimmedRange.end;
   }

   static conflictItemKey(item) {
      return `${item.item_type}::${item.name}`;
   }

   static getSelectionBlockersForItem(selection, item) {
      const blockers = [];
      let reachedCurrentItem = false;

      for (const selectedItem of selection.items) {
         if (ScheduleConflictBlockerAnalyzer.conflictItemKey(selectedItem) === ScheduleConflictBlockerAnalyzer.conflictItemKey(item)) {
            reachedCurrentItem = true;
            continue;
         }

         if (ScheduleConflictCompatibility.isWildEncounterConflictItem(selectedItem)) {
            blockers.push(selectedItem);
            continue;
         }

         if (reachedCurrentItem) {
            continue;
         }

         if (
            ScheduleConflictCompatibility.isGuardiansTalkConflictItem(selectedItem)
            && ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
            && ScheduleConflictCompatibility.scheduleTimesOverlap(selectedItem, item)
         ) {
            blockers.push(selectedItem);
         }
      }

      return blockers;
   }

   static guardiansTalkRequiresTrimOverride(talk, blockers = []) {
      const trimmedRange = ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(talk, blockers);

      if (trimmedRange == null || trimmedRange.start >= trimmedRange.end) {
         return false;
      }

      const originalStart = DayPlannerSchedule.parseClockTimeMinutes(talk.start_time);
      const originalEnd = DayPlannerSchedule.parseClockTimeMinutes(talk.end_time);

      return (
         trimmedRange.start !== originalStart
         || trimmedRange.end !== originalEnd
      );
   }

   static getGuardiansTalkTrimBlockers(selection, talk, extraBlocker = null) {
      const blockers = ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(selection, talk);

      if (
         extraBlocker
         && !blockers.some(
            (blocker) => ScheduleConflictBlockerAnalyzer.conflictItemKey(blocker) === ScheduleConflictBlockerAnalyzer.conflictItemKey(extraBlocker)
         )
      ) {
         blockers.push(extraBlocker);
      }

      return blockers;
   }

   static encounterHasScheduleExceptionWithSelectedTalks(selection, encounter) {
      return selection.items.some(
         (selectedItem) => {
            if (!ScheduleConflictCompatibility.isGuardiansTalkConflictItem(selectedItem)) {
               return false;
            }

            if (!ScheduleConflictCompatibility.scheduleTimesOverlap(selectedItem, encounter)) {
               return false;
            }

            const blockers = ScheduleConflictBlockerAnalyzer.getGuardiansTalkTrimBlockers(
               selection,
               selectedItem,
               encounter
            );
            const trimmedRange = ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
               selectedItem,
               blockers
            );

            if (trimmedRange == null) {
               return true;
            }

            return ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(selectedItem, blockers);
         }
      );
   }
}
