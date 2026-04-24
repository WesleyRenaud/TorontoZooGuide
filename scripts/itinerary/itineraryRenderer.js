import { renderItineraryPanelInto } from './panel/renderPanel.js';

export function getItineraryPanelBody() {
   return document.querySelector('.itinerary-panel .side-panel-body');
}

export function renderItineraryPanel(bodyEl = getItineraryPanelBody()) {
   return renderItineraryPanelInto(bodyEl);
}
