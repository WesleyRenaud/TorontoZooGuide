from __future__ import annotations

import json

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from api.models import Animal
from api.models import Itinerary
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.data_access.paths import VIEWING_SPOT_ROUTING_OVERRIDES_DIR
from api.walk_graph.resolve_viewing_walk_node_id import resolve_viewing_walk_node_id
from api.walk_graph.viewing_spot_routing_overrides import bulk_schedule_visit_before_rules
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


def test_bulk_schedule_visit_before_rules_include_aldabra_tortoise_outdoor() -> None:
   rules = bulk_schedule_visit_before_rules()

   assert any(
      rule.visit_first.key()
         == ( 'Aldabra Tortoise', 'African Rainforest Pavilion', 'Outdoor' )
      for rule in rules )


def test_sort_animals_for_bulk_schedule_visits_outdoor_tortoise_before_gorillas() -> None:
   graph = load_walk_graph()
   pavilion = 'African Rainforest Pavilion'
   animals = sort_animals_for_bulk_schedule(
      graph,
      [
         ItineraryAnimalRecord(
            species='Western Lowland Gorilla',
            exhibit=pavilion,
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Western Lowland Gorilla',
            exhibit=pavilion,
            enclosure_name='Indoor',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='Aldabra Tortoise',
            exhibit=pavilion,
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      start_node_id=str( graph[ 'entrance_node_id' ] ) )

   species_order = [ animal.species for animal in animals ]
   tortoise_index = species_order.index( 'Aldabra Tortoise' )
   gorilla_outdoor_index = species_order.index( 'Western Lowland Gorilla' )

   assert tortoise_index < gorilla_outdoor_index


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
