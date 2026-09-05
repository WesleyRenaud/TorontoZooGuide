import { NoticePopup } from './components/noticePopup.js';
import { ScheduleTimeConflictContent } from './scheduleTimeConflictContent.js';
import { ScheduleTimeConflictResolution } from './scheduleTimeConflictResolution.js';
import { APP_STRINGS } from '../../strings.js';
import { SaveIssuesProceedConfirmation } from '../wizard/saveIssuesProceedConfirmation.js';

export const WILD_ENCOUNTER_TIME_CONFLICT = ScheduleTimeConflictContent.WILD_ENCOUNTER_TIME_CONFLICT;
export const createSaveIssuesContent = ScheduleTimeConflictContent.createSaveIssuesContent;

export class ScheduleTimeConflictConfirmation {
   static showScheduleTimeConflictConfirmation({
      issues = [],
      onConfirm,
      onCancel,
   } = {}) {
      const {
         content,
         conflictGroups,
      } = ScheduleTimeConflictContent.createSaveIssuesContent(issues);

      NoticePopup.showItineraryNoticePopup({
         title: APP_STRINGS.itinerary.confirmation.saveIssuesTitle,
         bodyContent: content,
         buttonText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
         showCloseButton: true,
         onClose: ({ close } = {}) => {
            SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation({
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
            const resolved = await ScheduleTimeConflictResolution.resolveScheduleTimeConflictSelection(
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

   static async confirmSaveIssuesConflictSelection(conflictGroups, onResolved) {
      return ScheduleTimeConflictResolution.resolveScheduleTimeConflictSelection(conflictGroups, onResolved);
   }
}
