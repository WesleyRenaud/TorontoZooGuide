import { NoticePopup } from '../panel/components/noticePopup.js';
import {
   createSaveIssuesContent,
   ScheduleTimeConflictConfirmation,
} from '../panel/scheduleTimeConflictConfirmation.js';
import { SaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { Strings } from '../../strings.js';
import { WildEncounterConflictResolution } from './wildEncounterConflictResolution.js';

export class WizardSaveIssuesPopup {
   static showWizardSaveIssuesPopup(
      savedItinerary,
      {
      showNoticePopup = NoticePopup.showItineraryNoticePopup,
      showProceedConfirmation = SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation,
      saveFinalItinerary,
      createSaveIssues = createSaveIssuesContent,
      confirmSaveIssues = ScheduleTimeConflictConfirmation.confirmSaveIssuesConflictSelection,
      buildResolvedItinerary = WildEncounterConflictResolution.buildItineraryWithSelectedConflictResolutions,
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
