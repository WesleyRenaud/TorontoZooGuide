import { normalizeItineraryDraft } from '../draftStorage.js';
import { syncItineraryAnimalDraftFromItinerary } from '../draftStorage.js';
import { isItineraryEmpty } from '../itineraryService.js';
import { saveItinerary } from '../itineraryServiceSave.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import {
   confirmSaveIssuesConflictSelection,
   createSaveIssuesContent,
} from '../panel/scheduleTimeConflictConfirmation.js';
import { showSaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { APP_STRINGS } from '../../strings.js';
import { buildItineraryWithSelectedConflictResolutions } from './wildEncounterConflictResolution.js';
import { showItineraryWizardPopup } from './wizardPopup.js';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: APP_STRINGS.itinerary.noItemsSelected.title,
   message: APP_STRINGS.itinerary.noItemsSelected.message,
   buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
});

function clearWizardMount(mountEl) {
   mountEl?.replaceChildren();
}

function createFinalItineraryDraft(draft = {}) {
   return normalizeItineraryDraft(draft);
}

function shouldBlockEmptyFinish(finalItinerary, allowEmpty = false) {
   return !allowEmpty && isItineraryEmpty(finalItinerary);
}

function showEmptySelectionPopup(mountEl) {
   showItineraryWizardPopup({
      mountEl,
      ...EMPTY_SELECTION_POPUP_CONFIG,
   });
}

function showSaveIssuesPopup(savedItinerary) {
   const issues = savedItinerary.saveIssues;

   if (!issues.length) {
      return;
   }

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
            onConfirm: close,
         });
      },
      onConfirm: async ({ close } = {}) => {
         const resolved = await confirmSaveIssuesConflictSelection(
            conflictGroups,
            async (selectedConflictItems) => {
               await saveFinalItinerary(
                  buildItineraryWithSelectedConflictResolutions(
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

function saveFinalItinerary(
   finalItinerary,
   { overridingConflictingGuardiansTalks = false } = {},
) {
   return saveItinerary(finalItinerary, {
      overridingConflictingGuardiansTalks,
   });
}

export async function finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false } = {},
) {
   const finalItinerary = createFinalItineraryDraft(draft);

   if (shouldBlockEmptyFinish(finalItinerary, allowEmpty)) {
      showEmptySelectionPopup(mountEl);
      return null;
   }

   let savedItinerary;

   try {
      savedItinerary = await saveFinalItinerary(finalItinerary);
   }
   catch (error) {
      showItineraryWizardPopup({
         mountEl,
         title: APP_STRINGS.itinerary.errors.generic,
         message: error?.message || APP_STRINGS.itinerary.errors.generic,
         buttonText: APP_STRINGS.itinerary.actions.accept,
      });
      return null;
   }

   syncItineraryAnimalDraftFromItinerary(savedItinerary);

   if (savedItinerary.saveIssues?.length) {
      showSaveIssuesPopup(savedItinerary);
   }

   clearWizardMount(mountEl);

   onDone?.(savedItinerary);

   return savedItinerary;
}
