import { ScheduleConflictChecker } from './scheduleConflictChecker.js';
import { ScheduledOccurrenceSorter } from '../scheduledOccurrenceSorter.js';
import { WildEncounterConflictResolutionHelper } from './wildEncounterConflictResolutionHelper.js';

export class WildEncounterConflictResolver {
   static getWildEncounterConflictIssueStartTime(issue) {
      const [earliestItem] = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(
         issue?.items ?? []
      );

      return earliestItem?.start_time ?? '';
   }

   static sortWildEncounterConflictIssuesByStartTime(issues = []) {
      return ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(
         issues,
         WildEncounterConflictResolver.getWildEncounterConflictIssueStartTime
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
      return WildEncounterConflictResolver.getSelectedConflictItems(conflictGroups).filter(
         (item) => !ScheduleConflictChecker.isGuardiansTalkConflictItem(item)
      );
   }

   static getSelectedGuardiansTalks(conflictGroups = []) {
      return WildEncounterConflictResolver.getSelectedConflictItems(conflictGroups).filter(
         ScheduleConflictChecker.isGuardiansTalkConflictItem
      );
   }

   static hasWildEncounterConflictSelection(conflictGroups = []) {
      return WildEncounterConflictResolver.getSelectedConflictItems(conflictGroups).length > 0;
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
         .filter(ScheduleConflictChecker.isGuardiansTalkConflictItem)
         .map(WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem);
      const wildEncounters = selectedItems
         .filter((item) => !ScheduleConflictChecker.isGuardiansTalkConflictItem(item))
         .map(WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem);

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
         const name = WildEncounterConflictResolutionHelper.getDraftItemName(item);

         return !conflictingNames.has(name) || selectedNames.has(name);
      };

      return {
         ...itinerary,
         guardiansTalks: (itinerary.guardiansTalks ?? []).filter(keepDraftItem),
         wildEncounters: (itinerary.wildEncounters ?? []).filter(keepDraftItem),
      };
   }
}
