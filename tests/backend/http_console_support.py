from __future__ import annotations

from typing import Any

from http_support import make_handler
from http_support import response_json
from http_support import StubZooControllers

import api.server as server


def assert_console_mutation_success(
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

   assert result.get( 'error' ) is None


def assert_weekly_schedule_success(
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


def assert_schedule_overlap_resolution(
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


def assert_opening_schedule_overlap_failure(
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


def assert_console_mutation_failure(
      path: str,
      body: dict[ str, Any ],
      expected_api_error_type: str,
      expected_api_error_params: dict[ str, Any ] | None = None ) -> None:
   StubZooControllers.default_success = False
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == expected_api_error_type

   if expected_api_error_params is None:
      assert 'apiErrorParams' not in result
   else:
      assert result.get( 'apiErrorParams' ) == expected_api_error_params
