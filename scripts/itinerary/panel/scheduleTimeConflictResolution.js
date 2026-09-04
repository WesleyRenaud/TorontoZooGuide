import { APP_STRINGS } from '../../strings.js';
import { showSaveIssuesProceedConfirmation } from '../wizard/saveIssuesProceedConfirmation.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';
import {
   getSelectedConflictItems,
   hasUnresolvedWildEncounterConflictGroups,
   hasWildEncounterConflictSelection,
} from '../wizard/wildEncounterConflictResolution.js';

export function createScheduleTimeConflictResolutionConfirmations(
   strings = APP_STRINGS
) {
   const confirmation = strings.itinerary.confirmation;

   return {
      showProceedWithoutSelection({ onConfirm } = {}) {
         showSaveIssuesProceedConfirmation({
            title: confirmation.proceedWithoutConflictSelectionTitle,
            message: confirmation.proceedWithoutConflictSelectionMessage,
            onConfirm: onConfirm ?? (() => {}),
         });
      },
      showProceedWithUnresolved({ onConfirm } = {}) {
         showSaveIssuesProceedConfirmation({
            title: confirmation.proceedWithUnresolvedConflictsTitle,
            message: confirmation.proceedWithUnresolvedConflictsMessage,
            onConfirm,
         });
      },
      showProceedWithAdditional({ onConfirm } = {}) {
         showSaveIssuesProceedConfirmation({
            title: confirmation.proceedWithAdditionalSelectableActivitiesTitle,
            message: confirmation.proceedWithAdditionalSelectableActivitiesMessage,
            onConfirm,
         });
      },
   };
}

export async function resolveScheduleTimeConflictSelection(
   conflictGroups,
   onResolved,
   confirmations = createScheduleTimeConflictResolutionConfirmations()
) {
   const selectedConflictItems = getSelectedConflictItems(conflictGroups);

   if (!hasWildEncounterConflictSelection(conflictGroups)) {
      confirmations.showProceedWithoutSelection();
      return false;
   }

   if (hasUnresolvedWildEncounterConflictGroups(conflictGroups)) {
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
