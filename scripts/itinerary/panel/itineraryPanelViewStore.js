import { ItineraryPanelView } from './components/itineraryPanelView.js';
import { ItineraryPanelViewResolver } from './itineraryPanelViewResolver.js';

export class ItineraryPanelViewStore {
   static activePanelView = ItineraryPanelViewResolver.getItineraryPanelViewFromUrl();

   static getActiveItineraryPanelView() {
      return ItineraryPanelViewStore.activePanelView;
   }

   static setActiveItineraryPanelView(view) {
      ItineraryPanelViewStore.activePanelView = view;
      ItineraryPanelViewResolver.setItineraryPanelViewInUrl(view);
   }

   static makeItineraryPanelViewShell() {
      return ItineraryPanelView.makeItineraryPanelViews({
         activeView: ItineraryPanelViewStore.activePanelView,
         onViewChange: ItineraryPanelViewStore.setActiveItineraryPanelView,
      });
   }

   static resetActiveItineraryPanelView(
      view = ItineraryPanelViewResolver.getItineraryPanelViewFromUrl()
   ) {
      ItineraryPanelViewStore.activePanelView = view;
   }
}
