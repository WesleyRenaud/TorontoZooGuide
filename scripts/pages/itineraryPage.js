import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import { loadInlineZooMap } from '../map/loadInlineZooMap.js';
import { initItineraryMap } from '../itinerary/itineraryMapController.js';

import { blockMapWheelWhileWizardOpen } from '../itinerary/wizard/wheelBlocker.js';
import { openItineraryWizard } from '../itinerary/wizard/wizardController.js';
import { getItinerary, isItineraryEmpty } from '../itinerary/itineraryService.js';

export function initItineraryPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

   window.addEventListener('tzg:editItinerarySection', (e) => {
      const step = e?.detail?.step || 'date';

      openItineraryWizard({
         mountEl,
         startAt: step,
         onDone: () => renderItineraryPanel(),
      });
   });

   blockMapWheelWhileWizardOpen(mountEl);

   window.addEventListener('tzg:editItinerary', () => {
      openItineraryWizard({
         mountEl,
         onDone: () => renderItineraryPanel(),
      });
   });

   window.addEventListener('tzg:buildItinerary', () => {
      openItineraryWizard({
         mountEl,
         onDone: () => renderItineraryPanel(),
      });
   });

   window.addEventListener('tzg:itineraryUpdated', () => {
      renderItineraryPanel();
   });

   (async () => {
      if (document.getElementById('mapInner')) {
         try {
            await loadInlineZooMap();
            initItineraryMap();
         } catch (err) {
            console.warn('initItineraryMap() failed:', err);
         }
      }

      await renderItineraryPanel();

      const itin = await getItinerary();
      const shouldAutoOpen = !itin || isItineraryEmpty(itin);

      if (shouldAutoOpen) {
         openItineraryWizard({
            mountEl,
            onDone: () => renderItineraryPanel(),
         });
      }
   })();
}
