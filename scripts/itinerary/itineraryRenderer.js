import { RenderPanel } from './panel/renderPanel.js';

export class ItineraryRenderer {
   static getItineraryPanelBody() {
      return document.querySelector('.itinerary-panel .side-panel-body');
   }

   static renderItineraryPanel(bodyEl = ItineraryRenderer.getItineraryPanelBody()) {
      return RenderPanel.renderItineraryPanelInto(bodyEl);
   }
}
