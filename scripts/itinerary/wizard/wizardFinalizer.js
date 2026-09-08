import { DraftStore } from '../draftStore.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ItineraryServiceSaver } from '../itineraryServiceSaver.js';
import { ItineraryShape } from '../itineraryShape.js';
import { NoticeFragment } from '../panel/components/noticeFragment.js';
import { SaveIssuesProceedFragment } from './saveIssuesProceedFragment.js';
import { Strings } from '../../strings.js';
import { WizardFinalizePresenter } from './wizardFinalizePresenter.js';
import { WizardFinalizerHelper } from './wizardFinalizerHelper.js';
import { WizardFragment } from './wizardFragment.js';
import { WizardSaveIssuesFragment } from './wizardSaveIssuesFragment.js';

export class WizardFinalizer {
   static async finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false, deps = {} } = {},
) {
      const {
         normalizeDraft = ItineraryShape.normalizeItineraryDraft,
         saveItineraryFn = ItineraryServiceSaver.saveItinerary,
         syncAnimalDraft = DraftStore.syncItineraryAnimalDraftFromItinerary,
         showWizardPopup = WizardFragment.showItineraryWizardPopup,
         showNoticePopup = NoticeFragment.showItineraryNoticePopup,
         showProceedConfirmation = SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation,
         showSaveIssuesPopup = WizardSaveIssuesFragment.showWizardSaveIssuesPopup,
         shouldBlockEmpty = WizardFinalizePresenter.shouldBlockEmptyFinish,
         shouldShowSaveIssues = WizardFinalizePresenter.shouldShowSaveIssuesPopup,
      } = deps;

      const finalItinerary = WizardFinalizerHelper.createFinalItineraryDraft(draft, normalizeDraft);

      if (shouldBlockEmpty(finalItinerary, allowEmpty)) {
         WizardFinalizerHelper.showEmptySelectionPopup(mountEl, showWizardPopup);
         return null;
      }

      let savedItinerary;

      try {
         savedItinerary = await WizardFinalizerHelper.saveFinalItinerary(
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
            saveFinalItinerary: (itinerary, options) => WizardFinalizerHelper.saveFinalItinerary(
               itinerary,
               options,
               saveItineraryFn,
            ),
         });
      }

      WizardFinalizerHelper.clearWizardMount(mountEl);

      onDone?.(savedItinerary);

      return savedItinerary;
   }
}
