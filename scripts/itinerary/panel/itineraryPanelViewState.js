import { makeItineraryPanelViews } from './components/dayPlanner.js';
import { ItineraryPanelViewUrl } from './itineraryPanelViewUrl.js';

let activePanelView = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl();

export function getActiveItineraryPanelView() {
   return activePanelView;
}

export function setActiveItineraryPanelView(view) {
   activePanelView = view;
   ItineraryPanelViewUrl.setItineraryPanelViewInUrl(view);
}

export function makeItineraryPanelViewShell() {
   return makeItineraryPanelViews({
      activeView: activePanelView,
      onViewChange: setActiveItineraryPanelView,
   });
}

export function resetActiveItineraryPanelView(
   view = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl()
) {
   activePanelView = view;
}
