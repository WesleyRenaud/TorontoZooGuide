from __future__ import annotations

from api.itinerary.routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from api.models import Animal
from api.models import Itinerary
from api.walk_graph.resolve_viewing_walk_node_id import resolve_viewing_walk_node_id
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def test_walk_node_id_for_outdoor_aldabra_tortoise_uses_viewing_location() -> None:
   pavilion = 'African Rainforest Pavilion'

   assert walk_node_id_for_viewing_spot(
      'Aldabra Tortoise',
      pavilion,
      'Outdoor' ) == 'v-0281'


def test_resolve_viewing_walk_node_id_for_outdoor_aldabra_tortoise() -> None:
   pavilion = 'African Rainforest Pavilion'

   assert resolve_viewing_walk_node_id(
      'Aldabra Tortoise',
      pavilion,
      47.091,
      66.261,
      'Outdoor' ) == 'v-0281'


def test_build_itinerary_walk_route_routes_to_outdoor_tortoise_viewing_node() -> None:
   pavilion = 'African Rainforest Pavilion'
   itinerary = Itinerary(
      animals=[
         Animal(
            species='Aldabra Tortoise',
            exhibit=pavilion,
            enclosure_name='Outdoor',
            enclosure_type='Outdoor',
            x_coord=47.091,
            y_coord=66.261,
            start_time='10:30 AM',
            end_time='10:33 AM',
         ),
         Animal(
            species='Western Lowland Gorilla',
            exhibit=pavilion,
            enclosure_name='Outdoor',
            enclosure_type='Outdoor',
            x_coord=48.951,
            y_coord=59.856,
            start_time='10:33 AM',
            end_time='10:36 AM',
         ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      date='2026-07-05' )

   walk_route = ItineraryWalkRouteBuilder.build( itinerary )
   tortoise_stop = next(
      stop
      for stop in walk_route.stops
      if stop.item_key.startswith( 'Aldabra Tortoise' ) )

   assert tortoise_stop.walk_node_id == 'v-0281'
