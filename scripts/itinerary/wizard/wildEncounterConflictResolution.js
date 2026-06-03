import { isGuardiansTalkConflictItem } from './scheduleConflictCompatibility.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';

export { isGuardiansTalkConflictItem };

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

function toConflictResolutionDraftItem(item) {
   if (isGuardiansTalkConflictItem(item)) {
      return {
         name: item.name,
         location: item.location,
      };
   }

   return {
      name: item.name,
      meeting_spot: item.meeting_spot,
   };
}

export function buildItineraryWithSelectedConflictResolutions(
   itinerary,
   selectedItems = [],
) {
   const guardiansTalks = selectedItems
      .filter(isGuardiansTalkConflictItem)
      .map(toConflictResolutionDraftItem);
   const wildEncounters = selectedItems
      .filter((item) => !isGuardiansTalkConflictItem(item))
      .map(toConflictResolutionDraftItem);

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

function getDraftItemName(item) {
   if (typeof item === 'string') {
      return item;
   }

   return item?.name ?? '';
}

export function applyConflictSelectionToItineraryDraft(
   itinerary,
   issues = [],
   selectedItems = [],
) {
   const selectedNames = new Set(selectedItems.map((item) => item.name));
   const conflictingNames = new Set(
      issues.flatMap(
         (issue) => (issue.items ?? []).map((item) => item.name)
      )
   );

   const keepDraftItem = (item) => {
      const name = getDraftItemName(item);

      return !conflictingNames.has(name) || selectedNames.has(name);
   };

   return {
      ...itinerary,
      guardiansTalks: (itinerary.guardiansTalks ?? []).filter(keepDraftItem),
      wildEncounters: (itinerary.wildEncounters ?? []).filter(keepDraftItem),
   };
}
