from __future__ import annotations

from typing import Any

from http_support import make_handler, response_json, StubZooControllers, WILD_ENCOUNTER_NAME
import pytest

import api.server as server

def test_get_animals_by_exhibit_endpoint_adds_type_and_maps_payload(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-animals-by-exhibit',
      {
         'month': 'June',
         'year': 2026,
         'day': 15,
         'temp': 22,
         'exhibitsToInclude': [ 'Africa Savanna' ]
      }
   )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': 15,
         'month': 'June',
         'year': 2026,
         'temp': 22,
         'include_off_display_animals': False,
         'threshold': 0,
         'exhibits_to_include': [ 'Africa Savanna' ]
      }
   )


def test_get_visible_animals_endpoint_maps_payload_and_response(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': 'June',
         'year': 2026,
         'day': 15,
         'temp': 22,
         'includeOffDisplayAnimals': True
      }
   )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler )[ 'animals' ][ 0 ][ 'species' ] == 'African Lion'
   assert StubZooControllers.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'day': 15,
         'month': 'June',
         'year': 2026,
         'temp': 22,
         'include_off_display_animals': True,
         'threshold': 0
      }
   )
   assert StubZooControllers.instances[ 0 ].closed is True


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-exhibits-in-region', { 'region': 'Africa' }, 'exhibits' ),
      ( '/get-regions', {}, 'regions' ),
      ( '/get-animal-names-by-exhibit', { 'exhibit': 'Africa Savanna' }, 'animals' ),
      (
         '/get-animal-viewing-scopes',
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         'viewingScopes'
      ),
      ( '/get-animal-information', { 'species': 'African Lion' }, 'information' ),
      ( '/get-pavilions', {}, 'pavilions' ),
      ( '/get-restaurants', { 'month': 'June', 'day': 15, 'year': 2026 }, 'restaurants' ),
      ( '/get-restrooms', { 'month': 'June', 'day': 15, 'year': 2026 }, 'restrooms' ),
      ( '/get-gift-shops', { 'month': 'June', 'day': 15, 'year': 2026 }, 'gift_shops' ),
      ( '/get-attractions', { 'month': 'June', 'day': 15, 'year': 2026 }, 'attractions' ),
      ( '/get-zoomobile-route', { 'zoomobileRoute': 'summer', 'month': 'June', 'day': 15, 'year': 2026 }, 'route' ),
      ( '/get-guardians-talks', { 'month': 'June', 'day': 15, 'year': 2026 }, 'guardians_talks' ),
      ( '/get-wild-encounters', { 'month': 'June', 'day': 15, 'year': 2026 }, 'wild_encounters' ),
      ( '/get-drinking-fountains', { 'month': 'June', 'day': 15, 'year': 2026 }, 'drinking_fountains' ),
      ( '/get-defibrillators', {}, 'defibrillators' ),
      ( '/get-emergency-intercoms', {}, 'emergency_intercoms' ),
      ( '/get-guest-services', {}, 'guest_services' ),
      ( '/get-picnic-sites', {}, 'picnic_sites' ),
      ( '/get-event-sites', {}, 'event_sites' ),
      ( '/get-updates', { 'month': 'June', 'day': 15, 'year': 2026 }, 'updates' ),
      ( '/get-closed-exhibits', { 'month': 'June', 'day': 15, 'year': 2026 }, 'closed_exhibits' ),
      ( '/get-zoo-hours', { 'day': 20, 'month': 'June', 'year': 2026 }, 'hours' )
   ]
)
def test_read_endpoints_return_json_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      response_key: str ) -> None:
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_key in response_json( handler )


def test_get_restrooms_endpoint_maps_closed_toggle(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-restrooms',
         {
            'month': 'June',
            'day': 15,
            'year': 2026,
            'includeClosedRestrooms': True
         }
   )

   server.MyHandler.do_POST( handler )

   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'get_restrooms',
         {
            'day': 15,
            'month': 'June',
            'year': 2026,
            'include_closed_restrooms': True
         }
      )
   ]


