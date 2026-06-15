import { makeItineraryPanelViews } from './components/dayPlanner.js';
import {
   getItineraryPanelViewFromUrl,
   setItineraryPanelViewInUrl,
} from './itineraryPanelViewUrl.js';

let activePanelView = getItineraryPanelViewFromUrl();

export function getActiveItineraryPanelView() {
   return activePanelView;
}

export function setActiveItineraryPanelView(view) {
   activePanelView = view;
   setItineraryPanelViewInUrl(view);
}

export function makeItineraryPanelViewShell() {
   return makeItineraryPanelViews({
      activeView: activePanelView,
      onViewChange: setActiveItineraryPanelView,
   });
}

export function resetActiveItineraryPanelView(
   view = getItineraryPanelViewFromUrl()
) {
   activePanelView = view;
}
