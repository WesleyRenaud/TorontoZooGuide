from __future__ import annotations

from collections.abc import Callable
from datetime import date
from pathlib import Path

from http_client import post_route
from support import MAP_VISIT_DATE


def test_search_returns_matching_animal_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, response = post_route(
      '/search',
      {
         'query': 'lion',
         'includeAnimals': True,
         'includePavilions': False,
         'includeRestaurants': False,
         'includeRestrooms': False,
         'includeGiftShops': False,
         'includeAttractions': False,
         'includeZoomobileStations': False,
         'includeGuardiansTalks': False,
         'includeWildEncounters': False,
         'zoomobileRoute': 'summer',
         **MAP_VISIT_DATE,
      },
   )

   assert status == 200
   assert response[ 'animals' ]
   assert response[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert any(
      animal[ 'species' ] == 'African Lion'
      for animal in response[ 'animals' ]
   )


def test_get_visible_animals_returns_exhibit_filtered_animals_via_http(
      integration_db: Path,
) -> None:
   status, response = post_route(
      '/get-visible-animals',
      {
         **MAP_VISIT_DATE,
         'includeOffDisplayAnimals': False,
      },
   )

   assert status == 200
   assert response[ 'animals' ]
   assert all( animal[ 'species' ] for animal in response[ 'animals' ] )
   assert all( animal[ 'likelihood' ] > 0 for animal in response[ 'animals' ] )

   status, filtered_response = post_route(
      '/get-animals-by-exhibit',
      {
         **MAP_VISIT_DATE,
         'exhibitsToInclude': [ 'Africa Savanna' ],
      },
   )

   assert status == 200
   assert filtered_response[ 'animals' ]
   assert filtered_response[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert { animal[ 'exhibit' ] for animal in filtered_response[ 'animals' ] } == {
      'Africa Savanna',
   }


def test_get_zoo_hours_returns_operating_bounds_via_http(
      integration_db: Path,
) -> None:
   status, weekday_response = post_route(
      '/get-zoo-hours',
      {
         'day': 22,
         'month': 'June',
         'year': 2026,
      },
   )

   assert status == 200
   assert weekday_response[ 'hours' ] == {
      'date': '2026-06-22',
      'earlyAdmissionTime': None,
      'openTime': '09:30',
      'lastAdmissionTime': '17:00',
      'closeTime': '18:00',
   }

   status, holiday_response = post_route(
      '/get-zoo-hours',
      {
         'day': 25,
         'month': 'December',
         'year': 2026,
      },
   )

   assert status == 200
   assert holiday_response[ 'hours' ] == {
      'date': '2026-12-25',
      'earlyAdmissionTime': None,
      'openTime': '11:00',
      'lastAdmissionTime': '15:00',
      'closeTime': '16:00',
   }


def test_create_and_get_updates_via_http(
      integration_db: Path,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   status, create_response = post_route(
      '/create-update',
      {
         'title': 'Savanna viewing change',
         'description': 'Some animals may be off display.',
         'type': 'Closure',
         'startDate': '2026-06-15',
         'endDate': None,
      },
   )

   assert status == 200
   assert create_response[ 'success' ] is True

   status, updates_response = post_route(
      '/get-updates',
      {
         'month': 'June',
         'day': 15,
         'year': 2026,
      },
   )

   assert status == 200
   assert len( updates_response[ 'updates' ] ) == 1
   assert updates_response[ 'updates' ][ 0 ] == {
      'title': 'Savanna viewing change',
      'description': 'Some animals may be off display.',
      'type': 'Closure',
      'start_date': '2026-06-15',
      'end_date': None,
   }
