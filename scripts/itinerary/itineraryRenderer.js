import { RenderView } from './panel/renderView.js';

export class ItineraryRenderer {
   static getItineraryPanelBody() {
      return document.querySelector('.itinerary-panel .side-panel-body');
   }

   static renderItineraryPanel(bodyEl = ItineraryRenderer.getItineraryPanelBody()) {
      return RenderView.renderItineraryPanelInto(bodyEl);
   }
}
