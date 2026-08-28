from __future__ import annotations

from typing import Any

from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers
import pytest

import api.http_request_handler as server


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
         '/get-transportation-station-names',
         {},
         ( 'get_transportation_station_names', { 'transportation': 'Zoomobile' } ),
         { 'transportation_stations': [ 'Main Zoomobile Station' ] }
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
                  'time': '10:00 AM'
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
                  'time': '2:00 PM'
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

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [ expected_call ]

   for key, value in response_subset.items():
      assert result[ key ] == value
