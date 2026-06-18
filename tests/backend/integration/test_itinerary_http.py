from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from http_client import post_itinerary_route
from itinerary.support import ANIMAL_KEY, CAROUSEL, LION_ITINERARY_ENTRY


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

   status, set_response = post_itinerary_route(
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

   status, get_response = post_itinerary_route( '/get-itinerary', {} )

   assert status == 200
   itinerary = get_response[ 'itinerary' ]
   assert itinerary[ 'date' ] == '2026-06-15'
   assert itinerary[ 'arrival_time' ] == '09:30'
   assert itinerary[ 'departure_time' ] == '17:00'
   assert _find_animal(
      itinerary,
      species='African Lion',
      exhibit='Africa Savanna',
   )[ 'species' ] == 'African Lion'
   assert [ attraction[ 'name' ] for attraction in itinerary[ 'attractions' ] ] == [
      CAROUSEL,
   ]

   status, clear_response = post_itinerary_route( '/clear-itinerary', {} )

   assert status == 200
   assert clear_response[ 'success' ] is True

   status, empty_response = post_itinerary_route( '/get-itinerary-date', {} )

   assert status == 200
   assert empty_response[ 'date' ] is None


def test_schedule_and_unschedule_animal_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_itinerary_route(
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

   status, schedule_response = post_itinerary_route(
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
   assert scheduled_lion[ 'start_time' ] == '14:00'
   assert scheduled_lion[ 'end_time' ] is not None

   status, unschedule_response = post_itinerary_route(
      '/unschedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': ANIMAL_KEY,
      },
   )

   assert status == 200
   assert unschedule_response[ 'status' ] == 'success'

   status, get_response = post_itinerary_route( '/get-itinerary', {} )

   assert status == 200
   unscheduled_lion = _find_animal(
      get_response[ 'itinerary' ],
      species='African Lion',
      exhibit='Africa Savanna',
   )
   assert unscheduled_lion[ 'start_time' ] is None
   assert unscheduled_lion[ 'end_time' ] is None


def test_set_arrival_time_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_itinerary_route(
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

   status, arrival_response = post_itinerary_route(
      '/set-itinerary-arrival-time',
      { 'arrivalTime': '09:45' },
   )

   assert status == 200
   assert arrival_response[ 'status' ] == 'success'
   assert arrival_response[ 'arrivalTime' ] == '09:45'

   status, get_response = post_itinerary_route( '/get-itinerary', {} )

   assert status == 200
   assert get_response[ 'itinerary' ][ 'arrival_time' ] == '09:45'


def test_remove_item_from_itinerary_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, set_response = post_itinerary_route(
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

   status, remove_response = post_itinerary_route(
      '/remove-item-from-itinerary',
      {
         'itemType': 'attractions',
         'key': CAROUSEL,
      },
   )

   assert status == 200
   assert remove_response[ 'status' ] == 'success'

   status, get_response = post_itinerary_route( '/get-itinerary', {} )

   assert status == 200
   assert get_response[ 'itinerary' ][ 'attractions' ] == []
   assert len( get_response[ 'itinerary' ][ 'animals' ] ) == 1


def test_date_change_adjusts_arrival_time_via_http(
      integration_db: Path,
) -> None:
   status, initial_response = post_itinerary_route(
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

   status, date_change_response = post_itinerary_route(
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
   assert date_change_response[ 'itinerary' ][ 'arrival_time' ] == '09:30'
   assert date_change_response[ 'adjustments' ] == [
      {
         'type': 'arrivalTimeAdjusted',
         'field': 'arrivalTime',
         'previous_value': '09:15',
         'value': '09:30',
         'reason': 'arrivalOutsideAdmissionHours',
      },
   ]
