from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from http_client import post_route
from itinerary.support import ANIMAL_KEY, CAROUSEL, CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, entrance_travel_seconds_to_animal, LION_ITINERARY_ENTRY, schedule_time_after_seconds

from api.itinerary.routing.walk_travel_time import travel_time_seconds_between_nodes
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


def _travel_seconds_between_animals(
      *,
      from_species: str,
      from_exhibit: str,
      to_species: str,
      to_exhibit: str ) -> int:
   walk_graph = load_walk_graph()
   from_node_id = walk_node_id_for_viewing_spot(
      from_species,
      from_exhibit,
      None )
   to_node_id = walk_node_id_for_viewing_spot(
      to_species,
      to_exhibit,
      None )
   assert from_node_id is not None
   assert to_node_id is not None

   return travel_time_seconds_between_nodes(
      walk_graph,
      from_node_id,
      to_node_id )


def _find_animal( itinerary: dict[ str, object ], *, species: str, exhibit: str ) -> dict[ str, object ]:
   animals = itinerary.get( 'animals', [] )

   for animal in animals:
      if animal.get( 'species' ) == species and animal.get( 'exhibit' ) == exhibit:
         return animal

   raise AssertionError( f'Expected animal { species } / { exhibit } in itinerary response' )


def test_set_get_and_clear_itinerary_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'arrivalTime': '09:30',
         'departureTime': '17:00',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [ CAROUSEL ],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'
   assert set_response[ 'reasons' ] == []
   assert set_response[ 'itinerary_path' ] == {
      'stops': [],
      'legs': [],
      'points': [],
   }

   status, get_response = post_route( '/get-itinerary', {} )

   assert status == 200
   itinerary = get_response[ 'itinerary' ]
   assert itinerary[ 'date' ] == '2026-06-15'
   assert get_response[ 'itinerary_path' ] == {
      'stops': [],
      'legs': [],
      'points': [],
   }
   assert itinerary[ 'arrival_time' ] == '9:30 AM'
   assert itinerary[ 'departure_time' ] == '5:00 PM'
   assert _find_animal(
      itinerary,
      species='African Lion',
      exhibit='Africa Savanna',
   )[ 'species' ] == 'African Lion'
   assert [ attraction[ 'name' ] for attraction in itinerary[ 'attractions' ] ] == [
      CAROUSEL,
   ]

   status, clear_response = post_route( '/clear-itinerary', {} )

   assert status == 200
   assert clear_response[ 'success' ] is True

   status, empty_response = post_route( '/get-itinerary-date', {} )

   assert status == 200
   assert empty_response[ 'date' ] is None


def test_schedule_and_unschedule_animal_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'arrivalTime': '09:00',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, schedule_response = post_route(
      '/schedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': ANIMAL_KEY,
         'startTime': '14:00',
      },
   )

   assert status == 200
   assert schedule_response[ 'status' ] == 'success'
   scheduled_lion = _find_animal(
      schedule_response[ 'itinerary' ],
      species='African Lion',
      exhibit='Africa Savanna',
   )
   assert scheduled_lion[ 'start_time' ] == '2:00 PM'
   assert scheduled_lion[ 'end_time' ] is not None
   itinerary_path = schedule_response[ 'itinerary_path' ]
   assert itinerary_path[ 'points' ]
   assert itinerary_path[ 'stops' ]
   assert itinerary_path[ 'legs' ]

   status, unschedule_response = post_route(
      '/unschedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': ANIMAL_KEY,
      },
   )

   assert status == 200
   assert unschedule_response[ 'status' ] == 'success'

   status, get_response = post_route( '/get-itinerary', {} )

   assert status == 200
   unscheduled_lion = _find_animal(
      get_response[ 'itinerary' ],
      species='African Lion',
      exhibit='Africa Savanna',
   )
   assert unscheduled_lion[ 'start_time' ] is None
   assert unscheduled_lion[ 'end_time' ] is None
   assert 'itinerary_path' in get_response


