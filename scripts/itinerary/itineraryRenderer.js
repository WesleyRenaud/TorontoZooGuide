import { renderItineraryPanelInto } from './panel/renderPanel.js';

export function renderItineraryPanel() {
   const body = document.querySelector('.itinerary-panel .side-panel-body');
   renderItineraryPanelInto(body);
}