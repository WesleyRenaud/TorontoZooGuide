import { showItineraryNoticePopup } from './components/noticePopup.js';
import { createSaveIssuesContent } from './scheduleTimeConflictContent.js';
import { resolveScheduleTimeConflictSelection } from './scheduleTimeConflictResolution.js';
import { APP_STRINGS } from '../../strings.js';
import { showSaveIssuesProceedConfirmation } from '../wizard/saveIssuesProceedConfirmation.js';

export { createSaveIssuesContent } from './scheduleTimeConflictContent.js';
export { WILD_ENCOUNTER_TIME_CONFLICT } from './scheduleTimeConflictContent.js';

export function showScheduleTimeConflictConfirmation({
   issues = [],
   onConfirm,
   onCancel,
} = {}) {
   const {
      content,
      conflictGroups,
   } = createSaveIssuesContent(issues);

   showItineraryNoticePopup({
      title: APP_STRINGS.itinerary.confirmation.saveIssuesTitle,
      bodyContent: content,
      buttonText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
      showCloseButton: true,
      onClose: ({ close } = {}) => {
         showSaveIssuesProceedConfirmation({
            title: APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle,
            message: APP_STRINGS.itinerary.confirmation
               .proceedWithoutConflictSelectionMessage,
            onConfirm: () => {
               onCancel?.();
               close();
            },
         });
      },
      onConfirm: async ({ close } = {}) => {
         const resolved = await resolveScheduleTimeConflictSelection(
            conflictGroups,
            async (selectedConflictItems) => {
               await onConfirm?.(selectedConflictItems);
               close();
            }
         );

         if (!resolved) {
            return false;
         }

         return true;
      },
   });
}

export async function confirmSaveIssuesConflictSelection(conflictGroups, onResolved) {
   return resolveScheduleTimeConflictSelection(conflictGroups, onResolved);
}
