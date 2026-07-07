from __future__ import annotations

import json

from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.models import Animal
from api.models import Itinerary
from api.walk_graph.data_access.paths import VIEWING_SPOT_ROUTING_OVERRIDES_DIR
from api.walk_graph.resolve_viewing_walk_node_id import resolve_viewing_walk_node_id
from api.walk_graph.walk_node_id_for_viewing_spot import scheduling_walk_node_id_for_viewing_spot
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def test_viewing_spot_routing_overrides_dir_has_aldabra_tortoise_outdoor() -> None:
   override_path = (
      VIEWING_SPOT_ROUTING_OVERRIDES_DIR / 'aldabra_tortoise_outdoor.json' )

   assert override_path.is_file()

   override = json.loads( override_path.read_text( encoding='utf-8' ) )

   assert override[ 'id' ] == 'aldabra_tortoise_outdoor'
   assert override[ 'scheduling_walk_node_id' ] == 'v-0192'


def test_scheduling_walk_node_id_for_viewing_spot_uses_routing_override() -> None:
   pavilion = 'African Rainforest Pavilion'

   assert scheduling_walk_node_id_for_viewing_spot(
      'Aldabra Tortoise',
      pavilion,
      'Outdoor' ) == 'v-0192'


def test_walk_node_id_for_viewing_spot_uses_viewing_location_not_override() -> None:
   pavilion = 'African Rainforest Pavilion'

   assert walk_node_id_for_viewing_spot(
      'Aldabra Tortoise',
      pavilion,
      'Outdoor' ) == 'v-0281'


def test_resolve_viewing_walk_node_id_uses_viewing_location_not_override() -> None:
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

   walk_route = build_itinerary_walk_route( itinerary )
   tortoise_stop = next(
      stop
      for stop in walk_route.stops
      if stop.item_key.startswith( 'Aldabra Tortoise' ) )

   assert tortoise_stop.walk_node_id == 'v-0281'
