import { Strings } from '../../strings.js';
import { SaveIssuesProceedFragment } from '../wizard/saveIssuesProceedFragment.js';
import { ScheduleConflictChecker } from '../wizard/scheduleConflictChecker.js';
import { WildEncounterConflictResolver } from '../wizard/wildEncounterConflictResolver.js';

export class ScheduleTimeConflictResolver {
   static createScheduleTimeConflictResolutionConfirmations(
      strings = Strings
   ) {
      const confirmation = strings.itinerary.confirmation;

      return {
         showProceedWithoutSelection({ onConfirm } = {}) {
            SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation({
               title: confirmation.proceedWithoutConflictSelectionTitle,
               message: confirmation.proceedWithoutConflictSelectionMessage,
               onConfirm: onConfirm ?? (() => {}),
            });
         },
         showProceedWithUnresolved({ onConfirm } = {}) {
            SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation({
               title: confirmation.proceedWithUnresolvedConflictsTitle,
               message: confirmation.proceedWithUnresolvedConflictsMessage,
               onConfirm,
            });
         },
         showProceedWithAdditional({ onConfirm } = {}) {
            SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation({
               title: confirmation.proceedWithAdditionalSelectableActivitiesTitle,
               message: confirmation.proceedWithAdditionalSelectableActivitiesMessage,
               onConfirm,
            });
         },
      };
   }

   static async resolveScheduleTimeConflictSelection(
      conflictGroups,
      onResolved,
      confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations()
   ) {
      const selectedConflictItems = WildEncounterConflictResolver.getSelectedConflictItems(
         conflictGroups
      );

      if (!WildEncounterConflictResolver.hasWildEncounterConflictSelection(conflictGroups)) {
         confirmations.showProceedWithoutSelection();
         return false;
      }

      if (WildEncounterConflictResolver.hasUnresolvedWildEncounterConflictGroups(conflictGroups)) {
         confirmations.showProceedWithUnresolved({
            onConfirm: async () => {
               await onResolved(selectedConflictItems);
            },
         });

         return false;
      }

      if (ScheduleConflictChecker.hasAnyAdditionalSelectableConflictItems(conflictGroups)) {
         confirmations.showProceedWithAdditional({
            onConfirm: async () => {
               await onResolved(selectedConflictItems);
            },
         });

         return false;
      }

      await onResolved(selectedConflictItems);
      return true;
   }
}
