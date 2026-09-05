import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import {
   confirmSaveIssuesConflictSelection,
   createSaveIssuesContent,
} from '../panel/scheduleTimeConflictConfirmation.js';
import { SaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { APP_STRINGS } from '../../strings.js';
import { WildEncounterConflictResolution } from './wildEncounterConflictResolution.js';

export function showWizardSaveIssuesPopup(
   savedItinerary,
   {
      showNoticePopup = showItineraryNoticePopup,
      showProceedConfirmation = SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation,
      saveFinalItinerary,
      createSaveIssues = createSaveIssuesContent,
      confirmSaveIssues = confirmSaveIssuesConflictSelection,
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
      title: APP_STRINGS.itinerary.confirmation.saveIssuesTitle,
      bodyContent: content,
      buttonText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
      showCloseButton: true,
      onClose: ({ close } = {}) => {
         showProceedConfirmation({
            title: APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle,
            message: APP_STRINGS.itinerary.confirmation
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
