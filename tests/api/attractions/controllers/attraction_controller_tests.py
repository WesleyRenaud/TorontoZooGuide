from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_attraction_coordinator import StubAttractionCoordinator
import pytest

from api import database_connection_provider as connection
from api.attractions.controllers.attraction_controller import AttractionController
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from api.attractions.scheduling.attraction_hours_time_bounds import AttractionHoursTimeBounds
import api.http_request_handler as server
from api.models.attraction import Attraction
import api.request_connection_provider as request_connection
from api.types import Types


ATTRACTION_NAME = 'Conservation Carousel'
OTHER_ATTRACTION_NAME = 'Zoomobile'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
SCHEDULE_MESSAGE = 'Schedule.'
WEEKDAY_START_TIME = '10:00 AM'
WEEKDAY_END_TIME = '4:00 PM'
WEEKEND_START_TIME = '11:00 AM'
WEEKEND_END_TIME = '5:00 PM'
WEEKDAY_OPERATING_DATE = '2026-06-15'
WEEKEND_OPERATING_DATE = '2026-06-20'


def _sample_attraction() -> Attraction:
   return Attraction(
      name=ATTRACTION_NAME,
      free_with_admission=True,
      likelihood=100,
      is_closed=False,
      open_time=WEEKDAY_START_TIME,
      close_time=WEEKDAY_END_TIME )


def _hours_time_bounds() -> AttractionHoursScheduleTimeBounds:
   return AttractionHoursScheduleTimeBounds(
      weekday=AttractionHoursTimeBounds(
         open_time='09:30',
         close_time='18:00',
         operating_date=WEEKDAY_OPERATING_DATE ),
      weekend_holiday=AttractionHoursTimeBounds(
         open_time='09:30',
         close_time='19:00',
         operating_date=WEEKEND_OPERATING_DATE ) )


def _weekly_schedule_body() -> dict[ str, object ]:
   return {
      'attraction': ATTRACTION_NAME,
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
      'attraction': ATTRACTION_NAME,
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


def _hours_schedule_body() -> dict[ str, object ]:
   return {
      'attraction': ATTRACTION_NAME,
      'scheduleStartDate': SCHEDULE_START_DATE,
      'scheduleEndDate': SCHEDULE_END_DATE,
      'weekdayStartTime': WEEKDAY_START_TIME,
      'weekdayEndTime': WEEKDAY_END_TIME,
      'weekendHolidayStartTime': WEEKEND_START_TIME,
      'weekendHolidayEndTime': WEEKEND_END_TIME,
   }


def _hours_schedule_call() -> dict[ str, object ]:
   return {
      'attraction': ATTRACTION_NAME,
      'start_date': SCHEDULE_START_DATE,
      'end_date': SCHEDULE_END_DATE,
      'weekday_start_time': WEEKDAY_START_TIME,
      'weekday_end_time': WEEKDAY_END_TIME,
      'weekend_holiday_start_time': WEEKEND_START_TIME,
      'weekend_holiday_end_time': WEEKEND_END_TIME,
   }


@pytest.fixture
def stub_attraction_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubAttractionCoordinator:
   StubAttractionCoordinator.instances = []
   StubAttractionCoordinator.default_success = True
   StubAttractionCoordinator.raise_time_bounds_error = False
   StubAttractionCoordinator.raise_hours_schedule_error = False
   stub = StubAttractionCoordinator(
      attraction_names=[ ATTRACTION_NAME, OTHER_ATTRACTION_NAME ],
      attractions=[ _sample_attraction() ],
      hours_time_bounds=_hours_time_bounds() )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubAttractionCoordinator.instances:
         StubAttractionCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, AttractionCoordinator, stub )

   return stub


