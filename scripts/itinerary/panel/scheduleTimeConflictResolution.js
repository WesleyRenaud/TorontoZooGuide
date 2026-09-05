import { APP_STRINGS } from '../../strings.js';
import { SaveIssuesProceedConfirmation } from '../wizard/saveIssuesProceedConfirmation.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';
import { WildEncounterConflictResolution } from '../wizard/wildEncounterConflictResolution.js';

export class ScheduleTimeConflictResolution {
   static createScheduleTimeConflictResolutionConfirmations(
      strings = APP_STRINGS
   ) {
      const confirmation = strings.itinerary.confirmation;

      return {
         showProceedWithoutSelection({ onConfirm } = {}) {
            SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation({
               title: confirmation.proceedWithoutConflictSelectionTitle,
               message: confirmation.proceedWithoutConflictSelectionMessage,
               onConfirm: onConfirm ?? (() => {}),
            });
         },
         showProceedWithUnresolved({ onConfirm } = {}) {
            SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation({
               title: confirmation.proceedWithUnresolvedConflictsTitle,
               message: confirmation.proceedWithUnresolvedConflictsMessage,
               onConfirm,
            });
         },
         showProceedWithAdditional({ onConfirm } = {}) {
            SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation({
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
      confirmations = ScheduleTimeConflictResolution.createScheduleTimeConflictResolutionConfirmations()
   ) {
      const selectedConflictItems = WildEncounterConflictResolution.getSelectedConflictItems(
         conflictGroups
      );

      if (!WildEncounterConflictResolution.hasWildEncounterConflictSelection(conflictGroups)) {
         confirmations.showProceedWithoutSelection();
         return false;
      }

      if (WildEncounterConflictResolution.hasUnresolvedWildEncounterConflictGroups(conflictGroups)) {
         confirmations.showProceedWithUnresolved({
            onConfirm: async () => {
               await onResolved(selectedConflictItems);
            },
         });

         return false;
      }

      if (ScheduleConflictCompatibility.hasAnyAdditionalSelectableConflictItems(conflictGroups)) {
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
