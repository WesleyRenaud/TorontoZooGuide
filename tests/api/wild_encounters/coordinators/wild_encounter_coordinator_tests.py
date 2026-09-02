from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import cast

import pytest

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.models import ScheduledOccurrence
from api.models import WildEncounter
from api.request_connection_provider import RequestConnectionProvider
from api.types import Types
from api.wild_encounters.cancellations.wild_encounter_cancellation_input import WildEncounterCancellationInput
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.data_access.wild_encounter_cancellation_provider import WildEncounterCancellationProvider
from api.wild_encounters.data_access.wild_encounter_cancellation_record import WildEncounterCancellationRecord
from api.wild_encounters.data_access.wild_encounter_provider import WildEncounterProvider
from api.wild_encounters.data_access.wild_encounter_record import WildEncounterRecord
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from api.wild_encounters.data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from api.wild_encounters.domain.wild_encounter_builder import WildEncounterBuilder
from api.wild_encounters.itinerary.itinerary_wild_encounters_builder import ItineraryWildEncountersBuilder
from api.wild_encounters.scheduling.wild_encounter_day_schedule_builder import WildEncounterDayScheduleBuilder
from api.wild_encounters.scheduling.wild_encounter_day_schedule_finder import WildEncounterDayScheduleFinder
from api.wild_encounters.scheduling.wild_encounter_occurrences_builder import WildEncounterOccurrencesBuilder
from api.wild_encounters.scheduling.wild_encounter_schedule_builder import WildEncounterScheduleBuilder
from api.wild_encounters.scheduling.wild_encounter_schedule_conflict_resolver import WildEncounterScheduleConflictResolver
from api.wild_encounters.scheduling.wild_encounter_schedule_end_input import WildEncounterScheduleEndInput
from api.wild_encounters.scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput
from api.wild_encounters.search.wild_encounters_matching_query_builder import WildEncountersMatchingQueryBuilder


WILD_ENCOUNTER_NAME = 'African Rainforest'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
ENCOUNTER_TIME = '2:00 PM'
MESSAGE = 'Encounter unavailable.'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
QUERY = 'rain'
OCCURRENCE_DATE = '2026-06-15'
MEETING_SPOT = 'Rainforest Pavilion'
LINK = 'https://www.torontozoo.com/wild-encounters/african-rainforest'

SCHEDULE_ROW = {
   'time': ENCOUNTER_TIME,
   'monday': True,
   'tuesday': True,
   'wednesday': True,
   'thursday': True,
   'friday': True,
   'saturday': False,
   'sunday': False,
}

SCHEDULE_INPUT = WildEncounterScheduleInput(
   wild_encounter=WILD_ENCOUNTER_NAME,
   start_date=START_DATE,
   end_date=END_DATE,
   encounter_time=ENCOUNTER_TIME,
   monday=True,
   tuesday=True,
   wednesday=True,
   thursday=True,
   friday=True,
   saturday=False,
   sunday=False,
   message=MESSAGE )

WILD_ENCOUNTER = WildEncounter(
   name=WILD_ENCOUNTER_NAME,
   meeting_spot=MEETING_SPOT,
   link=LINK,
   start_time=ENCOUNTER_TIME )


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_GetWildEncounterNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      WildEncounterProvider,
      'fetch_wild_encounter_names',
      lambda _conn: [ WILD_ENCOUNTER_NAME ] )

   assert WildEncounterCoordinator.get_wild_encounter_names() == [ WILD_ENCOUNTER_NAME ]


def Test_GetWildEncounterDetails_TestBuilderResult_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      WildEncounterProvider,
      'fetch_wild_encounter_records',
      lambda _conn: records )

   def build_details(
         fetched: list[ WildEncounterRecord ],
         *,
         wild_encounters_to_include: list[ str ] | None = None ) -> list[ WildEncounter ]:
      captured[ 'records' ] = fetched
      captured[ 'include' ] = wild_encounters_to_include
      return [ WILD_ENCOUNTER ]

   monkeypatch.setattr( WildEncounterBuilder, 'build_details', build_details )

   assert WildEncounterCoordinator.get_wild_encounter_details(
      wild_encounters_to_include=[ WILD_ENCOUNTER_NAME ] ) == [ WILD_ENCOUNTER ]
   assert captured[ 'records' ] is records
   assert captured[ 'include' ] == [ WILD_ENCOUNTER_NAME ]


