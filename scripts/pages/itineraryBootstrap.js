import { ItineraryPanelFragment } from '../itinerary/panel/components/itineraryPanelFragment.js';
import { WheelBlocker } from '../itinerary/wizard/wheelBlocker.js';
import { ItineraryPageBootstrap } from './itineraryPageBootstrap.js';
import { SpeciesFragment } from '../overlays/speciesFragment.js';

export class ItineraryBootstrap {
   static initItineraryPage() {
      const mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl();
      if (!mountEl) return;

      SpeciesFragment.initSpeciesOverlay();

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
