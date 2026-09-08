import { NoticeFragment } from '../panel/components/noticeFragment.js';
import { ScheduleTimeConflictFragment } from '../panel/scheduleTimeConflictFragment.js';
import { ScheduleTimeConflictView } from '../panel/scheduleTimeConflictView.js';
import { SaveIssuesProceedFragment } from './saveIssuesProceedFragment.js';
import { Strings } from '../../strings.js';
import { WildEncounterConflictResolver } from './wildEncounterConflictResolver.js';

export class WizardSaveIssuesFragment {
   static showWizardSaveIssuesPopup(
      savedItinerary,
      {
      showNoticePopup = NoticeFragment.showItineraryNoticePopup,
      showProceedConfirmation = SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation,
      saveFinalItinerary,
      createSaveIssues = ScheduleTimeConflictView.createSaveIssuesContent,
      confirmSaveIssues = ScheduleTimeConflictFragment.confirmSaveIssuesConflictSelection,
      buildResolvedItinerary = WildEncounterConflictResolver.buildItineraryWithSelectedConflictResolutions,
      } = {}
   ) {
      const issues = savedItinerary.saveIssues;

      if (!issues.length) {
         return;
      }

      const {
         content,
         conflictGroups,
      } = createSaveIssues(issues);

      showNoticePopup({
         title: Strings.itinerary.confirmation.saveIssuesTitle,
         bodyContent: content,
         buttonText: Strings.itinerary.confirmation.saveIssuesButton,
         showCloseButton: true,
         onClose: ({ close } = {}) => {
            showProceedConfirmation({
               title: Strings.itinerary.confirmation.closeSaveIssuesTitle,
               message: Strings.itinerary.confirmation
                  .proceedWithoutConflictSelectionMessage,
               onConfirm: close,
            });
         },
         onConfirm: async ({ close } = {}) => {
            const resolved = await confirmSaveIssues(
               conflictGroups,
               async (selectedConflictItems) => {
                  await saveFinalItinerary(
                     buildResolvedItinerary(
                        savedItinerary,
                        selectedConflictItems
                     ),
                     { overridingConflictingGuardiansTalks: true },
                  );
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
}
