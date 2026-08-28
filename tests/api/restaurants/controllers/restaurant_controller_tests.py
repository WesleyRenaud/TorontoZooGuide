from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_restaurant_coordinator import StubRestaurantCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.models.restaurant import Restaurant
import api.request_connection_provider as request_connection
from api.restaurants.controllers.restaurant_controller import RestaurantController
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.types import Types


RESTAURANT_NAME = 'Africa Restaurant'
OTHER_RESTAURANT_NAME = 'Beavertails'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
SCHEDULE_MESSAGE = 'Schedule.'


def _sample_restaurant() -> Restaurant:
   return Restaurant(
      name=RESTAURANT_NAME,
      location='Africa',
      sub_location=None,
      likelihood=100,
      is_closed=False )


def _weekly_schedule_body() -> dict[ str, object ]:
   return {
      'restaurant': RESTAURANT_NAME,
      'scheduleStartDate': SCHEDULE_START_DATE,
      'scheduleEndDate': SCHEDULE_END_DATE,
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
      'holidaysOnly': False,
      'message': SCHEDULE_MESSAGE,
   }


def _weekly_schedule_call() -> dict[ str, object ]:
   return {
      'restaurant': RESTAURANT_NAME,
      'start_date': SCHEDULE_START_DATE,
      'end_date': SCHEDULE_END_DATE,
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
      'holidays_only': False,
      'message': SCHEDULE_MESSAGE,
   }


@pytest.fixture
def stub_restaurant_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubRestaurantCoordinator:
   StubRestaurantCoordinator.instances = []
   StubRestaurantCoordinator.default_success = True
   stub = StubRestaurantCoordinator(
      restaurant_names=[ RESTAURANT_NAME, OTHER_RESTAURANT_NAME ],
      restaurants=[ _sample_restaurant() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubRestaurantCoordinator.instances:
         StubRestaurantCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, RestaurantCoordinator, stub )

   return stub


def Test_GetRestaurants_TestHttpRequest_ExpectMapsVisitDateAndReturnsRestaurants(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler(
      '/get-restaurants',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'includeClosedRestaurants': True,
         'restaurantsToInclude': [ RESTAURANT_NAME ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'restaurants' ] == [ _sample_restaurant().to_dict() ]
   assert stub_restaurant_coordinator.calls == [
      (
         'get_restaurants',
         {
            'day': VISIT_DAY,
            'month': VISIT_MONTH,
            'year': VISIT_YEAR,
            'include_closed_restaurants': True,
            'restaurants_to_include': [ RESTAURANT_NAME ],
         }
      )
   ]


def Test_GetRestaurantNames_TestDirectCall_ExpectWritesRestaurantNamesFromCoordinator(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   RestaurantController.get_restaurant_names( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'restaurants': [ RESTAURANT_NAME, OTHER_RESTAURANT_NAME ],
   }


def Test_SetRestaurantClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler(
      '/set-restaurant-closed',
      {
         'restaurant': RESTAURANT_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_restaurant_coordinator.calls == [
      (
         'set_restaurant_as_closed',
         {
            'restaurant': RESTAURANT_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetRestaurantClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   StubRestaurantCoordinator.default_success = False
   handler = make_handler( '/set-restaurant-closed', { 'restaurant': RESTAURANT_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'


def Test_SetRestaurantClosureOverride_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler(
      '/set-restaurant-closure-override',
      {
         'restaurant': RESTAURANT_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restaurant_coordinator.calls == [
      (
         'set_restaurant_closure_override',
         {
            'restaurant': RESTAURANT_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetRestaurantClosureOverride_TestHttpRequest_ExpectCouldNotCreateClosureOverrideApiError(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   StubRestaurantCoordinator.default_success = False
   handler = make_handler(
      '/set-restaurant-closure-override',
      { 'restaurant': RESTAURANT_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotCreateClosureOverride'


def Test_SetRestaurantOpeningSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler( '/set-restaurant-opening-schedule', _weekly_schedule_body() )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restaurant_coordinator.calls == [
      ( 'set_restaurant_opening_schedule', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_SetRestaurantOpeningSchedule_TestHttpRequest_ExpectOverlappingScheduleApiError(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   StubRestaurantCoordinator.default_success = False
   handler = make_handler( '/set-restaurant-opening-schedule', _weekly_schedule_body() )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetOpeningSchedule'
   assert result[ 'errorType' ] == 'overlappingSchedule'


def Test_ReplaceRestaurantOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler(
      '/replace-restaurant-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restaurant_coordinator.calls == [
      ( 'replace_restaurant_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_ReplaceRestaurantOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotReplaceApiError(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   StubRestaurantCoordinator.default_success = False
   handler = make_handler(
      '/replace-restaurant-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotReplaceOpeningScheduleOverlaps'


def Test_TrimRestaurantOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   handler = make_handler(
      '/trim-restaurant-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_restaurant_coordinator.calls == [
      ( 'trim_restaurant_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_TrimRestaurantOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotTrimApiError(
      stub_restaurant_coordinator: StubRestaurantCoordinator ) -> None:
   StubRestaurantCoordinator.default_success = False
   handler = make_handler(
      '/trim-restaurant-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotTrimOpeningScheduleOverlaps'
