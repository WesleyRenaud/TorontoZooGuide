from __future__ import annotations

import sqlite3

import pytest

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler import GuardiansTalkItineraryItemScheduler
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType


SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

TALK_KEY = GuardiansTalkScheduleItemKey(
   name='Turtle Talk',
   start_time='14:00',
)

TALK_DIFF = GuardiansTalkDiff(
   name='Turtle Talk',
   is_deleted=False,
   start_time='2:00 PM',
   end_time='2:15 PM',
   location='Americas Pavilion',
)

ITINERARY_CONTEXT = {
   'guardians_coordinator': GuardiansCoordinator,
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
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value=None,
         arrival_time=None,
         departure_time=None ) )

   result = GuardiansTalkItineraryItemScheduler.schedule(
      scheduler_conn,
      TALK_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_guardians_talk_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_Schedule_TestAlreadyScheduledTalk_ExpectItemAlreadyScheduled(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         guardians_talk_rows=[
            ItineraryGuardiansTalkRecord(
               talk_name='Turtle Talk',
               start_time='2:00 PM',
               end_time='2:15 PM',
               is_deleted=False,
            ),
         ],
      ) )

   result = GuardiansTalkItineraryItemScheduler.schedule(
      scheduler_conn,
      TALK_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_guardians_talk_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED


def Test_Schedule_TestTalkNotOnDaySchedule_ExpectTypedError(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      GuardiansTalkItineraryItemScheduler,
      '_guardians_talk_diff_for_saved_itinerary_day',
      lambda *args, **kwargs: GuardiansTalkDiff(
         name='Turtle Talk',
         is_deleted=True ) )

   result = GuardiansTalkItineraryItemScheduler.schedule(
      scheduler_conn,
      TALK_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_guardians_talk_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result.status == ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE


def Test_Schedule_TestOverlapWithoutConfirmation_ExpectUnscheduleWarning(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      GuardiansTalkItineraryItemScheduler,
      '_guardians_talk_diff_for_saved_itinerary_day',
      lambda *args, **kwargs: TALK_DIFF )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap',
      lambda saved_itinerary, talks: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk',
      lambda *args, **kwargs: False )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.GuardiansTalkLongWaitWarningBuilder.reason_after_adding_with_simulated_bulk',
      lambda *args, **kwargs: None )

   result = GuardiansTalkItineraryItemScheduler.schedule(
      scheduler_conn,
      TALK_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_guardians_talk_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS


def Test_Schedule_TestValidTalk_ExpectCoverForActivity(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      GuardiansTalkItineraryItemScheduler,
      '_guardians_talk_diff_for_saved_itinerary_day',
      lambda *args, **kwargs: TALK_DIFF )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.GuardiansTalkUnschedulePreparer.saved_itinerary_has_overlap',
      lambda saved_itinerary, talks: False )
   monkeypatch.setattr(
      GuardiansTalkItineraryItemScheduler,
      '_insert_scheduled_guardians_talk',
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
      }

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.guardians_talk_itinerary_item_scheduler.ScheduledActivityVisitTimesCoverer.cover_for_activity',
      cover_for_activity )

   result = GuardiansTalkItineraryItemScheduler.schedule(
      scheduler_conn,
      TALK_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_guardians_talk_unschedule=False,
      confirming_fixed_time_item_long_wait=True,
      confirming_guardians_talk_without_animal=True )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'cover' ] == {
      'start_time': '2:00 PM',
      'end_time': '2:15 PM',
   }