def Test_GetAttractions_TestHttpRequest_ExpectMapsVisitDateAndReturnsAttractions(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/get-attractions',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'includeClosedAttractions': True,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'attractions' ] == [ _sample_attraction().to_dict() ]
   assert stub_attraction_coordinator.calls == [
      (
         'get_attractions',
         {
            'day': VISIT_DAY,
            'month': VISIT_MONTH,
            'year': VISIT_YEAR,
            'include_closed_attractions': True,
         }
      )
   ]


def Test_GetAttractionNames_TestDirectCall_ExpectWritesAttractionNamesFromCoordinator(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   AttractionController.get_attraction_names( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'attractions': [ ATTRACTION_NAME, OTHER_ATTRACTION_NAME ],
   }
   assert stub_attraction_coordinator.calls == [ ( 'get_attraction_names', {} ) ]


def Test_SetAttractionClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/set-attraction-closed',
      {
         'attraction': ATTRACTION_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      (
         'set_attraction_as_closed',
         {
            'attraction': ATTRACTION_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'attraction' ] == ATTRACTION_NAME
   assert result.get( 'error' ) is None


def Test_SetAttractionClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/set-attraction-closed',
      { 'attraction': ATTRACTION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'
   assert result.get( 'apiErrorParams' ) == { 'name': ATTRACTION_NAME }


def Test_SetAttractionClosureOverride_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/set-attraction-closure-override',
      {
         'attraction': ATTRACTION_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      (
         'set_attraction_closure_override',
         {
            'attraction': ATTRACTION_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetAttractionClosureOverride_TestHttpRequest_ExpectCouldNotCreateClosureOverrideApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/set-attraction-closure-override',
      { 'attraction': ATTRACTION_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotCreateClosureOverride'


def Test_SetAttractionOpeningSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/set-attraction-opening-schedule',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'set_attraction_opening_schedule', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True
   assert result[ 'scheduleStartDate' ] == SCHEDULE_START_DATE


def Test_SetAttractionOpeningSchedule_TestHttpRequest_ExpectOverlappingScheduleApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/set-attraction-opening-schedule',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetOpeningSchedule'
   assert result[ 'errorType' ] == 'overlappingSchedule'


def Test_ReplaceAttractionOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/replace-attraction-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'replace_attraction_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_ReplaceAttractionOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotReplaceApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/replace-attraction-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotReplaceOpeningScheduleOverlaps'


def Test_TrimAttractionOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/trim-attraction-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'trim_attraction_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_TrimAttractionOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotTrimApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/trim-attraction-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotTrimOpeningScheduleOverlaps'


def Test_GetAttractionHoursScheduleTimeBounds_TestHttpRequest_ExpectNormalizedBoundsResponse(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/get-attraction-hours-schedule-time-bounds',
      {
         'scheduleStartDate': SCHEDULE_START_DATE,
         'scheduleEndDate': SCHEDULE_END_DATE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is True
   assert result[ 'weekday' ] == {
      'openTime': '9:30 AM',
      'closeTime': '6:00 PM',
      'operatingDate': WEEKDAY_OPERATING_DATE,
   }
   assert result[ 'weekendHoliday' ] == {
      'openTime': '9:30 AM',
      'closeTime': '7:00 PM',
      'operatingDate': WEEKEND_OPERATING_DATE,
   }


def Test_GetAttractionHoursScheduleTimeBounds_TestHttpRequest_ExpectCouldNotResolveBoundsApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.raise_time_bounds_error = True
   handler = make_handler(
      '/get-attraction-hours-schedule-time-bounds',
      {
         'scheduleStartDate': SCHEDULE_START_DATE,
         'scheduleEndDate': SCHEDULE_END_DATE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotResolveAttractionHoursTimeBounds'


def Test_SetAttractionHoursSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/set-attraction-hours-schedule',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'set_attraction_hours_schedule', _hours_schedule_call() )
   ]
   assert result[ 'success' ] is True
   assert result[ 'weekdayStartTime' ] == WEEKDAY_START_TIME


def Test_SetAttractionHoursSchedule_TestHttpRequest_ExpectInvalidAttractionHoursApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.raise_hours_schedule_error = True
   handler = make_handler(
      '/set-attraction-hours-schedule',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'invalidAttractionHours'


def Test_SetAttractionHoursSchedule_TestHttpRequest_ExpectOverlappingScheduleApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/set-attraction-hours-schedule',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotSetAttractionHours'
   assert result[ 'errorType' ] == 'overlappingSchedule'


def Test_ReplaceAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/replace-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'replace_attraction_hours_schedule_overlaps', _hours_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_ReplaceAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectInvalidAttractionHoursApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.raise_hours_schedule_error = True
   handler = make_handler(
      '/replace-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'invalidAttractionHours'


def Test_ReplaceAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectCouldNotReplaceApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/replace-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotReplaceAttractionHoursOverlaps'


def Test_TrimAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   handler = make_handler(
      '/trim-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_attraction_coordinator.calls == [
      ( 'trim_attraction_hours_schedule_overlaps', _hours_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_TrimAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectInvalidAttractionHoursApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.raise_hours_schedule_error = True
   handler = make_handler(
      '/trim-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'invalidAttractionHours'


def Test_TrimAttractionHoursScheduleOverlaps_TestHttpRequest_ExpectCouldNotTrimApiError(
      stub_attraction_coordinator: StubAttractionCoordinator ) -> None:
   StubAttractionCoordinator.default_success = False
   handler = make_handler(
      '/trim-attraction-hours-schedule-overlaps',
      _hours_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotTrimAttractionHoursOverlaps'
