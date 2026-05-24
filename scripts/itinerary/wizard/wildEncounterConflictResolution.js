import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';

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

export function getSelectedWildEncounters(conflictGroups = []) {
   const selectedEncounters = conflictGroups
      .map((group) => group?.selection?.item)
      .filter(Boolean);
   const seenNames = new Set();

   return selectedEncounters.filter((encounter) => {
      if (seenNames.has(encounter.name)) {
         return false;
      }

      seenNames.add(encounter.name);
      return true;
   });
}

export function hasWildEncounterConflictSelection(conflictGroups = []) {
   return getSelectedWildEncounters(conflictGroups).length > 0;
}

export function hasUnresolvedWildEncounterConflictGroups(conflictGroups = []) {
   if (!conflictGroups.length) {
      return false;
   }

   const selectedGroupCount = conflictGroups.filter(
      (group) => group?.selection?.item
   ).length;

   return (
      selectedGroupCount > 0
      && selectedGroupCount < conflictGroups.length
   );
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
