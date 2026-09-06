import { NoticePopup } from './components/noticePopup.js';
import { ScheduleTimeConflictContent } from './scheduleTimeConflictContent.js';
import { ScheduleTimeConflictResolution } from './scheduleTimeConflictResolution.js';
import { Strings } from '../../strings.js';
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
         title: Strings.itinerary.confirmation.saveIssuesTitle,
         bodyContent: content,
         buttonText: Strings.itinerary.confirmation.saveIssuesButton,
         showCloseButton: true,
         onClose: ({ close } = {}) => {
            SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation({
               title: Strings.itinerary.confirmation.closeSaveIssuesTitle,
               message: Strings.itinerary.confirmation
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
