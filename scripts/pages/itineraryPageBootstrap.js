import { ItineraryMapController } from '../itinerary/itineraryMapController.js';
import { ItineraryRenderer } from '../itinerary/itineraryRenderer.js';
import { ItineraryService } from '../itinerary/itineraryService.js';
import { ItineraryShape } from '../itinerary/itineraryShape.js';
import { OfferPastItineraryClearOrRecoverer } from '../itinerary/pastItinerary/offerPastItineraryClearOrRecoverer.js';
import { WizardDiffPresenter } from '../itinerary/wizard/diff/wizardDiffPresenter.js';
import { ValidationFragment } from '../itinerary/wizard/validationFragment.js';
import { WizardController } from '../itinerary/wizard/wizardController.js';
import { WizardStepConfigs } from '../itinerary/wizard/wizardStepConfigs.js';
import { LoadInlineZooMapLoader } from '../map/loadInlineZooMapLoader.js';

export class ItineraryPageBootstrap {
   static lastShownValidationSignature = null;

   static hasEmbeddedMap() {
      return Boolean(document.getElementById('mapInner'));
   }

   static createWizardOpener(mountEl) {
      return ({ startAt = null } = {}) => {
         WizardController.openItineraryWizard({
            mountEl,
            startAt,
         });
      };
   }

   static showItineraryValidationDiff(mountEl, itinerary, openWizard) {
      if (!itinerary?.validation?.hasChanges) {
         return;
      }

      const validationSignature = JSON.stringify({
         date: itinerary.date,
         added: itinerary.validation.added,
         removed: itinerary.validation.removed,
         unscheduled: itinerary.validation.unscheduled,
         reducedVisibility: itinerary.validation.reducedVisibility,
         improvedVisibility: itinerary.validation.improvedVisibility,
         adjustments: itinerary.validation.adjustments,
      });

      if (validationSignature === ItineraryPageBootstrap.lastShownValidationSignature) {
         return;
      }

      ItineraryPageBootstrap.lastShownValidationSignature = validationSignature;

      ValidationFragment.showWizardValidationPopupIfNeeded({
         mountEl,
         pendingValidation: {
            added: itinerary.validation.added,
            removed: itinerary.validation.removed,
            unscheduled: itinerary.validation.unscheduled,
            reducedVisibility: itinerary.validation.reducedVisibility,
            improvedVisibility: itinerary.validation.improvedVisibility,
            adjustments: itinerary.validation.adjustments,
            isEmptyItinerary: WizardDiffPresenter.isValidatedItineraryEmpty(itinerary),
         },
         onViewAlternatives: (step) => openWizard({ startAt: step }),
      });
   }

   static async refreshItineraryPageContent(
      mountEl,
      openWizard,
      { openBuilderWhenEmpty = false, itinerary: providedItinerary = null, skipStaleCheck = false } = {}
   ) {
      const itinerary = providedItinerary ?? await ItineraryService.getItinerary();

      if (!skipStaleCheck) {
         const pastDatePromptShown = await OfferPastItineraryClearOrRecoverer.offerPastItineraryClearOrRecovery({
            mountEl,
            itinerary,
            onCleared: () => {
               void ItineraryPageBootstrap.refreshItineraryPageContent(mountEl, openWizard, {
                  skipStaleCheck: true,
               });
            },
            onRecovered: (savedItinerary) => {
               void ItineraryPageBootstrap.refreshItineraryPageContent(mountEl, openWizard, {
                  itinerary: savedItinerary,
                  skipStaleCheck: true,
               });
            },
         });

         if (pastDatePromptShown) {
            await ItineraryRenderer.renderItineraryPanel();
            return;
         }
      }

      await ItineraryRenderer.renderItineraryPanel();

      if (!itinerary || !ItineraryShape.hasSavedItineraryContent(itinerary)) {
         if (openBuilderWhenEmpty) {
            openWizard();
         }

         return;
      }

      ItineraryPageBootstrap.showItineraryValidationDiff(mountEl, itinerary, openWizard);
   }

   static bindWizardEvents(openWizard) {
      window.addEventListener('tzg:editItinerarySection', (event) => {
         openWizard({
            startAt: event?.detail?.step || WizardStepConfigs.WIZARD_DEFAULT_START_STEP,
         });
      });

      window.addEventListener('tzg:editItinerary', () => {
         openWizard();
      });

      window.addEventListener('tzg:buildItinerary', () => {
         openWizard();
      });
   }

   static bindPanelRefreshEvents(refreshPanel) {
      window.addEventListener('tzg:itineraryUpdated', (event) => {
         void refreshPanel({
            itinerary: event?.detail?.itinerary ?? null,
         });
      });
   }

   static async initEmbeddedItineraryMap() {
      if (!ItineraryPageBootstrap.hasEmbeddedMap()) {
         return;
      }

      try {
         await LoadInlineZooMapLoader.loadInlineZooMap();
         ItineraryMapController.initItineraryMap();
      } catch (err) {
         console.warn('ItineraryMapController.initItineraryMap() failed:', err);
      }
   }

   static async initItineraryPageContent(mountEl, openWizard, refreshPanel) {
      await refreshPanel({ openBuilderWhenEmpty: true });
      await ItineraryPageBootstrap.initEmbeddedItineraryMap();
   }
}
