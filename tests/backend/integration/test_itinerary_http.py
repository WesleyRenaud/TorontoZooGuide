from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from api_test_support.itinerary_test_support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY
from api_test_support.itinerary_test_support import entrance_travel_seconds_to_animal
from api_test_support.itinerary_test_support import LION_ITINERARY_ENTRY
from api_test_support.itinerary_test_support import schedule_time_after_seconds
from http_client import post_route

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


def _travel_seconds_between_animals(
      *,
      from_species: str,
      from_exhibit: str,
      to_species: str,
      to_exhibit: str ) -> int:
   walk_graph = WalkGraphProvider.fetch()
   from_node_id = ViewingSpotWalkNodeIdResolver.resolve(
      from_species,
      from_exhibit,
      None )
   to_node_id = ViewingSpotWalkNodeIdResolver.resolve(
      to_species,
      to_exhibit,
      None )
   assert from_node_id is not None
   assert to_node_id is not None

   return WalkTravelTimeCalculator.seconds_between_nodes(
      walk_graph,
      from_node_id,
      to_node_id )


def _find_animal( itinerary: dict[ str, object ], *, species: str, exhibit: str ) -> dict[ str, object ]:
   animals = itinerary.get( 'animals', [] )

   for animal in animals:
      if animal.get( 'species' ) == species and animal.get( 'exhibit' ) == exhibit:
         return animal

   raise AssertionError( f'Expected animal { species } / { exhibit } in itinerary response' )


def test_bulk_schedule_itinerary_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-20',
         'animals': [
            LION_ITINERARY_ENTRY,
            CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         ],
         'attractions': [],
         'transportations': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, bulk_response = post_route( '/bulk-schedule-itinerary', {} )

   assert status == 200
   assert bulk_response[ 'status' ] == 'success'

   cheetah = _find_animal(
      bulk_response[ 'itinerary' ],
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
   )
   lion = _find_animal(
      bulk_response[ 'itinerary' ],
      species='African Lion',
      exhibit='Africa Savanna',
   )

   assert cheetah[ 'start_time' ] == schedule_time_after_seconds(
      '9:30 AM',
      entrance_travel_seconds_to_animal(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor' ) )
   assert cheetah[ 'end_time' ] == schedule_time_after_seconds(
      cheetah[ 'start_time' ],
      5 * 60 )
   assert lion[ 'start_time' ] == schedule_time_after_seconds(
      cheetah[ 'end_time' ],
      _travel_seconds_between_animals(
         from_species='Cheetah',
         from_exhibit='Indo-Malaya Outdoor',
         to_species='African Lion',
         to_exhibit='Africa Savanna' ) )
   assert lion[ 'end_time' ] == schedule_time_after_seconds(
      lion[ 'start_time' ],
      8 * 60 )
