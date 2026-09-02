from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import cast

import pytest

from api.guardians.cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_cancellation_provider import GuardiansTalkCancellationProvider
from api.guardians.data_access.guardians_talk_day_schedule_provider import GuardiansTalkDayScheduleProvider
from api.guardians.data_access.guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.data_access.meet_the_guardians_talk_provider import MeetTheGuardiansTalkProvider
from api.guardians.data_access.meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from api.guardians.domain.guardians_talk_builder import GuardiansTalkBuilder
from api.guardians.domain.guardians_talk_linked_animals_builder import GuardiansTalkLinkedAnimalsBuilder
from api.guardians.itinerary.itinerary_guardians_talks_builder import ItineraryGuardiansTalksBuilder
from api.guardians.scheduling.guardians_talk_day_schedule_builder import GuardiansTalkDayScheduleBuilder
from api.guardians.scheduling.guardians_talk_day_schedule_finder import GuardiansTalkDayScheduleFinder
from api.guardians.scheduling.guardians_talk_occurrences_builder import GuardiansTalkOccurrencesBuilder
from api.guardians.scheduling.guardians_talk_schedule_builder import GuardiansTalkScheduleBuilder
from api.guardians.scheduling.guardians_talk_schedule_conflict_resolver import GuardiansTalkScheduleConflictResolver
from api.guardians.scheduling.guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
from api.guardians.scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from api.guardians.search.guardians_talks_matching_query_builder import GuardiansTalksMatchingQueryBuilder
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.models import GuardiansTalk
from api.models import ScheduledOccurrence
from api.request_connection_provider import RequestConnectionProvider
from api.types import Types


TALK_NAME = 'African Lion'
TALK_LOCATION = 'Africa Savanna'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
TALK_TIME = '10:00 AM'
MESSAGE = 'Talk cancelled today.'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
TARGET_DATE = date( 2026, 6, 15 )
QUERY = 'lion'
OCCURRENCE_DATE = '2026-06-15'

SCHEDULE_ROW = {
   'time': TALK_TIME,
   'monday': True,
   'tuesday': True,
   'wednesday': True,
   'thursday': True,
   'friday': True,
   'saturday': False,
   'sunday': False,
}

SCHEDULE_INPUT = GuardiansTalkScheduleInput(
   talk_name=TALK_NAME,
   location=TALK_LOCATION,
   start_date=START_DATE,
   end_date=END_DATE,
   talk_time=TALK_TIME,
   monday=True,
   tuesday=True,
   wednesday=True,
   thursday=True,
   friday=True,
   saturday=False,
   sunday=False,
   message=MESSAGE )

GUARDIANS_TALK = GuardiansTalk(
   name=TALK_NAME,
   location=TALK_LOCATION,
   x_coord=1.0,
   y_coord=2.0,
   start_time=TALK_TIME )


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_GetGuardiansTalkLocations_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MeetTheGuardiansTalkProvider,
      'fetch_guardians_talk_locations',
      lambda _conn: [ TALK_LOCATION ] )

   assert GuardiansCoordinator.get_guardians_talk_locations() == [ TALK_LOCATION ]


def Test_GetGuardiansTalkNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MeetTheGuardiansTalkProvider,
      'fetch_guardians_talk_names',
      lambda _conn: [ TALK_NAME ] )

   assert GuardiansCoordinator.get_guardians_talk_names() == [ TALK_NAME ]


def Test_GetGuardiansTalkNamesAtLocation_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def fetch(
         _conn: Types.Connection,
         *,
         location: str ) -> list[ str ]:
      captured[ 'location' ] = location
      return [ TALK_NAME ]

   monkeypatch.setattr(
      MeetTheGuardiansTalkProvider,
      'fetch_guardians_talk_names_at_location',
      fetch )

   assert GuardiansCoordinator.get_guardians_talk_names_at_location(
      TALK_LOCATION ) == [ TALK_NAME ]
   assert captured[ 'location' ] == TALK_LOCATION


def Test_GetGuardiansTalkDetails_TestBuilderResult_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk_records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      MeetTheGuardiansTalkProvider,
      'fetch_meet_the_guardians_talk_records',
      lambda _conn: talk_records )

   def build_details(
         records: list[ MeetTheGuardiansTalkRecord ],
         *,
         guardians_talks_to_include: list[ str ] | None = None ) -> list[ GuardiansTalk ]:
      captured[ 'records' ] = records
      captured[ 'include' ] = guardians_talks_to_include
      return [ GUARDIANS_TALK ]

   monkeypatch.setattr( GuardiansTalkBuilder, 'build_details', build_details )

   assert GuardiansCoordinator.get_guardians_talk_details(
      guardians_talks_to_include=[ TALK_NAME ] ) == [ GUARDIANS_TALK ]
   assert captured[ 'records' ] is talk_records
   assert captured[ 'include' ] == [ TALK_NAME ]


