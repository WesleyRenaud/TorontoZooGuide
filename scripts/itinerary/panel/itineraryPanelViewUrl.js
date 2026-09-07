import { ItineraryPanelViews } from './components/itineraryPanelViews.js';
import { ItineraryPanelViewUrlHelpers } from './itineraryPanelViewUrlHelpers.js';

const VALID_ITINERARY_PANEL_VIEWS = new Set(
   Object.values(ItineraryPanelViews.ITINERARY_PANEL_VIEWS)
);

export class ItineraryPanelViewUrl {
   static ITINERARY_PANEL_VIEW_QUERY_PARAM = 'view';

   static normalizeItineraryPanelView(view) {
      return VALID_ITINERARY_PANEL_VIEWS.has(view)
         ? view
         : ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list;
   }

   static getItineraryPanelViewFromUrl(
      location = ItineraryPanelViewUrlHelpers.getDefaultLocation()
   ) {
      if (!location) {
         return ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list;
      }

      const view = new URL(location.href).searchParams.get(
         ItineraryPanelViewUrl.ITINERARY_PANEL_VIEW_QUERY_PARAM
      );

      return ItineraryPanelViewUrl.normalizeItineraryPanelView(view);
   }

   static setItineraryPanelViewInUrl(
      view,
      {
         location = ItineraryPanelViewUrlHelpers.getDefaultLocation(),
         history = ItineraryPanelViewUrlHelpers.getDefaultHistory(),
      } = {}
   ) {
      if (!location || !history?.replaceState) {
         return;
      }

      const normalizedView = ItineraryPanelViewUrl.normalizeItineraryPanelView(view);
      const url = new URL(location.href);

      url.searchParams.set(
         ItineraryPanelViewUrl.ITINERARY_PANEL_VIEW_QUERY_PARAM,
         normalizedView
      );
      history.replaceState(null, '', url);
   }
}
