import { ScheduleConflictCompatibility } from './scheduleConflictCompatibility.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { WildEncounterConflictResolutionHelpers } from './wildEncounterConflictResolutionHelpers.js';

export class WildEncounterConflictResolution {
   static getWildEncounterConflictIssueStartTime(issue) {
      const [earliestItem] = ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
         issue?.items ?? []
      );

      return earliestItem?.start_time ?? '';
   }

   static sortWildEncounterConflictIssuesByStartTime(issues = []) {
      return ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
         issues,
         WildEncounterConflictResolution.getWildEncounterConflictIssueStartTime
      );
   }

   static getSelectedConflictItems(conflictGroups = []) {
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

   static getSelectedWildEncounters(conflictGroups = []) {
      return WildEncounterConflictResolution.getSelectedConflictItems(conflictGroups).filter(
         (item) => !ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
      );
   }

   static getSelectedGuardiansTalks(conflictGroups = []) {
      return WildEncounterConflictResolution.getSelectedConflictItems(conflictGroups).filter(
         ScheduleConflictCompatibility.isGuardiansTalkConflictItem
      );
   }

   static hasWildEncounterConflictSelection(conflictGroups = []) {
      return WildEncounterConflictResolution.getSelectedConflictItems(conflictGroups).length > 0;
   }

   static hasUnresolvedWildEncounterConflictGroups(conflictGroups = []) {
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

   static buildItineraryWithSelectedConflictResolutions(
      itinerary,
      selectedItems = [],
   ) {
      const guardiansTalks = selectedItems
         .filter(ScheduleConflictCompatibility.isGuardiansTalkConflictItem)
         .map(WildEncounterConflictResolutionHelpers.toConflictResolutionDraftItem);
      const wildEncounters = selectedItems
         .filter((item) => !ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item))
         .map(WildEncounterConflictResolutionHelpers.toConflictResolutionDraftItem);

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

   static buildItineraryWithSelectedWildEncounters(
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

   static applyConflictSelectionToItineraryDraft(
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
         const name = WildEncounterConflictResolutionHelpers.getDraftItemName(item);

         return !conflictingNames.has(name) || selectedNames.has(name);
      };

      return {
         ...itinerary,
         guardiansTalks: (itinerary.guardiansTalks ?? []).filter(keepDraftItem),
         wildEncounters: (itinerary.wildEncounters ?? []).filter(keepDraftItem),
      };
   }
}
