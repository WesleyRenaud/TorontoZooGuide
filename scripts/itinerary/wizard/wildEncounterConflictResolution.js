import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';

export function isGuardiansTalkConflictItem(item) {
   return item.item_type === ItinerarySaveIssueItemType.guardiansTalk;
}

export function getWildEncounterConflictIssueStartTime(issue) {
   const [earliestItem] = sortScheduledOccurrencesByStartTime(issue?.items ?? []);

   return earliestItem?.start_time ?? '';
}

export function sortWildEncounterConflictIssuesByStartTime(issues = []) {
   return sortScheduledOccurrencesByStartTime(
      issues,
      getWildEncounterConflictIssueStartTime
   );
}

export function getSelectedConflictItems(conflictGroups = []) {
   const selectedItems = conflictGroups.flatMap(
      (group) => group?.selection?.items ?? []
   );
   const seenNames = new Set();

   return selectedItems.filter((item) => {
      if (seenNames.has(item.name)) {
         return false;
      }

      seenNames.add(item.name);
      return true;
   });
}

export function getSelectedWildEncounters(conflictGroups = []) {
   return getSelectedConflictItems(conflictGroups).filter(
      (item) => !isGuardiansTalkConflictItem(item)
   );
}

export function getSelectedGuardiansTalks(conflictGroups = []) {
   return getSelectedConflictItems(conflictGroups).filter(
      isGuardiansTalkConflictItem
   );
}

export function hasWildEncounterConflictSelection(conflictGroups = []) {
   return getSelectedConflictItems(conflictGroups).length > 0;
}

export function hasUnresolvedWildEncounterConflictGroups(conflictGroups = []) {
   if (!conflictGroups.length) {
      return false;
   }

   const selectedGroupCount = conflictGroups.filter(
      (group) => (group?.selection?.items ?? []).length > 0
   ).length;

   return (
      selectedGroupCount > 0
      && selectedGroupCount < conflictGroups.length
   );
}

export function buildItineraryWithSelectedConflictResolutions(
   itinerary,
   selectedItems = [],
) {
   const guardiansTalks = selectedItems.filter(isGuardiansTalkConflictItem);
   const wildEncounters = selectedItems.filter(
      (item) => !isGuardiansTalkConflictItem(item)
   );

   return {
      ...itinerary,
      guardiansTalks: [
         ...itinerary.guardiansTalks,
         ...guardiansTalks,
      ],
      wildEncounters: [
         ...itinerary.wildEncounters,
         ...wildEncounters,
      ],
   };
}

export function buildItineraryWithSelectedWildEncounters(
   itinerary,
   wildEncounters = [],
) {
   return {
      ...itinerary,
      wildEncounters: [
         ...itinerary.wildEncounters,
         ...wildEncounters,
      ],
   };
}
