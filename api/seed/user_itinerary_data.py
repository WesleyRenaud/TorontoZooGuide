from __future__ import annotations

from ..itinerary.data_access.clear_itinerary_provider import ClearItineraryProvider
from ..itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ..types import Cursor


def clear_user_itinerary_data( cursor: Cursor ) -> None:
   ClearItineraryProvider.clear_itinerary_exhibits( cursor )
   ClearItineraryProvider.clear_itinerary_animals( cursor )
   ClearItineraryProvider.clear_itinerary_attractions( cursor )
   ClearItineraryProvider.clear_itinerary_guardians_talks( cursor )
   ClearItineraryProvider.clear_itinerary_wild_encounters( cursor )
   ClearItineraryProvider.clear_itinerary_events( cursor )
   ItineraryWalkRouteProvider.clear_itinerary_walk_route( cursor )
   ClearItineraryProvider.clear_itinerary_date( cursor )
