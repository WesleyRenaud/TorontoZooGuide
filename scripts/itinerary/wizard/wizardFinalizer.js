import { DraftStorage } from '../draftStorage.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { saveItinerary } from '../itineraryServiceSave.js';
import { ItineraryShape } from '../itineraryShape.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import { SaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { RegionStorage } from '../selectors/regionSelector/regionStorage.js';
import { StorageKeys } from '../storageKeys.js';
import { APP_STRINGS } from '../../strings.js';
import { WizardFinalizeDecisions } from './wizardFinalizeDecisions.js';
import { WizardPopup } from './wizardPopup.js';
import { showWizardSaveIssuesPopup } from './wizardSaveIssuesPopup.js';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: APP_STRINGS.itinerary.noItemsSelected.title,
   message: APP_STRINGS.itinerary.noItemsSelected.message,
   buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
});

function clearWizardMount(mountEl) {
   mountEl?.replaceChildren();
}

function createFinalItineraryDraft(draft = {}, normalizeDraft = ItineraryShape.normalizeItineraryDraft) {
   return normalizeDraft(draft);
}

function showEmptySelectionPopup(mountEl, showWizardPopup = WizardPopup.showItineraryWizardPopup) {
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
      selectedExhibits: RegionStorage.loadSelectedNames(StorageKeys.SELECTED_EXHIBITS_KEY),
   });
}

export async function finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false, deps = {} } = {},
) {
   const {
      normalizeDraft = ItineraryShape.normalizeItineraryDraft,
      saveItineraryFn = saveItinerary,
      syncAnimalDraft = DraftStorage.syncItineraryAnimalDraftFromItinerary,
      showWizardPopup = WizardPopup.showItineraryWizardPopup,
      showNoticePopup = showItineraryNoticePopup,
      showProceedConfirmation = SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation,
      showSaveIssuesPopup = showWizardSaveIssuesPopup,
      shouldBlockEmpty = WizardFinalizeDecisions.shouldBlockEmptyFinish,
      shouldShowSaveIssues = WizardFinalizeDecisions.shouldShowSaveIssuesPopup,
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

   if (ItineraryConfirmationResult.isItineraryConfirmationCancelled(savedItinerary)) {
      return savedItinerary;
   }

   if (!savedItinerary) {
      return ItineraryConfirmationResult.createItineraryConfirmationCancelledResult();
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
