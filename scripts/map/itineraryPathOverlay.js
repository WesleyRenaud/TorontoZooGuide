import { ItineraryPathOverlayRenderer } from './itineraryPathOverlayRenderer.js';

export class ItineraryPathOverlay {
   static clearItineraryPathOverlay() {
      ItineraryPathOverlayRenderer.removeItineraryPathLayer(ItineraryPathOverlayRenderer.getSvgRoot());
   }

   static renderItineraryPathOverlay(itineraryPath) {
      const svgRoot = ItineraryPathOverlayRenderer.getSvgRoot();

      ItineraryPathOverlay.clearItineraryPathOverlay();

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
