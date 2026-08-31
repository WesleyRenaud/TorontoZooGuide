from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler import WildEncounterItineraryItemScheduler
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[],
)

ENCOUNTER_KEY = WildEncounterScheduleItemKey(
   name='African Rainforest',
   start_time='15:30',
)

ITINERARY_CONTEXT = {
   'wild_encounter_coordinator': WildEncounterCoordinator,
}


@pytest.fixture
def scheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_save_result( monkeypatch: pytest.MonkeyPatch ) -> None:
   def save_result(
         conn: sqlite3.Connection,
         status: ItineraryErrorType,
         *,
         reasons: list[ ItineraryResultReason ] | None = None,
         **context: object ) -> ItinerarySaveResult:
      return ItinerarySaveResult(
         status=status,
         reasons=reasons or [],
         itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr( ItinerarySaveResultBuilder, 'save_result', save_result )


def Test_Schedule_TestMissingVisitDate_ExpectItineraryDateNotSet(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value=None,
         arrival_time=None,
         departure_time=None ) )

   result = WildEncounterItineraryItemScheduler.schedule(
      scheduler_conn,
      ENCOUNTER_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True )

   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_Schedule_TestEncounterNotOnDaySchedule_ExpectTypedError(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      WildEncounterCoordinator,
      'get_wild_encounter_on_day_schedule',
      lambda **kwargs: None )

   result = WildEncounterItineraryItemScheduler.schedule(
      scheduler_conn,
      ENCOUNTER_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True )

   assert result.status == ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE


def Test_Schedule_TestAlreadyScheduledEncounter_ExpectItemAlreadyScheduled(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         wild_encounter_rows=[
            ItineraryWildEncounterRecord(
               wild_encounter='African Rainforest',
               start_time='3:30 PM',
               end_time='4:15 PM',
               is_deleted=False,
            ),
         ],
      ) )

   result = WildEncounterItineraryItemScheduler.schedule(
      scheduler_conn,
      ENCOUNTER_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True )

   assert result.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED


ENCOUNTER_DIFF = WildEncounterDiff(
   name='African Rainforest',
   is_deleted=False,
   start_time='3:30 PM',
   end_time='4:15 PM',
   meeting_spot='Americas Pavilion',
)


def Test_Schedule_TestEncounterAfterDeparture_ExpectCoverForActivity(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='12:00 PM',
      ) )
   monkeypatch.setattr(
      WildEncounterItineraryItemScheduler,
      '_wild_encounter_diff_for_saved_itinerary_day',
      lambda *args, **kwargs: ENCOUNTER_DIFF )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.WildEncounterUnschedulePreparer.saved_itinerary_has_overlap',
      lambda saved_itinerary, encounters: False )
   monkeypatch.setattr(
      WildEncounterItineraryItemScheduler,
      '_insert_scheduled_wild_encounter',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   def cover_for_activity(
         conn: sqlite3.Connection,
         *,
         start_time: str,
         end_time: str,
         current_arrival_time: str | None,
         current_departure_time: str | None,
         itinerary_context: dict[ str, object ],
         seed_if_complete: bool = True ) -> None:
      captured[ 'cover' ] = {
         'start_time': start_time,
         'end_time': end_time,
         'current_departure_time': current_departure_time,
      }

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ScheduledActivityVisitTimesCoverer.cover_for_activity',
      cover_for_activity )

   result = WildEncounterItineraryItemScheduler.schedule(
      scheduler_conn,
      ENCOUNTER_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'cover' ] == {
      'start_time': '3:30 PM',
      'end_time': '4:15 PM',
      'current_departure_time': '12:00 PM',
   }


def Test_Schedule_TestOverlapWithoutConfirmation_ExpectUnscheduleWarning(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      WildEncounterItineraryItemScheduler,
      '_wild_encounter_diff_for_saved_itinerary_day',
      lambda *args, **kwargs: ENCOUNTER_DIFF )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.WildEncounterUnschedulePreparer.saved_itinerary_has_overlap',
      lambda saved_itinerary, encounters: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.wild_encounter_itinerary_item_scheduler.WildEncounterLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk',
      lambda *args, **kwargs: None )

   result = WildEncounterItineraryItemScheduler.schedule(
      scheduler_conn,
      ENCOUNTER_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_wild_encounter_unschedule=False,
      confirming_fixed_time_item_long_wait=True )

   assert result.status == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