def Test_GetWildEncounterOccurrences_TestProvidersAndBuilder_ExpectOccurrences(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_records: list[ WildEncounterScheduleRecord ] = []
   cancellation_records: list[ WildEncounterCancellationRecord ] = []
   expected: list[ ScheduledOccurrence ] = []
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'fetch_schedule_records_for_occurrences',
      lambda *_args, **_kwargs: schedule_records )
   monkeypatch.setattr(
      WildEncounterCancellationProvider,
      'fetch_cancellation_records',
      lambda *_args, **_kwargs: cancellation_records )

   def build( **kwargs: object ) -> list[ ScheduledOccurrence ]:
      captured.update( kwargs )
      return expected

   monkeypatch.setattr( WildEncounterOccurrencesBuilder, 'build', build )

   assert WildEncounterCoordinator.get_wild_encounter_occurrences(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      days_ahead=5 ) == expected
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'cancellation_records' ] is cancellation_records
   assert captured[ 'days_ahead' ] == 5


def Test_SetWildEncounterSchedule_TestBuiltSchedules_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ WildEncounterScheduleInput ] = []

   monkeypatch.setattr(
      WildEncounterScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )

   def save_schedule(
         _conn: Types.Connection,
         schedule: WildEncounterScheduleInput ) -> bool:
      saved.append( schedule )
      return True

   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'save_schedule',
      save_schedule )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_ReplaceWildEncounterScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ WildEncounterScheduleInput ] = []

   monkeypatch.setattr(
      WildEncounterScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )
   monkeypatch.setattr(
      WildEncounterScheduleConflictResolver,
      'save_replacing_overlaps',
      lambda _conn, schedule: saved.append( schedule ) or True )

   assert WildEncounterCoordinator.replace_wild_encounter_schedule_overlaps(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_TrimWildEncounterScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ WildEncounterScheduleInput ] = []

   monkeypatch.setattr(
      WildEncounterScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )
   monkeypatch.setattr(
      WildEncounterScheduleConflictResolver,
      'save_trimming_overlaps',
      lambda _conn, schedule: saved.append( schedule ) or True )

   assert WildEncounterCoordinator.trim_wild_encounter_schedule_overlaps(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is True
   assert saved == [ SCHEDULE_INPUT ]


def Test_SetWildEncounterSchedule_TestEmptyScheduleRows_ExpectFalse(
      stub_request_connection: None ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      schedule_rows=[] ) is False


def Test_SetWildEncounterSchedule_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      WildEncounterScheduleBuilder,
      'build',
      lambda **_kwargs: SCHEDULE_INPUT )
   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'save_schedule',
      lambda *_args, **_kwargs: False )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE,
      schedule_rows=[ SCHEDULE_ROW ] ) is False


def Test_EndWildEncounterSchedule_TestSaveEnds_ExpectTrue(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ str ] = []

   def save_schedule_end(
         _conn: Types.Connection,
         *,
         schedule_end: WildEncounterScheduleEndInput ) -> bool:
      saved_times.append( schedule_end.encounter_time )
      return True

   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'save_schedule_end',
      save_schedule_end )

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      schedule_end_date=END_DATE,
      encounter_times=[ ENCOUNTER_TIME, '3:00 PM' ] ) is True
   assert saved_times == [ ENCOUNTER_TIME, '3:00 PM' ]


def Test_EndWildEncounterSchedule_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'save_schedule_end',
      lambda *_args, **_kwargs: False )

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      schedule_end_date=END_DATE,
      encounter_times=[ ENCOUNTER_TIME ] ) is False


def Test_CancelWildEncounterOccurrence_TestSaveCancellations_ExpectTrue(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_times: list[ str ] = []

   def save_cancellation(
         _conn: Types.Connection,
         *,
         cancellation: WildEncounterCancellationInput ) -> bool:
      saved_times.append( cancellation.encounter_time )
      return True

   monkeypatch.setattr(
      WildEncounterCancellationProvider,
      'save_cancellation',
      save_cancellation )

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      date=OCCURRENCE_DATE,
      encounter_times=[ ENCOUNTER_TIME ] ) is True
   assert saved_times == [ ENCOUNTER_TIME ]


def Test_CancelWildEncounterOccurrence_TestSaveFails_ExpectFalse(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      WildEncounterCancellationProvider,
      'save_cancellation',
      lambda *_args, **_kwargs: False )

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name=WILD_ENCOUNTER_NAME,
      date=OCCURRENCE_DATE,
      encounter_times=[ ENCOUNTER_TIME ] ) is False


def Test_GetWildEncountersForSavedItinerary_TestEmpty_ExpectEmpty() -> None:
   assert WildEncounterCoordinator.get_wild_encounters_for_saved_itinerary( [] ) == []


