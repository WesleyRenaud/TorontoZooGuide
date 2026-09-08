import { ItineraryPanelViews } from './components/itineraryPanelViews.js';
import { ItineraryPanelViewUrl } from './itineraryPanelViewUrl.js';

export class ItineraryPanelViewState {
   static activePanelView = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl();

   static getActiveItineraryPanelView() {
      return ItineraryPanelViewState.activePanelView;
   }

   static setActiveItineraryPanelView(view) {
      ItineraryPanelViewState.activePanelView = view;
      ItineraryPanelViewUrl.setItineraryPanelViewInUrl(view);
   }

   static makeItineraryPanelViewShell() {
      return ItineraryPanelViews.makeItineraryPanelViews({
         activeView: ItineraryPanelViewState.activePanelView,
         onViewChange: ItineraryPanelViewState.setActiveItineraryPanelView,
      });
   }

   static resetActiveItineraryPanelView(
      view = ItineraryPanelViewUrl.getItineraryPanelViewFromUrl()
   ) {
      ItineraryPanelViewState.activePanelView = view;
   }
}