def Test_GetGuardiansTalkOccurrences_TestProvidersAndBuilder_ExpectOccurrences(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_records = [ object() ]
   cancellation_records = [ object() ]
   occurrence_records = [ object() ]
   expected = [ ScheduledOccurrence(
      date=OCCURRENCE_DATE,
      time=TALK_TIME ) ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'fetch_schedule_records_for_occurrences',
      lambda *_args, **_kwargs: schedule_records )
   monkeypatch.setattr(
      GuardiansTalkCancellationProvider,
      'fetch_cancellation_records',
      lambda *_args, **_kwargs: cancellation_records )
   monkeypatch.setattr(
      GuardiansTalkOccurrenceProvider,
      'fetch_occurrence_records',
      lambda *_args, **_kwargs: occurrence_records )

   def build( **kwargs: object ) -> list[ ScheduledOccurrence ]:
      captured.update( kwargs )
      return expected

   monkeypatch.setattr( GuardiansTalkOccurrencesBuilder, 'build', build )

   assert GuardiansCoordinator.get_guardians_talk_occurrences(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      days_ahead=3 ) == expected
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'cancellation_records' ] is cancellation_records
   assert captured[ 'occurrence_records' ] is occurrence_records
   assert captured[ 'days_ahead' ] == 3


def Test_SetGuardiansTalkSchedule_TestBuiltSchedules_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ GuardiansTalkScheduleInput ] = []

   monkeypatch.setattr(
      GuardiansTalkScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )

   def save_schedule(
         _conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      saved.append( schedule )
      return True

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'save_schedule',
      save_schedule )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_ReplaceGuardiansTalkScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ GuardiansTalkScheduleInput ] = []

   monkeypatch.setattr(
      GuardiansTalkScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )

   def save_replacing(
         _conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      saved.append( schedule )
      return True

   monkeypatch.setattr(
      GuardiansTalkScheduleConflictResolver,
      'save_replacing_overlaps',
      save_replacing )

   assert GuardiansCoordinator.replace_guardians_talk_schedule_overlaps(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_TrimGuardiansTalkScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ GuardiansTalkScheduleInput ] = []

   monkeypatch.setattr(
      GuardiansTalkScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )

   def save_trimming(
         _conn: Types.Connection,
         schedule: GuardiansTalkScheduleInput ) -> bool:
      saved.append( schedule )
      return True

   monkeypatch.setattr(
      GuardiansTalkScheduleConflictResolver,
      'save_trimming_overlaps',
      save_trimming )

   assert GuardiansCoordinator.trim_guardians_talk_schedule_overlaps(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_SetGuardiansTalkSchedule_TestEmptyScheduleRows_ExpectFalse(
      stub_request_connection: None ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      schedule_rows=[] ) is False


def Test_SetGuardiansTalkSchedule_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )
   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'save_schedule',
      lambda *_args, **_kwargs: False )

   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is False


def Test_EndGuardiansTalkSchedule_TestSaveEnds_ExpectTrue(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ str ] = []

   def save_schedule_end(
         _conn: Types.Connection,
         *,
         schedule_end: GuardiansTalkScheduleEndInput ) -> bool:
      saved_times.append( schedule_end.talk_time )
      return True

   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'save_schedule_end',
      save_schedule_end )

   assert GuardiansCoordinator.end_guardians_talk_schedule(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      schedule_end_date=END_DATE,
      talk_times=[ TALK_TIME, '11:00 AM' ] ) is True
   assert saved_times == [ TALK_TIME, '11:00 AM' ]


def Test_EndGuardiansTalkSchedule_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkScheduleProvider,
      'save_schedule_end',
      lambda *_args, **_kwargs: False )

   assert GuardiansCoordinator.end_guardians_talk_schedule(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      schedule_end_date=END_DATE,
      talk_times=[ TALK_TIME ] ) is False


def Test_CancelGuardiansTalkOccurrence_TestSaveCancellations_ExpectTrue(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ str ] = []

   def save_cancellation(
         _conn: Types.Connection,
         *,
         cancellation: GuardiansTalkCancellationInput ) -> bool:
      saved_times.append( cancellation.talk_time )
      return True

   monkeypatch.setattr(
      GuardiansTalkCancellationProvider,
      'save_cancellation',
      save_cancellation )

   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=OCCURRENCE_DATE,
      talk_times=[ TALK_TIME ] ) is True
   assert saved_times == [ TALK_TIME ]


def Test_CancelGuardiansTalkOccurrence_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkCancellationProvider,
      'save_cancellation',
      lambda *_args, **_kwargs: False )

   assert GuardiansCoordinator.cancel_guardians_talk_occurrence(
      talk=TALK_NAME,
      location=TALK_LOCATION,
      date=OCCURRENCE_DATE,
      talk_times=[ TALK_TIME ] ) is False


def Test_GetGuardiansTalksForSavedItinerary_TestEmpty_ExpectEmpty() -> None:
   assert GuardiansCoordinator.get_guardians_talks_for_saved_itinerary( [] ) == []


