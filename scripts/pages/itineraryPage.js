import { ItineraryPanelPopup } from '../itinerary/panel/components/itineraryPanelPopup.js';
import { WheelBlocker } from '../itinerary/wizard/wheelBlocker.js';
import { ItineraryPageBootstrap } from './itineraryPageBootstrap.js';
import { SpeciesOverlay } from '../overlays/speciesOverlay.js';

export class ItineraryPage {
   static initItineraryPage() {
      const mountEl = ItineraryPanelPopup.getItineraryOverlayMountEl();
      if (!mountEl) return;

      SpeciesOverlay.initSpeciesOverlay();

      const refreshPanel = (options) => ItineraryPageBootstrap.refreshItineraryPageContent(
         mountEl,
         openWizard,
         options
      );
      const openWizard = ItineraryPageBootstrap.createWizardOpener(mountEl);

      WheelBlocker.blockMapWheelWhileWizardOpen(mountEl);
      ItineraryPageBootstrap.bindWizardEvents(openWizard);
      ItineraryPageBootstrap.bindPanelRefreshEvents(refreshPanel);

      void ItineraryPageBootstrap.initItineraryPageContent(mountEl, openWizard, refreshPanel);
   }
}
