from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_guardians_coordinator import StubGuardiansCoordinator
import pytest

from api import database_connection_provider as connection
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
import api.http_request_handler as server
from api.models.guardians_talk import GuardiansTalk
from api.models.scheduled_occurrence import ScheduledOccurrence
import api.request_connection_provider as request_connection
from api.shared.api_operation_failure import ApiOperationFailure
from api.shared.enums.api_error_type import ApiErrorType
from api.types import Types


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
OCCURRENCE_DATE = '2026-06-15'
ADD_OCCURRENCE_DATE = '2026-06-20'

GUARDIANS_TALK_SCHEDULE_ROWS = [
   {
      'time': '10:00',
      'monday': True,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
   },
   {
      'time': '11:00',
      'monday': False,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': False,
      'saturday': False,
      'sunday': False,
   },
   {
      'time': '12:00',
      'monday': False,
      'tuesday': False,
      'wednesday': False,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': False,
   },
]

GUARDIANS_TALK_SCHEDULE_BODY = {
   'talk': TALK_NAME,
   'location': TALK_LOCATION,
   'startDate': SCHEDULE_START_DATE,
   'endDate': SCHEDULE_END_DATE,
   'scheduleRows': GUARDIANS_TALK_SCHEDULE_ROWS,
   'message': 'Schedule.',
}


def _sample_guardians_talk( *, start_time: str = '10:00 AM' ) -> GuardiansTalk:
   return GuardiansTalk(
      name=TALK_NAME,
      location=TALK_LOCATION,
      x_coord=1.0,
      y_coord=2.0,
      start_time=start_time )


def _sample_occurrence() -> ScheduledOccurrence:
   return ScheduledOccurrence( date=OCCURRENCE_DATE, time='10:00 AM' )