def Test_GetGuardiansTalksForSavedItinerary_TestSavedTalks_ExpectLinkedTalks(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved = [
      ItineraryGuardiansTalkRecord(
         talk_name=TALK_NAME,
         start_time=TALK_TIME,
         end_time='10:30 AM',
         is_deleted=False ),
   ]
   details = [ GUARDIANS_TALK ]
   itinerary_talks = [
      GuardiansTalk(
         name=TALK_NAME,
         location=TALK_LOCATION,
         x_coord=1.0,
         y_coord=2.0,
         start_time=TALK_TIME ),
   ]
   linked = [
      GuardiansTalk(
         name=TALK_NAME,
         location=TALK_LOCATION,
         x_coord=1.0,
         y_coord=2.0,
         start_time=TALK_TIME,
         linked_animals=[] ),
   ]

   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_details',
      lambda names: details if names == [ TALK_NAME ] else [] )
   monkeypatch.setattr(
      ItineraryGuardiansTalksBuilder,
      'build',
      lambda talks, saved_talks: itinerary_talks if talks is details else [] )
   monkeypatch.setattr(
      GuardiansTalkLinkedAnimalsBuilder,
      'attach',
      lambda _conn, talks: linked if talks is itinerary_talks else [] )

   assert GuardiansCoordinator.get_guardians_talks_for_saved_itinerary(
      saved ) == linked


def Test_GetGuardiansTalkScheduleForTargetDate_TestProvidersAndBuilders_ExpectTalks(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   records = [ object() ]
   day_talks = [ GUARDIANS_TALK ]
   linked = [ GUARDIANS_TALK ]

   monkeypatch.setattr(
      GuardiansTalkDayScheduleProvider,
      'fetch_day_schedule_records',
      lambda _conn, target: records if target == TARGET_DATE.isoformat() else [] )
   monkeypatch.setattr(
      GuardiansTalkDayScheduleBuilder,
      'build_from_records',
      lambda fetched: day_talks if fetched is records else [] )
   monkeypatch.setattr(
      GuardiansTalkLinkedAnimalsBuilder,
      'attach',
      lambda _conn, talks: linked if talks is day_talks else [] )

   assert GuardiansCoordinator.get_guardians_talk_schedule_for_target_date(
      TARGET_DATE ) == linked


def Test_GetGuardiansTalkSchedule_TestVisitDate_ExpectDelegatesToTargetDate(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_schedule_for_target_date',
      lambda target: [ GUARDIANS_TALK ] if target == TARGET_DATE else [] )

   assert GuardiansCoordinator.get_guardians_talk_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == [ GUARDIANS_TALK ]


def Test_GetGuardiansTalksMatchingQuery_TestScheduleAndBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   day_talks = [ GUARDIANS_TALK ]
   matched = [ GUARDIANS_TALK ]

   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_schedule',
      lambda **_kwargs: day_talks )
   monkeypatch.setattr(
      GuardiansTalksMatchingQueryBuilder,
      'build',
      lambda talks, query: matched if talks is day_talks and query == QUERY else [] )

   assert GuardiansCoordinator.get_guardians_talks_matching_query(
      query=QUERY,
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == matched


def Test_GetGuardiansTalkOnDaySchedule_TestProvidedDaySchedule_ExpectFinderResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   day_schedule = [ GUARDIANS_TALK ]
   captured: dict[ str, object ] = {}

   def find(
         rows: list[ GuardiansTalk ],
         talk_name: str,
         *,
         start_time: str ) -> GuardiansTalk | None:
      captured[ 'rows' ] = rows
      captured[ 'talk_name' ] = talk_name
      captured[ 'start_time' ] = start_time
      return GUARDIANS_TALK

   monkeypatch.setattr(
      GuardiansTalkDayScheduleFinder,
      'find_on_day_schedule',
      find )

   assert GuardiansCoordinator.get_guardians_talk_on_day_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      talk_name=TALK_NAME,
      year=VISIT_YEAR,
      start_time=TALK_TIME,
      day_schedule=day_schedule ) is GUARDIANS_TALK
   assert captured[ 'rows' ] is day_schedule
   assert captured[ 'talk_name' ] == TALK_NAME
   assert captured[ 'start_time' ] == TALK_TIME


def Test_GetGuardiansTalkOnDaySchedule_TestMissingDaySchedule_ExpectFetchesSchedule(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fetched = [ GUARDIANS_TALK ]

   monkeypatch.setattr(
      GuardiansCoordinator,
      'get_guardians_talk_schedule',
      lambda **_kwargs: fetched )
   monkeypatch.setattr(
      GuardiansTalkDayScheduleFinder,
      'find_on_day_schedule',
      lambda rows, *_args, **_kwargs: GUARDIANS_TALK if rows is fetched else None )

   assert GuardiansCoordinator.get_guardians_talk_on_day_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      talk_name=TALK_NAME,
      year=VISIT_YEAR,
      start_time=TALK_TIME ) is GUARDIANS_TALK