def test_unschedule_all_itinerary_items_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'arrivalTime': '09:30',
         'departureTime': '17:00',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [ CAROUSEL ],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, schedule_response = post_route(
      '/schedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': ANIMAL_KEY,
         'startTime': '14:00',
      },
   )

   assert status == 200
   assert schedule_response[ 'status' ] == 'success'

   status, unschedule_all_response = post_route(
      '/unschedule-all-itinerary-items',
      {},
   )

   assert status == 200
   assert unschedule_all_response[ 'status' ] == 'success'

   itinerary = unschedule_all_response[ 'itinerary' ]
   lion = _find_animal(
      itinerary,
      species='African Lion',
      exhibit='Africa Savanna',
   )

   assert lion[ 'start_time' ] is None
   assert lion[ 'end_time' ] is None
   assert itinerary[ 'arrival_time' ] == '9:30 AM'
   assert itinerary[ 'departure_time' ] == '5:00 PM'
   assert [ attraction[ 'name' ] for attraction in itinerary[ 'attractions' ] ] == [
      CAROUSEL,
   ]


def test_set_arrival_time_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, arrival_response = post_route(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': '09:45' },
   )

   assert status == 200
   assert arrival_response[ 'status' ] == 'success'
   assert arrival_response[ 'itinerary' ][ 'arrival_time' ] == '9:45 AM'

   status, get_response = post_route( '/get-itinerary', {} )

   assert status == 200
   assert get_response[ 'itinerary' ][ 'arrival_time' ] == '9:45 AM'


def test_remove_item_from_itinerary_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [ CAROUSEL ],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, remove_response = post_route(
      '/remove-item-from-itinerary',
      {
         'itemType': 'attractions',
         'key': CAROUSEL,
      },
   )

   assert status == 200
   assert remove_response[ 'status' ] == 'success'

   status, get_response = post_route( '/get-itinerary', {} )

   assert status == 200
   assert get_response[ 'itinerary' ][ 'attractions' ] == []
   assert len( get_response[ 'itinerary' ][ 'animals' ] ) == 1


def test_date_change_adjusts_arrival_time_via_http(
      integration_db: Path,
) -> None:
   status, initial_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-20',
         'arrivalTime': '09:15',
         'departureTime': '17:00',
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert initial_response[ 'status' ] == 'success'

   status, date_change_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-22',
         'arrivalTime': '09:15',
         'departureTime': '17:00',
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
      },
   )

   assert status == 200
   assert date_change_response[ 'status' ] == 'success'
   assert date_change_response[ 'itinerary' ][ 'date' ] == '2026-06-22'
   assert date_change_response[ 'itinerary' ][ 'arrival_time' ] == '9:30 AM'
   assert date_change_response[ 'adjustments' ] == [
      {
         'type': 'arrivalTimeAdjusted',
         'field': 'arrivalTime',
         'previous_value': '9:15 AM',
         'value': '09:30',
         'reason': 'arrivalOutsideAdmissionHours',
      },
   ]


def test_bulk_schedule_animals_via_http(
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
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, bulk_response = post_route( '/bulk-schedule-animals', {} )

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


def test_set_departure_time_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'departureTime': '17:00',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, departure_response = post_route(
      '/set-itinerary-departure-time',
      { 'departureTime': '16:30' },
   )

   assert status == 200
   assert departure_response[ 'status' ] == 'success'
   assert departure_response[ 'itinerary' ][ 'departure_time' ] == '4:30 PM'

   status, get_response = post_route( '/get-itinerary', {} )

   assert status == 200
   assert get_response[ 'itinerary' ][ 'departure_time' ] == '4:30 PM'


def test_accept_itinerary_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_route(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'animals': [ LION_ITINERARY_ENTRY ],
         'attractions': [ CAROUSEL ],
         'guardiansTalks': [],
         'wildEncounters': [],
         'confirmingEarlyAdmission': True,
      },
   )

   assert status == 200
   assert set_response[ 'status' ] == 'success'

   status, accept_response = post_route( '/accept-itinerary', {} )

   assert status == 200
   assert accept_response[ 'success' ] is True
   assert accept_response[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert len( accept_response[ 'itinerary' ][ 'animals' ] ) == 1
   assert [ attraction[ 'name' ] for attraction in accept_response[ 'itinerary' ][ 'attractions' ] ] == [
      CAROUSEL,
   ]
