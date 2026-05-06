import { initItineraryMap } from '../itinerary/itineraryMapController.js';
import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import {
   getItinerary,
   isItineraryEmpty,
} from '../itinerary/itineraryService.js';
import { blockMapWheelWhileWizardOpen } from '../itinerary/wizard/wheelBlocker.js';
import { openItineraryWizard } from '../itinerary/wizard/wizardController.js';
import { loadInlineZooMap } from '../map/loadInlineZooMap.js';

const DEFAULT_WIZARD_STEP = 'date';

function hasEmbeddedMap() {
   return Boolean(document.getElementById('mapInner'));
}

function createPanelRefresh() {
   return () => renderItineraryPanel();
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
   window.addEventListener('tzg:itineraryUpdated', () => {
      refreshPanel();
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

async function shouldOpenWizardOnLoad() {
   const itinerary = await getItinerary();
   return !itinerary || isItineraryEmpty(itinerary);
}

async function initItineraryPageContent(openWizard, refreshPanel) {
   await initEmbeddedItineraryMap();
   await refreshPanel();

   if (await shouldOpenWizardOnLoad()) {
      openWizard();
   }
}

export function initItineraryPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

   const refreshPanel = createPanelRefresh();
   const openWizard = createWizardOpener(mountEl, refreshPanel);

   blockMapWheelWhileWizardOpen(mountEl);
   bindWizardEvents(openWizard);
   bindPanelRefreshEvents(refreshPanel);

   void initItineraryPageContent(openWizard, refreshPanel);
}
