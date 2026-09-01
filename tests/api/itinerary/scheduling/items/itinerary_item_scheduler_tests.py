from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.attraction_itinerary_item_scheduler import AttractionItineraryItemScheduler
from api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler import GuardiansTalkItineraryItemScheduler
from api.itinerary.scheduling.items.itinerary_event_scheduler import ItineraryEventScheduler
from api.itinerary.scheduling.items.itinerary_item_scheduler import ItineraryItemScheduler
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.listed_itinerary_item_scheduler import ListedItineraryItemScheduler
from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


ITINERARY_CONTEXT = { 'visit_date_temp': None }

ANIMAL_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)

ATTRACTION_KEY = AttractionScheduleItemKey( name='Conservation Carousel' )

TALK_KEY = GuardiansTalkScheduleItemKey(
   name='African Lion',
   start_time='2:00 PM',
)

SUCCESS_RESULT = ItinerarySaveResult(
   status=ItineraryErrorType.SUCCESS,
   reasons=[],
   itinerary=ItineraryBuilder.empty() )


@pytest.fixture
def item_scheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_item_scheduler_context( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ItineraryScheduleContextBuilder.build',
      lambda **kwargs: ITINERARY_CONTEXT )


def Test_Schedule_TestMissingKey_ExpectSaveFailed(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      None,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False )

   assert result.status == ItineraryErrorType.SAVE_FAILED


def Test_Schedule_TestInvalidTimeOptions_ExpectParseError(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ScheduleTimeOptionsParser.parse',
      lambda start_time, duration_minutes: ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      ANIMAL_KEY,
      start_time='bad-time',
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False )

   assert result.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def Test_Schedule_TestEventKey_ExpectEventSchedulerCalled(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   parsed_options = ParsedScheduleTimeOptions(
      start_time='12:00 PM',
      duration_minutes=40 )
   calls: list[ object ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ScheduleTimeOptionsParser.parse',
      lambda start_time, duration_minutes: parsed_options )
   monkeypatch.setattr(
      ItineraryEventScheduler,
      'schedule',
      lambda conn, *, event_type, time_options, itinerary_context: calls.append(
         ( event_type, time_options ) ) or SUCCESS_RESULT )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      ItineraryEventType.LUNCH,
      start_time='12:00',
      duration_minutes=40,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False )

   assert result == SUCCESS_RESULT
   assert calls == [ ( ItineraryEventType.LUNCH, parsed_options ) ]


def Test_Schedule_TestAnimalKey_ExpectListedSchedulerCalled(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   parsed_options = ParsedScheduleTimeOptions(
      start_time='2:00 PM',
      duration_minutes=None )
   calls: list[ object ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ScheduleTimeOptionsParser.parse',
      lambda start_time, duration_minutes: parsed_options )
   monkeypatch.setattr(
      ListedItineraryItemScheduler,
      'schedule',
      lambda conn, schedule_item_key, parsed_schedule_options, **kwargs: calls.append(
         ( schedule_item_key, parsed_schedule_options ) ) or SUCCESS_RESULT )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      ANIMAL_KEY,
      start_time='14:00',
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False )

   assert result == SUCCESS_RESULT
   assert calls == [ ( ANIMAL_KEY, parsed_options ) ]


def Test_Schedule_TestAttractionKey_ExpectAttractionSchedulerCalled(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   parsed_options = ParsedScheduleTimeOptions(
      start_time='11:00 AM',
      duration_minutes=20 )
   calls: list[ object ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ScheduleTimeOptionsParser.parse',
      lambda start_time, duration_minutes: parsed_options )
   monkeypatch.setattr(
      AttractionItineraryItemScheduler,
      'schedule',
      lambda conn, schedule_item_key, parsed_schedule_options, **kwargs: calls.append(
         ( schedule_item_key, parsed_schedule_options ) ) or SUCCESS_RESULT )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      ATTRACTION_KEY,
      start_time='11:00',
      duration_minutes=20,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=True,
      confirming_attraction_outside_operating_hours=True,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=False,
      confirming_guardians_talk_without_animal=False )

   assert result == SUCCESS_RESULT
   assert calls == [ ( ATTRACTION_KEY, parsed_options ) ]


def Test_Schedule_TestGuardiansTalkKey_ExpectTalkSchedulerCalled(
      item_scheduler_conn: sqlite3.Connection,
      stub_item_scheduler_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   parsed_options = ParsedScheduleTimeOptions(
      start_time='2:00 PM',
      duration_minutes=None )
   calls: list[ object ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_item_scheduler.ScheduleTimeOptionsParser.parse',
      lambda start_time, duration_minutes: parsed_options )
   monkeypatch.setattr(
      GuardiansTalkItineraryItemScheduler,
      'schedule',
      lambda conn, schedule_item_key, **kwargs: calls.append( schedule_item_key ) or SUCCESS_RESULT )

   result = ItineraryItemScheduler.schedule(
      item_scheduler_conn,
      TALK_KEY,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False,
      confirming_guardians_talk_unschedule=True,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result == SUCCESS_RESULT
   assert calls == [ TALK_KEY ]
