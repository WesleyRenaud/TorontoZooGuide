import { normalizeItineraryDraft } from '../draftStorage.js';
import { syncItineraryAnimalDraftFromItinerary } from '../draftStorage.js';
import { saveItinerary } from '../itineraryServiceSave.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import {
   confirmSaveIssuesConflictSelection,
   createSaveIssuesContent,
} from '../panel/scheduleTimeConflictConfirmation.js';
import { showSaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { APP_STRINGS } from '../../strings.js';
import { buildItineraryWithSelectedConflictResolutions } from './wildEncounterConflictResolution.js';
import {
   shouldBlockEmptyFinish,
   shouldShowSaveIssuesPopup,
} from './wizardFinalizeDecisions.js';
import { showItineraryWizardPopup } from './wizardPopup.js';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: APP_STRINGS.itinerary.noItemsSelected.title,
   message: APP_STRINGS.itinerary.noItemsSelected.message,
   buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
});

function clearWizardMount(mountEl) {
   mountEl?.replaceChildren();
}

function createFinalItineraryDraft(draft = {}, normalizeDraft = normalizeItineraryDraft) {
   return normalizeDraft(draft);
}

function showEmptySelectionPopup(mountEl, showWizardPopup = showItineraryWizardPopup) {
   showWizardPopup({
      mountEl,
      ...EMPTY_SELECTION_POPUP_CONFIG,
   });
}

function showSaveIssuesPopup(
   savedItinerary,
   {
      showNoticePopup = showItineraryNoticePopup,
      showProceedConfirmation = showSaveIssuesProceedConfirmation,
      saveFinalItinerary,
   } = {}
) {
   const issues = savedItinerary.saveIssues;

   if (!issues.length) {
      return;
   }

   const {
      content,
      conflictGroups,
   } = createSaveIssuesContent(issues);

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
   saveItineraryFn = saveItinerary,
) {
   return saveItineraryFn(finalItinerary, {
      overridingConflictingGuardiansTalks,
   });
}

export async function finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false, deps = {} } = {},
) {
   const {
      normalizeDraft = normalizeItineraryDraft,
      saveItineraryFn = saveItinerary,
      syncAnimalDraft = syncItineraryAnimalDraftFromItinerary,
      showWizardPopup = showItineraryWizardPopup,
      showNoticePopup = showItineraryNoticePopup,
      showProceedConfirmation = showSaveIssuesProceedConfirmation,
      shouldBlockEmpty = shouldBlockEmptyFinish,
      shouldShowSaveIssues = shouldShowSaveIssuesPopup,
   } = deps;

   const finalItinerary = createFinalItineraryDraft(draft, normalizeDraft);

   if (shouldBlockEmpty(finalItinerary, allowEmpty)) {
      showEmptySelectionPopup(mountEl, showWizardPopup);
      return null;
   }

   let savedItinerary;

   try {
      savedItinerary = await saveFinalItinerary(
         finalItinerary,
         {},
         saveItineraryFn,
      );
   }
   catch (error) {
      showWizardPopup({
         mountEl,
         title: APP_STRINGS.itinerary.errors.generic,
         message: error?.message || APP_STRINGS.itinerary.errors.generic,
         buttonText: APP_STRINGS.itinerary.actions.accept,
      });
      return null;
   }

   syncAnimalDraft(savedItinerary);

   if (shouldShowSaveIssues(savedItinerary)) {
      showSaveIssuesPopup(savedItinerary, {
         showNoticePopup,
         showProceedConfirmation,
         saveFinalItinerary: (itinerary, options) => saveFinalItinerary(
            itinerary,
            options,
            saveItineraryFn,
         ),
      });
   }

   clearWizardMount(mountEl);

   onDone?.(savedItinerary);

   return savedItinerary;
}
