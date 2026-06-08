import { initItineraryMap } from '../itinerary/itineraryMapController.js';
import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import {
   getItinerary,
   isItineraryEmpty,
} from '../itinerary/itineraryService.js';
import { isValidatedItineraryEmpty } from '../itinerary/wizard/itineraryDiff.js';
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

function createWizardOpener(mountEl, onDone) {
   return ({ startAt = null } = {}) => {
      openItineraryWizard({
         mountEl,
         startAt,
         onDone,
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
         isEmptyItinerary: isValidatedItineraryEmpty(itinerary),
      },
      onViewAlternatives: (step) => openWizard({ startAt: step }),
   });
}

async function refreshItineraryPageContent(
   mountEl,
   openWizard,
   { openBuilderWhenEmpty = false, itinerary: providedItinerary = null } = {}
) {
   await renderItineraryPanel();

   const itinerary = providedItinerary ?? await getItinerary();

   if (!itinerary || isItineraryEmpty(itinerary)) {
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
   await initEmbeddedItineraryMap();
   await refreshPanel({ openBuilderWhenEmpty: true });
}

export function initItineraryPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

   initSpeciesOverlay();

   const refreshPanel = (options) => refreshItineraryPageContent(
      mountEl,
      openWizard,
      options
   );
   const openWizard = createWizardOpener(mountEl, refreshPanel);

   blockMapWheelWhileWizardOpen(mountEl);
   bindWizardEvents(openWizard);
   bindPanelRefreshEvents(refreshPanel);

   void initItineraryPageContent(mountEl, openWizard, refreshPanel);
}
