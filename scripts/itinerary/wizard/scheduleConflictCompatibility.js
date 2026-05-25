import { parseClockTimeMinutes } from '../panel/dayPlannerSchedule.js';

export function scheduleTimesOverlap(first, second) {
   const firstStart = parseClockTimeMinutes(first.start_time);
   const firstEnd = parseClockTimeMinutes(first.end_time);
   const secondStart = parseClockTimeMinutes(second.start_time);
   const secondEnd = parseClockTimeMinutes(second.end_time);

   return firstStart < secondEnd && secondStart < firstEnd;
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

export function canSelectConflictItem(selection, item) {
   if (isConflictItemSelected(selection, item)) {
      return true;
   }

   return selection.items.every(
      (selectedItem) => !scheduleTimesOverlap(selectedItem, item)
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
