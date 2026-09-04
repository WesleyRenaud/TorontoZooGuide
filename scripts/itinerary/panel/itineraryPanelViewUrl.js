import { ItineraryPanelViews } from './components/itineraryPanelViews.js';

const VALID_ITINERARY_PANEL_VIEWS = new Set(
   Object.values(ItineraryPanelViews.ITINERARY_PANEL_VIEWS)
);

function getDefaultLocation() {
   return globalThis.location ?? null;
}

function getDefaultHistory() {
   return globalThis.history ?? null;
}

export class ItineraryPanelViewUrl {
   static ITINERARY_PANEL_VIEW_QUERY_PARAM = 'view';

   static normalizeItineraryPanelView(view) {
      return VALID_ITINERARY_PANEL_VIEWS.has(view)
         ? view
         : ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list;
   }

   static getItineraryPanelViewFromUrl(
      location = getDefaultLocation()
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
         location = getDefaultLocation(),
         history = getDefaultHistory(),
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
