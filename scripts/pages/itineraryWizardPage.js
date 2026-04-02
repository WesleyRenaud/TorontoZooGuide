import { renderItineraryPanel } from '../itinerary/itineraryRenderer.js';
import { loadInlineZooMap } from './loadInlineZooMap.js';
import { initItineraryPage } from './itineraryPage.js';

import { blockMapWheelWhileWizardOpen } from './itineraryWizard/wheelBlocker.js';
import { openItineraryBuilder } from './itineraryWizard/builder.js';
import { getItinerary, isItineraryEmpty } from './itineraryWizard/itineraryApi.js';

export function initItineraryWizardPage() {
   const mountEl = document.getElementById('itineraryFlow');
   if (!mountEl) return;

   window.addEventListener('tzg:editItinerarySection', (e) => {
      const step = e?.detail?.step || 'date';

      openItineraryBuilder({
         mountEl,
         startAt: step,
         onDone: () => renderItineraryPanel(),
      });
   });

   blockMapWheelWhileWizardOpen(mountEl);

   window.addEventListener('tzg:editItinerary', () => {
      openItineraryBuilder({
         mountEl,
         onDone: () => renderItineraryPanel(),
      });
   });

   window.addEventListener('tzg:buildItinerary', () => {
      openItineraryBuilder({
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
            initItineraryPage();
         } catch (err) {
            console.warn('initItineraryPage() failed:', err);
         }
      }

      await renderItineraryPanel();

      const itin = await getItinerary();
      const shouldAutoOpen = !itin || isItineraryEmpty(itin);

      if (shouldAutoOpen) {
         openItineraryBuilder({
            mountEl,
            onDone: () => renderItineraryPanel(),
         });
      }
   })();
}