def Test_GetWildEncountersForSavedItinerary_TestSavedEncounters_ExpectBuilderResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved = [
      ItineraryWildEncounterRecord(
         wild_encounter=WILD_ENCOUNTER_NAME,
         start_time=ENCOUNTER_TIME,
         end_time='2:30 PM',
         is_deleted=False ),
   ]
   details = [ WILD_ENCOUNTER ]
   built = [
      WildEncounter(
         name=WILD_ENCOUNTER_NAME,
         meeting_spot=MEETING_SPOT,
         link=LINK,
         start_time=ENCOUNTER_TIME ),
   ]

   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounter_details',
      lambda names: details if names == [ WILD_ENCOUNTER_NAME ] else [] )
   monkeypatch.setattr(
      ItineraryWildEncountersBuilder,
      'build',
      lambda encounters, saved_encounters: built if encounters is details else [] )

   assert WildEncounterCoordinator.get_wild_encounters_for_saved_itinerary(
      saved ) == built


def Test_GetWildEncounterSchedule_TestProviderAndBuilder_ExpectDaySchedule(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   records: list[ WildEncounterScheduleRecord ] = []
   expected = [ WILD_ENCOUNTER ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      WildEncounterScheduleProvider,
      'fetch_schedule_records',
      lambda _conn, target_date: records )

   def build_for_target_date(
         fetched: list[ WildEncounterScheduleRecord ],
         target_date: date ) -> list[ WildEncounter ]:
      captured[ 'records' ] = fetched
      captured[ 'target_date' ] = target_date
      return expected

   monkeypatch.setattr(
      WildEncounterDayScheduleBuilder,
      'build_for_target_date',
      build_for_target_date )

   assert WildEncounterCoordinator.get_wild_encounter_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == expected
   assert captured[ 'records' ] is records
   assert getattr( captured[ 'target_date' ], 'isoformat' )() == '2026-06-15'


def Test_GetWildEncounterOnDaySchedule_TestProvidedDaySchedule_ExpectFinderResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   day_schedule = [ WILD_ENCOUNTER ]

   monkeypatch.setattr(
      WildEncounterDayScheduleFinder,
      'find_on_day_schedule',
      lambda rows, name, *, start_time: WILD_ENCOUNTER
      if rows is day_schedule and name == WILD_ENCOUNTER_NAME and start_time == ENCOUNTER_TIME
      else None )

   assert WildEncounterCoordinator.get_wild_encounter_on_day_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      encounter_name=WILD_ENCOUNTER_NAME,
      year=VISIT_YEAR,
      start_time=ENCOUNTER_TIME,
      day_schedule=day_schedule ) is WILD_ENCOUNTER


def Test_GetWildEncounterOnDaySchedule_TestMissingDaySchedule_ExpectFetchesSchedule(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fetched = [ WILD_ENCOUNTER ]

   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounter_schedule',
      lambda **_kwargs: fetched )
   monkeypatch.setattr(
      WildEncounterDayScheduleFinder,
      'find_on_day_schedule',
      lambda rows, *_args, **_kwargs: WILD_ENCOUNTER if rows is fetched else None )

   assert WildEncounterCoordinator.get_wild_encounter_on_day_schedule(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      encounter_name=WILD_ENCOUNTER_NAME,
      year=VISIT_YEAR,
      start_time=ENCOUNTER_TIME ) is WILD_ENCOUNTER


def Test_GetAvailableWildEncounters_TestFilterAvailable_ExpectFiltered(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   day_schedule = [ WILD_ENCOUNTER ]
   available = [ WILD_ENCOUNTER ]

   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounter_schedule',
      lambda **_kwargs: day_schedule )
   monkeypatch.setattr(
      WildEncounterDayScheduleBuilder,
      'filter_available',
      lambda rows: available if rows is day_schedule else [] )

   assert WildEncounterCoordinator.get_available_wild_encounters(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == available


def Test_GetWildEncountersMatchingQuery_TestAvailableAndBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   available = [ WILD_ENCOUNTER ]
   matched = [ WILD_ENCOUNTER ]

   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_available_wild_encounters',
      lambda **_kwargs: available )
   monkeypatch.setattr(
      WildEncountersMatchingQueryBuilder,
      'build',
      lambda encounters, query: matched if encounters is available and query == QUERY else [] )

   assert WildEncounterCoordinator.get_wild_encounters_matching_query(
      query=QUERY,
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == matched
