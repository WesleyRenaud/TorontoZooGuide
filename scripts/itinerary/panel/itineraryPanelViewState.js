import { ItineraryPanelViews } from './components/itineraryPanelViews.js';
import { ItineraryPanelViewUrl } from './itineraryPanelViewUrl.js';

let activePanelView = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl();

export class ItineraryPanelViewState {
   static getActiveItineraryPanelView() {
      return activePanelView;
   }

   static setActiveItineraryPanelView(view) {
      activePanelView = view;
      ItineraryPanelViewUrl.setItineraryPanelViewInUrl(view);
   }

   static makeItineraryPanelViewShell() {
      return ItineraryPanelViews.makeItineraryPanelViews({
         activeView: activePanelView,
         onViewChange: ItineraryPanelViewState.setActiveItineraryPanelView,
      });
   }

   static resetActiveItineraryPanelView(
      view = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl()
   ) {
      activePanelView = view;
   }
}
