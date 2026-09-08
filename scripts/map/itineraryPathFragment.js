import { ItineraryPathOverlayRenderer } from './itineraryPathOverlayRenderer.js';

export class ItineraryPathFragment {
   static clearItineraryPathOverlay() {
      ItineraryPathOverlayRenderer.removeItineraryPathLayer(ItineraryPathOverlayRenderer.getSvgRoot());
   }

   static renderItineraryPathOverlay(itineraryPath) {
      const svgRoot = ItineraryPathOverlayRenderer.getSvgRoot();

      ItineraryPathFragment.clearItineraryPathOverlay();

      if (!svgRoot) {
         return;
      }

      const pathD = ItineraryPathOverlayRenderer.buildPathD(itineraryPath);

      if (!pathD) {
         return;
      }

      svgRoot.appendChild(ItineraryPathOverlayRenderer.createPathLayer(pathD));
   }
}