def test_get_wild_encounters_endpoint_uses_available_database_results(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/get-wild-encounters',
      { 'month': 'June', 'day': 21, 'year': 2026 } )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [
      ( 'get_available_wild_encounters', { 'month': 'June', 'day': 21, 'year': 2026 } )
   ]
   assert [ item[ 'name' ] for item in result[ 'wild_encounters' ] ] == [
      WILD_ENCOUNTER_NAME
   ]


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/get-animal-species-names',
         {},
         ( 'get_animal_species_names', {} ),
         { 'species': [ 'African Lion', 'Amur Tiger' ] }
      ),
      (
         '/get-exhibits',
         {},
         ( 'get_exhibits', {} ),
         { 'exhibits': [ 'Africa Savanna', 'Eurasia Wilds' ] }
      ),
      (
         '/get-exhibits-by-region',
         {},
         (
            'get_regions_with_exhibits',
            {}
         ),
         {
            'regions': [
               {
                  'name': 'Africa',
                  'exhibits': [ 'Africa Savanna' ]
               }
            ]
         }
      ),
      (
         '/get-restaurant-names',
         {},
         ( 'get_restaurant_names', {} ),
         { 'restaurants': [ 'Africa Restaurant' ] }
      ),
      (
         '/get-restroom-names',
         {},
         ( 'get_restroom_names', {} ),
         { 'restrooms': [ 'Entrance Restroom' ] }
      ),
      (
         '/get-gift-shop-names',
         {},
         ( 'get_gift_shop_names', {} ),
         { 'gift_shops': [ 'Zootique' ] }
      ),
      (
         '/get-attraction-names',
         {},
         ( 'get_attraction_names', {} ),
         { 'attractions': [ 'Conservation Carousel' ] }
      ),
      (
         '/get-zoomobile-station-names',
         {},
         ( 'get_zoomobile_station_names', {} ),
         { 'zoomobile_stations': [ 'Main Zoomobile Station' ] }
      ),
      (
         '/get-guardians-talk-locations',
         {},
         ( 'get_guardians_talk_locations', {} ),
         { 'guardians_talk_locations': [ 'Africa Savanna' ] }
      ),
      (
         '/get-guardians-talk-names',
         {},
         ( 'get_guardians_talk_names', {} ),
         { 'guardians_talks': [ 'African Lion' ] }
      ),
      (
         '/get-guardians-talk-names-at-location',
         { 'location': 'Africa Savanna' },
         (
            'get_guardians_talk_names_at_location',
            { 'location': 'Africa Savanna' }
         ),
         { 'guardians_talks': [ 'African Lion' ] }
      ),
      (
         '/get-guardians-talk-occurrences',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna'
         },
         (
            'get_guardians_talk_occurrences',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna'
            }
         ),
         {
            'occurrences': [
               {
                  'date': '2026-06-15',
                  'time': '10:00'
               }
            ],
            'talk': 'African Lion',
            'location': 'Africa Savanna'
         }
      ),
      (
         '/get-wild-encounter-names',
         {},
         ( 'get_wild_encounter_names', {} ),
         { 'wild_encounters': [ 'African Rainforest' ] }
      ),
      (
         '/get-wild-encounter-occurrences',
         { 'wildEncounter': 'African Rainforest' },
         (
            'get_wild_encounter_occurrences',
            { 'wild_encounter_name': 'African Rainforest' }
         ),
         {
            'occurrences': [
               {
                  'date': '2026-06-15',
                  'time': '14:00'
               }
            ],
            'wildEncounter': 'African Rainforest'
         }
      ),
      (
         '/get-active-update-options',
         {},
         ( 'get_unexpired_updates', {} ),
         {
            'updates': [
               {
                  'title': 'New baby giraffe',
                  'description': 'Come meet the new calf.',
                  'type': 'New Arrival',
                  'start_date': '2026-06-01',
                  'end_date': '2026-06-30'
               }
            ]
         }
      )
   ]
)
def test_console_options_endpoints_map_payloads_and_return_expected_keys(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_call: tuple[ str, dict[ str, Any ] ],
      response_subset: dict[ str, Any ] ) -> None:
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [ expected_call ]

   for key, value in response_subset.items():
      assert result[ key ] == value

