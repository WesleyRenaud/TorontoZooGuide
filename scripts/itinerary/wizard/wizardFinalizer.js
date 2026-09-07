import { DraftStorage } from '../draftStorage.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ItineraryServiceSave } from '../itineraryServiceSave.js';
import { ItineraryShape } from '../itineraryShape.js';
import { NoticePopup } from '../panel/components/noticePopup.js';
import { SaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import { Strings } from '../../strings.js';
import { WizardFinalizeDecisions } from './wizardFinalizeDecisions.js';
import { WizardFinalizerHelpers } from './wizardFinalizerHelpers.js';
import { WizardPopup } from './wizardPopup.js';
import { WizardSaveIssuesPopup } from './wizardSaveIssuesPopup.js';

export class WizardFinalizer {
   static async finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false, deps = {} } = {},
) {
      const {
         normalizeDraft = ItineraryShape.normalizeItineraryDraft,
         saveItineraryFn = ItineraryServiceSave.saveItinerary,
         syncAnimalDraft = DraftStorage.syncItineraryAnimalDraftFromItinerary,
         showWizardPopup = WizardPopup.showItineraryWizardPopup,
         showNoticePopup = NoticePopup.showItineraryNoticePopup,
         showProceedConfirmation = SaveIssuesProceedConfirmation.showSaveIssuesProceedConfirmation,
         showSaveIssuesPopup = WizardSaveIssuesPopup.showWizardSaveIssuesPopup,
         shouldBlockEmpty = WizardFinalizeDecisions.shouldBlockEmptyFinish,
         shouldShowSaveIssues = WizardFinalizeDecisions.shouldShowSaveIssuesPopup,
      } = deps;

      const finalItinerary = WizardFinalizerHelpers.createFinalItineraryDraft(draft, normalizeDraft);

      if (shouldBlockEmpty(finalItinerary, allowEmpty)) {
         WizardFinalizerHelpers.showEmptySelectionPopup(mountEl, showWizardPopup);
         return null;
      }

      let savedItinerary;

      try {
         savedItinerary = await WizardFinalizerHelpers.saveFinalItinerary(
            finalItinerary,
            {},
            saveItineraryFn,
         );
      }
      catch (error) {
         showWizardPopup({
            mountEl,
            title: Strings.itinerary.errors.generic,
            message: error?.message || Strings.itinerary.errors.generic,
            buttonText: Strings.itinerary.actions.accept,
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
            saveFinalItinerary: (itinerary, options) => WizardFinalizerHelpers.saveFinalItinerary(
               itinerary,
               options,
               saveItineraryFn,
            ),
         });
      }

      WizardFinalizerHelpers.clearWizardMount(mountEl);

      onDone?.(savedItinerary);

      return savedItinerary;
   }
}
