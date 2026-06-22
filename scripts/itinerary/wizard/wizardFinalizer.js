import { normalizeItineraryDraft } from '../draftStorage.js';
import { syncItineraryAnimalDraftFromItinerary } from '../draftStorage.js';
import { saveItinerary } from '../itineraryServiceSave.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import { showSaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { APP_STRINGS } from '../../strings.js';
import {
   shouldBlockEmptyFinish,
   shouldShowSaveIssuesPopup,
} from './wizardFinalizeDecisions.js';
import { showItineraryWizardPopup } from './wizardPopup.js';
import { showWizardSaveIssuesPopup } from './wizardSaveIssuesPopup.js';

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
      showSaveIssuesPopup = showWizardSaveIssuesPopup,
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

   if (!savedItinerary) {
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