@pytest.fixture
def stub_guardians_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubGuardiansCoordinator:
   StubGuardiansCoordinator.instances = []
   StubGuardiansCoordinator.default_success = True
   StubGuardiansCoordinator.default_failure = None
   stub = StubGuardiansCoordinator(
      guardians_talks=[
         _sample_guardians_talk( start_time='10:00 AM' ),
         _sample_guardians_talk( start_time='11:00 AM' ),
      ],
      guardians_talk_locations=[ TALK_LOCATION ],
      guardians_talk_names=[ TALK_NAME ],
      guardians_talk_names_at_location=[ TALK_NAME ],
      guardians_talk_occurrences=[ _sample_occurrence() ],
      guardians_talk_schedule_times=[ '10:00 AM', '11:00 AM' ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubGuardiansCoordinator.instances:
         StubGuardiansCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, GuardiansCoordinator, stub )

   return stub


def Test_GetGuardiansTalks_TestHttpRequest_ExpectMapsVisitDateAndCollapsesSchedule(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/get-guardians-talks',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_guardians_coordinator.calls == [
      (
         'get_guardians_talk_schedule',
         {
            'month': VISIT_MONTH,
            'day': VISIT_DAY,
            'year': VISIT_YEAR,
         }
      )
   ]
   assert len( result[ 'guardians_talks' ] ) == 1
   assert result[ 'guardians_talks' ][ 0 ][ 'name' ] == TALK_NAME
   assert result[ 'guardians_talks' ][ 0 ][ 'times' ] == [ '10:00 AM', '11:00 AM' ]


def Test_GetGuardiansTalks_TestHttpRequest_ExpectOmittedYearPassesThrough(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/get-guardians-talks',
      {
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.errors == []
   assert (
      'get_guardians_talk_schedule',
      {
         'month': VISIT_MONTH,
         'day': VISIT_DAY,
         'year': None,
      },
   ) in stub_guardians_coordinator.calls


def Test_GetGuardiansTalkLocations_TestHttpRequest_ExpectReturnsLocations(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler( '/get-guardians-talk-locations', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'guardians_talk_locations' ] == [ TALK_LOCATION ]


def Test_GetGuardiansTalkNames_TestHttpRequest_ExpectReturnsTalkNames(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler( '/get-guardians-talk-names', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'guardians_talks' ] == [ TALK_NAME ]


def Test_GetGuardiansTalkNamesAtLocation_TestHttpRequest_ExpectMapsLocation(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/get-guardians-talk-names-at-location',
      { 'location': TALK_LOCATION }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_guardians_coordinator.calls[ -1 ] == (
      'get_guardians_talk_names_at_location',
      { 'location': TALK_LOCATION },
   )
   assert result[ 'guardians_talks' ] == [ TALK_NAME ]


def Test_GetGuardiansTalkOccurrences_TestHttpRequest_ExpectMapsTalkAndLocation(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/get-guardians-talk-occurrences',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'talk' ] == TALK_NAME
   assert result[ 'location' ] == TALK_LOCATION
   assert result[ 'occurrences' ] == [ _sample_occurrence().to_dict() ]


def Test_SetGuardiansTalkSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler( '/set-guardians-talk-schedule', GUARDIANS_TALK_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_guardians_coordinator.calls[ -1 ] == (
      'set_guardians_talk_schedule',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'start_date': SCHEDULE_START_DATE,
         'end_date': SCHEDULE_END_DATE,
         'schedule_rows': GUARDIANS_TALK_SCHEDULE_ROWS,
         'message': 'Schedule.',
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'talk' ] == TALK_NAME
   assert result[ 'location' ] == TALK_LOCATION
   assert result[ 'startDate' ] == SCHEDULE_START_DATE
   assert result[ 'endDate' ] == SCHEDULE_END_DATE


def Test_SetGuardiansTalkSchedule_TestHttpRequest_ExpectOverlappingScheduleErrorType(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   StubGuardiansCoordinator.default_success = False
   handler = make_handler( '/set-guardians-talk-schedule', GUARDIANS_TALK_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'errorType' ] == 'overlappingSchedule'
   assert result[ 'apiErrorType' ] == 'couldNotSetGuardiansTalkSchedule'


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-guardians-talk-schedule-overlaps',
         'replace_guardians_talk_schedule_overlaps'
      ),
      (
         '/trim-guardians-talk-schedule-overlaps',
         'trim_guardians_talk_schedule_overlaps'
      ),
   ]
)
def Test_GuardiansTalkScheduleOverlapResolution_TestHttpRequest_ExpectMapsPayload(
      stub_guardians_coordinator: StubGuardiansCoordinator,
      path: str,
      expected_method: str ) -> None:
   handler = make_handler( path, GUARDIANS_TALK_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_guardians_coordinator.calls[ -1 ] == (
      expected_method,
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'start_date': SCHEDULE_START_DATE,
         'end_date': SCHEDULE_END_DATE,
         'schedule_rows': GUARDIANS_TALK_SCHEDULE_ROWS,
         'message': 'Schedule.',
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'talk' ] == TALK_NAME
   assert result[ 'location' ] == TALK_LOCATION


def Test_GetGuardiansTalkScheduleTimes_TestHttpRequest_ExpectMapsTalkAndLocation(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/get-guardians-talk-schedule-times',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'talk' ] == TALK_NAME
   assert result[ 'location' ] == TALK_LOCATION
   assert result[ 'times' ] == [ '10:00 AM', '11:00 AM' ]


def Test_EndGuardiansTalkSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/end-guardians-talk-schedule',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'endDate': SCHEDULE_END_DATE,
         'times': [ '10:00' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_guardians_coordinator.calls[ -1 ] == (
      'end_guardians_talk_schedule',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'schedule_end_date': SCHEDULE_END_DATE,
         'talk_times': [ '10:00' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'endDate' ] == SCHEDULE_END_DATE


def Test_EndGuardiansTalkSchedule_TestHttpRequest_ExpectCouldNotEndScheduleApiError(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   StubGuardiansCoordinator.default_success = False
   handler = make_handler(
      '/end-guardians-talk-schedule',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'endDate': SCHEDULE_END_DATE,
         'times': [ '10:00' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotEndGuardiansTalkSchedule'


def Test_CancelGuardiansTalkOccurrence_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/cancel-guardians-talk-occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': OCCURRENCE_DATE,
         'times': [ '10:00 AM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_guardians_coordinator.calls[ -1 ] == (
      'cancel_guardians_talk_occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': OCCURRENCE_DATE,
         'talk_times': [ '10:00 AM' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'date' ] == OCCURRENCE_DATE
   assert result[ 'times' ] == [ '10:00 AM' ]


def Test_CancelGuardiansTalkOccurrence_TestHttpRequest_ExpectCouldNotCancelApiError(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   StubGuardiansCoordinator.default_success = False
   handler = make_handler(
      '/cancel-guardians-talk-occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': OCCURRENCE_DATE,
         'times': [ '10:00 AM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotCancelGuardiansTalkOccurrence'


def Test_AddGuardiansTalkOccurrence_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   handler = make_handler(
      '/add-guardians-talk-occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': ADD_OCCURRENCE_DATE,
         'times': [ '3:00 PM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_guardians_coordinator.calls[ -1 ] == (
      'add_guardians_talk_occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': ADD_OCCURRENCE_DATE,
         'talk_times': [ '3:00 PM' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'date' ] == ADD_OCCURRENCE_DATE
   assert result[ 'times' ] == [ '3:00 PM' ]


def Test_AddGuardiansTalkOccurrence_TestHttpRequest_ExpectAppliesCoordinatorFailure(
      stub_guardians_coordinator: StubGuardiansCoordinator ) -> None:
   StubGuardiansCoordinator.default_failure = ApiOperationFailure(
      error_type=ApiErrorType.GUARDIANS_TALK_OCCURRENCE_ALREADY_EXISTS,
      params={
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': ADD_OCCURRENCE_DATE,
         'talkTime': '3:00 PM',
      } )
   handler = make_handler(
      '/add-guardians-talk-occurrence',
      {
         'talk': TALK_NAME,
         'location': TALK_LOCATION,
         'date': ADD_OCCURRENCE_DATE,
         'times': [ '3:00 PM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'guardiansTalkOccurrenceAlreadyExists'
