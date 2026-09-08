import { ItineraryPanelView } from './components/itineraryPanelView.js';
import { ItineraryPanelViewUrlHelper } from './itineraryPanelViewUrlHelper.js';

export class ItineraryPanelViewResolver {
   static VALID_ITINERARY_PANEL_VIEWS = new Set(
      Object.values(ItineraryPanelView.ITINERARY_PANEL_VIEWS)
   );

   static ITINERARY_PANEL_VIEW_QUERY_PARAM = 'view';

   static normalizeItineraryPanelView(view) {
      return ItineraryPanelViewResolver.VALID_ITINERARY_PANEL_VIEWS.has(view)
         ? view
         : ItineraryPanelView.ITINERARY_PANEL_VIEWS.list;
   }

   static getItineraryPanelViewFromUrl(
      location = ItineraryPanelViewUrlHelper.getDefaultLocation()
   ) {
      if (!location) {
         return ItineraryPanelView.ITINERARY_PANEL_VIEWS.list;
      }

      const view = new URL(location.href).searchParams.get(
         ItineraryPanelViewResolver.ITINERARY_PANEL_VIEW_QUERY_PARAM
      );

      return ItineraryPanelViewResolver.normalizeItineraryPanelView(view);
   }

   static setItineraryPanelViewInUrl(
      view,
      {
         location = ItineraryPanelViewUrlHelper.getDefaultLocation(),
         history = ItineraryPanelViewUrlHelper.getDefaultHistory(),
      } = {}
   ) {
      if (!location || !history?.replaceState) {
         return;
      }

      const normalizedView = ItineraryPanelViewResolver.normalizeItineraryPanelView(view);
      const url = new URL(location.href);

      url.searchParams.set(
         ItineraryPanelViewResolver.ITINERARY_PANEL_VIEW_QUERY_PARAM,
         normalizedView
      );
      history.replaceState(null, '', url);
   }
}
