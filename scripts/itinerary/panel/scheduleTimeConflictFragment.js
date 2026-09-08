import { NoticeFragment } from './components/noticeFragment.js';
import { ScheduleTimeConflictResolver } from './scheduleTimeConflictResolver.js';
import { ScheduleTimeConflictView } from './scheduleTimeConflictView.js';
import { Strings } from '../../strings.js';
import { SaveIssuesProceedFragment } from '../wizard/saveIssuesProceedFragment.js';

export class ScheduleTimeConflictFragment {
   static showScheduleTimeConflictConfirmation({
      issues = [],
      onConfirm,
      onCancel,
   } = {}) {
      const {
         content,
         conflictGroups,
      } = ScheduleTimeConflictView.createSaveIssuesContent(issues);

      NoticeFragment.showItineraryNoticePopup({
         title: Strings.itinerary.confirmation.saveIssuesTitle,
         bodyContent: content,
         buttonText: Strings.itinerary.confirmation.saveIssuesButton,
         showCloseButton: true,
         onClose: ({ close } = {}) => {
            SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation({
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
            const resolved = await ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(
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
      return ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(conflictGroups, onResolved);
   }
}
