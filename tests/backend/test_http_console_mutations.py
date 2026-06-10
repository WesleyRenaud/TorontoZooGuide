from __future__ import annotations

from typing import Any

from http_support import make_handler, response_json, StubZooControllers
import pytest

import api.server as server
from api.shared.enums import AnimalViewingScope

@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-animal-off-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'indoor',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         },
         (
            'set_animal_as_off_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewing_scope': AnimalViewingScope.INDOOR,
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Unavailable.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'indoor',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         }
      ),
      (
         '/set-animal-on-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'outdoor'
         },
         (
            'set_animal_as_on_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewing_scope': AnimalViewingScope.OUTDOOR
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'outdoor'
         }
      ),
      (
         '/set-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         },
         (
            'set_animal_limited_viewing_schedule',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'daily_start_time': '09:00',
               'daily_end_time': '10:00',
               'message': 'Morning only.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         }
      ),
      (
         '/remove-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'viewingScope': 'all'
         },
         (
            'remove_animal_visibility_schedule',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         }
      ),
      (
         '/set-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         },
         (
            'set_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Hard to spot.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         }
      ),
      (
         '/remove-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         (
            'remove_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         }
      ),
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_exhibit_as_closed',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-exhibit-open',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_exhibit_as_open',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/set-restaurant-closed',
         {
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restaurant_as_closed',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restroom-closed',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restroom_as_closed',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restroom-open',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_restroom_as_open',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/set-restroom-alert',
         {
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         },
         (
            'set_restroom_alert',
            {
               'restroom': 'Entrance Restroom',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Women\'s restroom is temporarily unavailable.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         }
      ),
      (
         '/remove-restroom-alert',
         {
            'restroom': 'Entrance Restroom'
         },
         (
            'remove_restroom_alert',
            {
               'restroom': 'Entrance Restroom'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom'
         }
      ),
      (
         '/create-update',
         {
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'create_update',
            {
               'title': 'New baby giraffe',
               'description': 'Come meet the new calf.',
               'update_type': 'New Arrival',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/create-update',
         {
            'title': 'Open-ended update',
            'description': 'This has no end date.',
            'type': 'Closure',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'create_update',
            {
               'title': 'Open-ended update',
               'description': 'This has no end date.',
               'update_type': 'Closure',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'title': 'Open-ended update',
            'description': 'This has no end date.',
            'type': 'Closure',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/end-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         },
         (
            'end_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'end_date': '2026-06-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         }
      ),
      (
         '/edit-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
         },
         (
            'edit_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'description': 'Updated calf details.',
               'update_type': 'Closure',
               'end_date': '2026-07-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
         }
      ),
      (
         '/set-gift-shop-closed',
         {
            'giftShop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_gift_shop_as_closed',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'gift_shop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restaurant-closure-override',
         {
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_restaurant_closure_override',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         }
      ),
      (
         '/set-gift-shop-closure-override',
         {
            'giftShop': 'Zootique',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_gift_shop_closure_override',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'gift_shop': 'Zootique',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         }
      ),
      (
         '/set-attraction-closed',
         {
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_attraction_as_closed',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-attraction-closure-override',
         {
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         },
         (
            'set_attraction_closure_override',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-20',
               'end_date': '2026-06-21',
               'message': 'Closed this weekend.'
            }
         ),
         {
            'success': True,
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-20',
            'endDate': '2026-06-21',
            'message': 'Closed this weekend.'
         }
      ),
      (
         '/set-zoomobile-station-closed',
         {
            'zoomobileStation': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_zoomobile_station_as_closed',
            {
               'zoomobile_station': 'Africa Zoomobile Station',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-zoomobile-station-open',
         {
            'zoomobileStation': 'Africa Zoomobile Station'
         },
         (
            'set_zoomobile_station_as_open',
            {
               'zoomobile_station': 'Africa Zoomobile Station'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station'
         }
      ),
      (
         '/set-drinking-fountains-closed',
         {
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_drinking_fountains_as_closed',
            {
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-drinking-fountains-open',
         {
            'startDate': '2026-07-01',
            'endDate': None
         },
         (
            'set_drinking_fountains_as_open',
            {
               'start_date': '2026-07-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'startDate': '2026-07-01',
            'endDate': None
         }
      )
   ]
)
def test_console_mutation_endpoints_map_payloads_and_success_responses(
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

   assert 'error' not in result


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-restaurant-opening-schedule',
         {
            'restaurant': 'Africa Restaurant',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_restaurant_opening_schedule',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'restaurant': 'Africa Restaurant',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      ),
      (
         '/set-gift-shop-opening-schedule',
         {
            'giftShop': 'Zootique',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_gift_shop_opening_schedule',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'gift_shop': 'Zootique',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      ),
      (
         '/set-attraction-opening-schedule',
         {
            'attraction': 'Conservation Carousel',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_attraction_opening_schedule',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'attraction': 'Conservation Carousel',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      )
   ]
)
def test_weekly_schedule_endpoints_map_payloads_and_success_responses(
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
   assert result[ 'success' ] is True

   for key, value in response_subset.items():
      assert result[ key ] == value

   assert result[ 'monday' ] is True
   assert result[ 'tuesday' ] is False
   assert result[ 'wednesday' ] is True
   assert result[ 'thursday' ] is False
   assert result[ 'friday' ] is True
   assert result[ 'saturday' ] is False
   assert result[ 'sunday' ] is True
   assert result[ 'holidaysOnly' ] is False
   assert result[ 'message' ] == 'Schedule.'


@pytest.mark.parametrize(
   'path, body_key, item_name, expected_method, response_key',
   [
      (
         '/replace-restaurant-opening-schedule-overlaps',
         'restaurant',
         'Africa Restaurant',
         'replace_restaurant_opening_schedule_overlaps',
         'restaurant'
      ),
      (
         '/trim-restaurant-opening-schedule-overlaps',
         'restaurant',
         'Africa Restaurant',
         'trim_restaurant_opening_schedule_overlaps',
         'restaurant'
      ),
      (
         '/replace-gift-shop-opening-schedule-overlaps',
         'giftShop',
         'Zootique',
         'replace_gift_shop_opening_schedule_overlaps',
         'gift_shop'
      ),
      (
         '/trim-gift-shop-opening-schedule-overlaps',
         'giftShop',
         'Zootique',
         'trim_gift_shop_opening_schedule_overlaps',
         'gift_shop'
      ),
      (
         '/replace-attraction-opening-schedule-overlaps',
         'attraction',
         'Conservation Carousel',
         'replace_attraction_opening_schedule_overlaps',
         'attraction'
      ),
      (
         '/trim-attraction-opening-schedule-overlaps',
         'attraction',
         'Conservation Carousel',
         'trim_attraction_opening_schedule_overlaps',
         'attraction'
      )
   ]
)
def test_schedule_overlap_resolution_endpoints_map_payloads(
      stub_database: type[ StubZooControllers ],
      path: str,
      body_key: str,
      item_name: str,
      expected_method: str,
      response_key: str ) -> None:
   body = {
      body_key: item_name,
      'scheduleStartDate': '2026-06-01',
      'scheduleEndDate': '2026-06-30',
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
      'holidaysOnly': False,
      'message': 'Schedule.'
   }
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         expected_method,
         {
            response_key: item_name,
            'start_date': '2026-06-01',
            'end_date': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidays_only': False,
            'message': 'Schedule.'
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ response_key ] == item_name
   assert result[ 'scheduleStartDate' ] == '2026-06-01'
   assert result[ 'scheduleEndDate' ] == '2026-06-30'


@pytest.mark.parametrize(
   'path, body_key, item_name',
   [
      (
         '/set-restaurant-opening-schedule',
         'restaurant',
         'Africa Restaurant'
      ),
      (
         '/set-gift-shop-opening-schedule',
         'giftShop',
         'Zootique'
      ),
      (
         '/set-attraction-opening-schedule',
         'attraction',
         'Conservation Carousel'
      )
   ]
)
def test_opening_schedule_overlap_failure_returns_error_type(
      stub_database: type[ StubZooControllers ],
      path: str,
      body_key: str,
      item_name: str ) -> None:
   StubZooControllers.default_success = False
   handler = make_handler(
      path,
      {
         body_key: item_name,
         'scheduleStartDate': '2026-06-01',
         'scheduleEndDate': '2026-06-30',
         'monday': True,
         'tuesday': False,
         'wednesday': True,
         'thursday': False,
         'friday': True,
         'saturday': False,
         'sunday': True,
         'holidaysOnly': False,
         'message': 'Schedule.'
      } )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'errorType' ] == 'overlappingSchedule'


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'set_current_zoomobile_route',
            {
               'route': 'winter',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/set-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'mondayTime': '10:00',
            'tuesdayTime': None,
            'wednesdayTime': '11:00',
            'thursdayTime': None,
            'fridayTime': '12:00',
            'saturdayTime': None,
            'sundayTime': None,
            'message': 'Schedule.'
         },
         (
            'set_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday_time': '10:00',
               'tuesday_time': None,
               'wednesday_time': '11:00',
               'thursday_time': None,
               'friday_time': '12:00',
               'saturday_time': None,
               'sunday_time': None,
               'message': 'Schedule.'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'mondayTime': '10:00',
            'wednesdayTime': '11:00',
            'fridayTime': '12:00'
         }
      ),
      (
         '/end-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         },
         (
            'end_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'schedule_end_date': '2026-06-30'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/cancel-guardians-talk-occurrence',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00'
         },
         (
            'cancel_guardians_talk_occurrence',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'date': '2026-06-15',
               'time': '10:00'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00'
         }
      ),
      (
         '/set-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '14:00',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'message': 'Schedule.'
         },
         (
            'set_wild_encounter_schedule',
            {
               'wild_encounter_name': 'African Rainforest',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'encounter_time': '14:00',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'message': 'Schedule.'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '14:00'
         }
      ),
      (
         '/end-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30'
         },
         (
            'end_wild_encounter_schedule',
            {
               'wild_encounter_name': 'African Rainforest',
               'schedule_end_date': '2026-06-30'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         },
         (
            'cancel_wild_encounter_occurrence',
            {
               'wild_encounter_name': 'African Rainforest',
               'date': '2026-06-15',
               'time': '14:00'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         }
      )
   ]
)
def test_schedule_and_occurrence_endpoints_map_payloads_and_success_responses(
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
   assert result[ 'success' ] is True

   for key, value in response_subset.items():
      assert result[ key ] == value

   assert 'error' not in result


@pytest.mark.parametrize(
   'path, body, expected_error',
   [
         (
            '/set-animal-off-display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'viewingScope': 'all'
            },
            'No animal found with species "African Lion".'
         ),
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna'
         },
         'Could not set "Africa Savanna" as closed.'
      ),
      (
         '/set-restaurant-opening-schedule',
         {
            'restaurant': 'Africa Restaurant'
         },
         'Could not set opening schedule for "Africa Restaurant".'
      ),
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter'
         },
         'Could not set Zoomobile route to "winter".'
      ),
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         },
         'Could not cancel "African Rainforest" on 2026-06-15 at 14:00.'
      )
   ]
)
def test_console_mutation_endpoints_return_error_when_database_returns_false(
      stub_database: type[ StubZooControllers ],
      path: str,
      body: dict[ str, Any ],
      expected_error: str ) -> None:
   StubZooControllers.default_success = False
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'error' ] == expected_error
