import { parseClockTimeMinutes } from '../panel/dayPlannerSchedule.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';

export function isWildEncounterConflictItem(item) {
   return item.item_type === ItinerarySaveIssueItemType.wildEncounter;
}

export function isGuardiansTalkConflictItem(item) {
   return item.item_type === ItinerarySaveIssueItemType.guardiansTalk;
}

export function scheduleTimesOverlap(first, second) {
   const firstStart = parseClockTimeMinutes(first.start_time);
   const firstEnd = parseClockTimeMinutes(first.end_time);
   const secondStart = parseClockTimeMinutes(second.start_time);
   const secondEnd = parseClockTimeMinutes(second.end_time);

   return firstStart < secondEnd && secondStart < firstEnd;
}

function trimRangeAgainstBlocker(start, end, blockerStart, blockerEnd) {
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

function getTrimmedGuardiansTalkMinutes(talk, blockers = []) {
   let start = parseClockTimeMinutes(talk.start_time);
   let end = parseClockTimeMinutes(talk.end_time);

   for (const blocker of blockers) {
      const blockerStart = parseClockTimeMinutes(blocker.start_time);
      const blockerEnd = parseClockTimeMinutes(blocker.end_time);
      const trimmedRange = trimRangeAgainstBlocker(
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

function isGuardiansTalkFullyCoveredByBlockers(talk, blockers = []) {
   const trimmedRange = getTrimmedGuardiansTalkMinutes(talk, blockers);

   if (trimmedRange == null) {
      return true;
   }

   return trimmedRange.start >= trimmedRange.end;
}

function getSelectionBlockersForItem(selection, item) {
   const blockers = [];
   let reachedCurrentItem = false;

   for (const selectedItem of selection.items) {
      if (conflictItemKey(selectedItem) === conflictItemKey(item)) {
         reachedCurrentItem = true;
         continue;
      }

      if (isWildEncounterConflictItem(selectedItem)) {
         blockers.push(selectedItem);
         continue;
      }

      if (reachedCurrentItem) {
         continue;
      }

      if (
         isGuardiansTalkConflictItem(selectedItem)
         && isGuardiansTalkConflictItem(item)
         && scheduleTimesOverlap(selectedItem, item)
      ) {
         blockers.push(selectedItem);
      }
   }

   return blockers;
}

export function createConflictSelection() {
   return { items: [] };
}

function conflictItemKey(item) {
   return `${item.item_type}::${item.name}`;
}

export function isConflictItemSelected(selection, item) {
   const key = conflictItemKey(item);

   return selection.items.some(
      (selectedItem) => conflictItemKey(selectedItem) === key
   );
}

export function canSelectConflictItem(selection, item) {
   if (isConflictItemSelected(selection, item)) {
      return true;
   }

   if (isGuardiansTalkConflictItem(item)) {
      return !isGuardiansTalkFullyCoveredByBlockers(
         item,
         getSelectionBlockersForItem(selection, item)
      );
   }

   const overlapsSelectedWildEncounter = selection.items.some(
      (selectedItem) => (
         isWildEncounterConflictItem(selectedItem)
         && scheduleTimesOverlap(selectedItem, item)
      )
   );

   if (overlapsSelectedWildEncounter) {
      return false;
   }

   const wouldFullyCoverSelectedTalk = selection.items.some(
      (selectedItem) => (
         isGuardiansTalkConflictItem(selectedItem)
         && scheduleTimesOverlap(selectedItem, item)
         && getTrimmedGuardiansTalkMinutes(
            selectedItem,
            getGuardiansTalkTrimBlockers(selection, selectedItem, item)
         ) == null
      )
   );

   return !wouldFullyCoverSelectedTalk;
}

function guardiansTalkRequiresTrimOverride(talk, blockers = []) {
   const trimmedRange = getTrimmedGuardiansTalkMinutes(talk, blockers);

   if (trimmedRange == null || trimmedRange.start >= trimmedRange.end) {
      return false;
   }

   const originalStart = parseClockTimeMinutes(talk.start_time);
   const originalEnd = parseClockTimeMinutes(talk.end_time);

   return (
      trimmedRange.start !== originalStart
      || trimmedRange.end !== originalEnd
   );
}

function getGuardiansTalkTrimBlockers(selection, talk, extraBlocker = null) {
   const blockers = getSelectionBlockersForItem(selection, talk);

   if (
      extraBlocker
      && !blockers.some(
         (blocker) => conflictItemKey(blocker) === conflictItemKey(extraBlocker)
      )
   ) {
      blockers.push(extraBlocker);
   }

   return blockers;
}

function encounterHasScheduleExceptionWithSelectedTalks(selection, encounter) {
   return selection.items.some(
      (selectedItem) => {
         if (!isGuardiansTalkConflictItem(selectedItem)) {
            return false;
         }

         if (!scheduleTimesOverlap(selectedItem, encounter)) {
            return false;
         }

         const blockers = getGuardiansTalkTrimBlockers(
            selection,
            selectedItem,
            encounter
         );
         const trimmedRange = getTrimmedGuardiansTalkMinutes(
            selectedItem,
            blockers
         );

         if (trimmedRange == null) {
            return true;
         }

         return guardiansTalkRequiresTrimOverride(selectedItem, blockers);
      }
   );
}

export function conflictItemRequiresTrimOverride(selection, item) {
   if (isGuardiansTalkConflictItem(item)) {
      if (
         !isConflictItemSelected(selection, item)
         && !canSelectConflictItem(selection, item)
      ) {
         return false;
      }

      return guardiansTalkRequiresTrimOverride(
         item,
         getSelectionBlockersForItem(selection, item)
      );
   }

   if (isWildEncounterConflictItem(item)) {
      if (!canSelectConflictItem(selection, item)) {
         return false;
      }

      return encounterHasScheduleExceptionWithSelectedTalks(selection, item);
   }

   return false;
}

export function hasAdditionalSelectableConflictItems(items, selection) {
   if (!selection.items.length) {
      return false;
   }

   return items.some(
      (item) => (
         !isConflictItemSelected(selection, item)
         && canSelectConflictItem(selection, item)
      )
   );
}

export function hasAnyAdditionalSelectableConflictItems(conflictGroups = []) {
   return conflictGroups.some(
      (group) => hasAdditionalSelectableConflictItems(
         group.items,
         group.selection
      )
   );
}

export function toggleConflictItemSelection(selection, item) {
   if (isConflictItemSelected(selection, item)) {
      const key = conflictItemKey(item);

      selection.items = selection.items.filter(
         (selectedItem) => conflictItemKey(selectedItem) !== key
      );

      return;
   }

   if (!canSelectConflictItem(selection, item)) {
      return;
   }

   selection.items.push(item);
}
