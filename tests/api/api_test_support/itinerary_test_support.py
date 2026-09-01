from __future__ import annotations

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.shared.calendar_dates import DateValues
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


CAROUSEL = 'Conservation Carousel'
ANIMAL_KEY = 'African Lion||Africa Savanna'

LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}

CHEETAH_INDO_MALAYA_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Indo-Malaya Outdoor',
}


def entrance_travel_seconds_to_animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> int:
   walk_graph = WalkGraphProvider.fetch()
   walk_node_id = ViewingSpotWalkNodeIdResolver.resolve(
      species,
      exhibit,
      enclosure_name )

   if walk_node_id is None:
      return 0

   return WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      walk_node_id )


def schedule_time_after_seconds(
      start_time: str,
      offset_seconds: int ) -> str:
   start_seconds = DateValues.time_value_in_seconds( start_time )
   assert start_seconds is not None
   result = DateValues.schedule_time_key_from_seconds(
      start_seconds + offset_seconds )
   assert result is not None
   return result
