import { initItineraryMap } from '../itinerary/itineraryMapController.js';
import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import { getItinerary } from '../itinerary/itineraryService.js';
import { hasSavedItineraryContent } from '../itinerary/itineraryShape.js';
import { getItineraryOverlayMountEl } from '../itinerary/panel/components/popup.js';
import { offerPastItineraryClearOrRecovery } from '../itinerary/pastItinerary/offerPastItineraryClearOrRecovery.js';
import { Summary } from '../itinerary/wizard/diff/summary.js';
import { showWizardValidationPopupIfNeeded } from '../itinerary/wizard/validationPopup.js';
import { blockMapWheelWhileWizardOpen } from '../itinerary/wizard/wheelBlocker.js';
import { openItineraryWizard } from '../itinerary/wizard/wizardController.js';
import { loadInlineZooMap } from '../map/loadInlineZooMap.js';
import { initSpeciesOverlay } from '../overlays/speciesOverlay.js';

const DEFAULT_WIZARD_STEP = 'date';
let lastShownValidationSignature = null;

function hasEmbeddedMap() {
   return Boolean(document.getElementById('mapInner'));
}

function createWizardOpener(mountEl) {
   return ({ startAt = null } = {}) => {
      openItineraryWizard({
         mountEl,
         startAt,
      });
   };
}

function showItineraryValidationDiff(mountEl, itinerary, openWizard) {
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

   if (validationSignature === lastShownValidationSignature) {
      return;
   }

   lastShownValidationSignature = validationSignature;

   showWizardValidationPopupIfNeeded({
      mountEl,
      pendingValidation: {
         added: itinerary.validation.added,
         removed: itinerary.validation.removed,
         unscheduled: itinerary.validation.unscheduled,
         reducedVisibility: itinerary.validation.reducedVisibility,
         improvedVisibility: itinerary.validation.improvedVisibility,
         adjustments: itinerary.validation.adjustments,
         isEmptyItinerary: Summary.isValidatedItineraryEmpty(itinerary),
      },
      onViewAlternatives: (step) => openWizard({ startAt: step }),
   });
}

async function refreshItineraryPageContent(
   mountEl,
   openWizard,
   { openBuilderWhenEmpty = false, itinerary: providedItinerary = null, skipStaleCheck = false } = {}
) {
   const itinerary = providedItinerary ?? await getItinerary();

   if (!skipStaleCheck) {
      const pastDatePromptShown = await offerPastItineraryClearOrRecovery({
         mountEl,
         itinerary,
         onCleared: () => {
            void refreshItineraryPageContent(mountEl, openWizard, {
               openBuilderWhenEmpty: true,
               skipStaleCheck: true,
            });
         },
         onRecovered: (savedItinerary) => {
            void refreshItineraryPageContent(mountEl, openWizard, {
               itinerary: savedItinerary,
               skipStaleCheck: true,
            });
         },
      });

      if (pastDatePromptShown) {
         await renderItineraryPanel();
         return;
      }
   }

   await renderItineraryPanel();

   if (!itinerary || !hasSavedItineraryContent(itinerary)) {
      if (openBuilderWhenEmpty) {
         openWizard();
      }

      return;
   }

   showItineraryValidationDiff(mountEl, itinerary, openWizard);
}

function bindWizardEvents(openWizard) {
   window.addEventListener('tzg:editItinerarySection', (event) => {
      openWizard({
         startAt: event?.detail?.step || DEFAULT_WIZARD_STEP,
      });
   });

   window.addEventListener('tzg:editItinerary', () => {
      openWizard();
   });

   window.addEventListener('tzg:buildItinerary', () => {
      openWizard();
   });
}

function bindPanelRefreshEvents(refreshPanel) {
   window.addEventListener('tzg:itineraryUpdated', (event) => {
      void refreshPanel({
         itinerary: event?.detail?.itinerary ?? null,
      });
   });
}

async function initEmbeddedItineraryMap() {
   if (!hasEmbeddedMap()) {
      return;
   }

   try {
      await loadInlineZooMap();
      initItineraryMap();
   } catch (err) {
      console.warn('initItineraryMap() failed:', err);
   }
}

async function initItineraryPageContent(mountEl, openWizard, refreshPanel) {
   await refreshPanel({ openBuilderWhenEmpty: true });
   await initEmbeddedItineraryMap();
}

export function initItineraryPage() {
   const mountEl = getItineraryOverlayMountEl();
   if (!mountEl) return;

   initSpeciesOverlay();

   const refreshPanel = (options) => refreshItineraryPageContent(
      mountEl,
      openWizard,
      options
   );
   const openWizard = createWizardOpener(mountEl);

   blockMapWheelWhileWizardOpen(mountEl);
   bindWizardEvents(openWizard);
   bindPanelRefreshEvents(refreshPanel);

   void initItineraryPageContent(mountEl, openWizard, refreshPanel);
}
