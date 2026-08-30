from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_wild_encounter_coordinator import StubWildEncounterCoordinator
import pytest

from api import database_connection_provider as connection
import api.http_request_handler as server
from api.models.scheduled_occurrence import ScheduledOccurrence
from api.models.wild_encounter import WildEncounter
import api.request_connection_provider as request_connection
from api.types import Types
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


WILD_ENCOUNTER_NAME = 'African Rainforest'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
OCCURRENCE_DATE = '2026-06-15'

WILD_ENCOUNTER_SCHEDULE_ROWS = [
   {
      'time': '2:00 PM',
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
   },
   {
      'time': '3:30 PM',
      'monday': False,
      'tuesday': True,
      'wednesday': False,
      'thursday': False,
      'friday': False,
      'saturday': True,
      'sunday': False,
   },
]

WILD_ENCOUNTER_SCHEDULE_BODY = {
   'wildEncounter': WILD_ENCOUNTER_NAME,
   'startDate': SCHEDULE_START_DATE,
   'endDate': SCHEDULE_END_DATE,
   'scheduleRows': WILD_ENCOUNTER_SCHEDULE_ROWS,
   'message': 'Schedule.',
}

WILD_ENCOUNTER_SCHEDULE_BODY_SIMPLE = {
   'wildEncounter': WILD_ENCOUNTER_NAME,
   'startDate': SCHEDULE_START_DATE,
   'endDate': SCHEDULE_END_DATE,
   'scheduleRows': [
      {
         'time': '2:00 PM',
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ],
   'message': 'Schedule.',
}


def _sample_wild_encounter( *, start_time: str = '2:00 PM' ) -> WildEncounter:
   return WildEncounter(
      name=WILD_ENCOUNTER_NAME,
      meeting_spot='Rainforest Pavilion',
      link='https://www.torontozoo.com/wild-encounters/african-rainforest',
      start_time=start_time,
      x_coord=3.0,
      y_coord=4.0 )


def _sample_occurrence() -> ScheduledOccurrence:
   return ScheduledOccurrence( date=OCCURRENCE_DATE, time='2:00 PM' )


@pytest.fixture
def stub_wild_encounter_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubWildEncounterCoordinator:
   StubWildEncounterCoordinator.instances = []
   StubWildEncounterCoordinator.default_success = True
   stub = StubWildEncounterCoordinator(
      wild_encounters=[
         _sample_wild_encounter( start_time='2:00 PM' ),
         _sample_wild_encounter( start_time='3:30 PM' ),
      ],
      wild_encounter_names=[ WILD_ENCOUNTER_NAME ],
      wild_encounter_occurrences=[ _sample_occurrence() ],
      wild_encounter_schedule_times=[ '2:00 PM', '3:30 PM' ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubWildEncounterCoordinator.instances:
         StubWildEncounterCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, WildEncounterCoordinator, stub )

   return stub


def Test_GetWildEncounters_TestHttpRequest_ExpectMapsVisitDateAndCollapsesSchedule(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler(
      '/get-wild-encounters',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_wild_encounter_coordinator.calls == [
      (
         'get_available_wild_encounters',
         {
            'month': VISIT_MONTH,
            'day': VISIT_DAY,
            'year': VISIT_YEAR,
         }
      )
   ]
   assert len( result[ 'wild_encounters' ] ) == 1
   assert result[ 'wild_encounters' ][ 0 ][ 'name' ] == WILD_ENCOUNTER_NAME
   assert result[ 'wild_encounters' ][ 0 ][ 'times' ] == [ '2:00 PM', '3:30 PM' ]


def Test_GetWildEncounterNames_TestHttpRequest_ExpectReturnsEncounterNames(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler( '/get-wild-encounter-names', {} )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'wild_encounters' ] == [ WILD_ENCOUNTER_NAME ]


def Test_GetWildEncounterOccurrences_TestHttpRequest_ExpectMapsWildEncounter(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler(
      '/get-wild-encounter-occurrences',
      { 'wildEncounter': WILD_ENCOUNTER_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_wild_encounter_coordinator.calls[ -1 ] == (
      'get_wild_encounter_occurrences',
      { 'wild_encounter_name': WILD_ENCOUNTER_NAME },
   )
   assert result[ 'wildEncounter' ] == WILD_ENCOUNTER_NAME
   assert result[ 'occurrences' ] == [ _sample_occurrence().to_dict() ]


def Test_SetWildEncounterSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler( '/set-wild-encounter-schedule', WILD_ENCOUNTER_SCHEDULE_BODY )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_wild_encounter_coordinator.calls[ -1 ] == (
      'set_wild_encounter_schedule',
      {
         'wild_encounter_name': WILD_ENCOUNTER_NAME,
         'start_date': SCHEDULE_START_DATE,
         'end_date': SCHEDULE_END_DATE,
         'message': 'Schedule.',
         'schedule_rows': WILD_ENCOUNTER_SCHEDULE_ROWS,
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'wildEncounter' ] == WILD_ENCOUNTER_NAME
   assert result[ 'startDate' ] == SCHEDULE_START_DATE
   assert result[ 'endDate' ] == SCHEDULE_END_DATE


def Test_SetWildEncounterSchedule_TestHttpRequest_ExpectOverlappingScheduleErrorType(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   StubWildEncounterCoordinator.default_success = False
   handler = make_handler(
      '/set-wild-encounter-schedule',
      WILD_ENCOUNTER_SCHEDULE_BODY_SIMPLE )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'errorType' ] == 'overlappingSchedule'
   assert result[ 'apiErrorType' ] == 'couldNotSetWildEncounterSchedule'


@pytest.mark.parametrize(
   'path, expected_method',
   [
      (
         '/replace-wild-encounter-schedule-overlaps',
         'replace_wild_encounter_schedule_overlaps'
      ),
      (
         '/trim-wild-encounter-schedule-overlaps',
         'trim_wild_encounter_schedule_overlaps'
      ),
   ]
)
def Test_WildEncounterScheduleOverlapResolution_TestHttpRequest_ExpectMapsPayload(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator,
      path: str,
      expected_method: str ) -> None:
   handler = make_handler( path, WILD_ENCOUNTER_SCHEDULE_BODY_SIMPLE )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert stub_wild_encounter_coordinator.calls[ -1 ] == (
      expected_method,
      {
         'wild_encounter_name': WILD_ENCOUNTER_NAME,
         'start_date': SCHEDULE_START_DATE,
         'end_date': SCHEDULE_END_DATE,
         'message': 'Schedule.',
         'schedule_rows': WILD_ENCOUNTER_SCHEDULE_BODY_SIMPLE[ 'scheduleRows' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'wildEncounter' ] == WILD_ENCOUNTER_NAME


def Test_GetWildEncounterScheduleTimes_TestHttpRequest_ExpectMapsWildEncounter(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler(
      '/get-wild-encounter-schedule-times',
      { 'wildEncounter': WILD_ENCOUNTER_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'wildEncounter' ] == WILD_ENCOUNTER_NAME
   assert result[ 'times' ] == [ '2:00 PM', '3:30 PM' ]


def Test_EndWildEncounterSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler(
      '/end-wild-encounter-schedule',
      {
         'wildEncounter': WILD_ENCOUNTER_NAME,
         'endDate': SCHEDULE_END_DATE,
         'times': [ '14:00' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_wild_encounter_coordinator.calls[ -1 ] == (
      'end_wild_encounter_schedule',
      {
         'wild_encounter_name': WILD_ENCOUNTER_NAME,
         'schedule_end_date': SCHEDULE_END_DATE,
         'encounter_times': [ '14:00' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'endDate' ] == SCHEDULE_END_DATE
   assert result[ 'times' ] == [ '14:00' ]


def Test_EndWildEncounterSchedule_TestHttpRequest_ExpectCouldNotEndScheduleApiError(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   StubWildEncounterCoordinator.default_success = False
   handler = make_handler(
      '/end-wild-encounter-schedule',
      {
         'wildEncounter': WILD_ENCOUNTER_NAME,
         'endDate': SCHEDULE_END_DATE,
         'times': [ '14:00' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotEndWildEncounterSchedule'


def Test_CancelWildEncounterOccurrence_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   handler = make_handler(
      '/cancel-wild-encounter-occurrence',
      {
         'wildEncounter': WILD_ENCOUNTER_NAME,
         'date': OCCURRENCE_DATE,
         'times': [ '2:00 PM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_wild_encounter_coordinator.calls[ -1 ] == (
      'cancel_wild_encounter_occurrence',
      {
         'wild_encounter_name': WILD_ENCOUNTER_NAME,
         'date': OCCURRENCE_DATE,
         'encounter_times': [ '2:00 PM' ],
      }
   )
   assert result[ 'success' ] is True
   assert result[ 'date' ] == OCCURRENCE_DATE
   assert result[ 'times' ] == [ '2:00 PM' ]


def Test_CancelWildEncounterOccurrence_TestHttpRequest_ExpectCouldNotCancelApiError(
      stub_wild_encounter_coordinator: StubWildEncounterCoordinator ) -> None:
   StubWildEncounterCoordinator.default_success = False
   handler = make_handler(
      '/cancel-wild-encounter-occurrence',
      {
         'wildEncounter': WILD_ENCOUNTER_NAME,
         'date': OCCURRENCE_DATE,
         'times': [ '2:00 PM' ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is False
   assert result[ 'apiErrorType' ] == 'couldNotCancelWildEncounterOccurrence'
