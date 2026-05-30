import { ITINERARY_PANEL_VIEWS } from './components/itineraryPanelViews.js';

export const ITINERARY_PANEL_VIEW_QUERY_PARAM = 'view';

const VALID_ITINERARY_PANEL_VIEWS = new Set(
   Object.values(ITINERARY_PANEL_VIEWS)
);

function getDefaultLocation() {
   return globalThis.location ?? null;
}

function getDefaultHistory() {
   return globalThis.history ?? null;
}

export function normalizeItineraryPanelView(view) {
   return VALID_ITINERARY_PANEL_VIEWS.has(view)
      ? view
      : ITINERARY_PANEL_VIEWS.list;
}

export function getItineraryPanelViewFromUrl(
   location = getDefaultLocation()
) {
   if (!location) {
      return ITINERARY_PANEL_VIEWS.list;
   }

   const view = new URL(location.href).searchParams.get(
      ITINERARY_PANEL_VIEW_QUERY_PARAM
   );

   return normalizeItineraryPanelView(view);
}

export function setItineraryPanelViewInUrl(
   view,
   {
      location = getDefaultLocation(),
      history = getDefaultHistory(),
   } = {}
) {
   if (!location || !history?.replaceState) {
      return;
   }

   const normalizedView = normalizeItineraryPanelView(view);
   const url = new URL(location.href);

   url.searchParams.set(
      ITINERARY_PANEL_VIEW_QUERY_PARAM,
      normalizedView
   );
   history.replaceState(null, '', url);
}
