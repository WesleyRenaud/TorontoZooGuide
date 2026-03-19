import { renderItineraryPanelInto } from './panel/renderPanel.js';

export function renderItineraryPanel() {
   const body = document.getElementById('itineraryPanelBody');
   renderItineraryPanelInto(body);
}