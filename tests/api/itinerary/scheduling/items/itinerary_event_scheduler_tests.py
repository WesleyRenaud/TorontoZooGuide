from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.itinerary_event_scheduler import ItineraryEventScheduler
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.shared.operating_hours import OperatingHours


VISIT_DATE = date( 2026, 6, 20 )
VISIT_WINDOW = ( 9 * 3600 + 30 * 60, 17 * 3600 )
ZOO_HOURS = OperatingHours.from_schedule_times( '9:30 AM', '5:00 PM' )
assert ZOO_HOURS is not None

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='12:00 PM',
)

ITINERARY_CONTEXT: dict[ str, object ] = {}


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


def _stub_event_schedule_flow(
      monkeypatch: pytest.MonkeyPatch,
      *,
      saved_itinerary: SavedItinerary = SAVED_ITINERARY,
      default_duration_seconds: int = 40 * 60,
      ) -> dict[ str, object ]:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=VISIT_WINDOW,
      visit_date=VISIT_DATE,
      zoo_operating_hours=ZOO_HOURS )
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_slot_time_resolver.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds',
      lambda conn, event_type: default_duration_seconds )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ScheduleItineraryItemProvider.insert_itinerary_event_schedule',
      lambda cur, event: captured.setdefault( 'event', event ) )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
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
         'current_arrival_time': current_arrival_time,
         'current_departure_time': current_departure_time,
      }

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ScheduledActivityVisitTimesCoverer.cover_for_activity',
      cover_for_activity )

   return captured


def Test_Schedule_TestAlreadyScheduledEvent_ExpectItemAlreadyScheduled(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_event_schedule_flow(
      monkeypatch,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         event_rows=[
            ItineraryEventRecord(
               event_type=ItineraryEventType.LUNCH,
               start_time='12:00 PM',
               end_time='12:40 PM',
            ),
         ],
      ) )

   result = ItineraryEventScheduler.schedule(
      scheduler_conn,
      event_type=ItineraryEventType.LUNCH,
      time_options=ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED


def Test_Schedule_TestLunchAfterDeparture_ExpectCoverForActivity(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured = _stub_event_schedule_flow( monkeypatch )

   result = ItineraryEventScheduler.schedule(
      scheduler_conn,
      event_type=ItineraryEventType.LUNCH,
      time_options=ParsedScheduleTimeOptions( start_time='15:30', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'event' ].start_time == '3:30 PM'
   assert captured[ 'event' ].end_time == '4:10 PM'
   assert captured[ 'cover' ] == {
      'start_time': '3:30 PM',
      'end_time': '4:10 PM',
      'current_arrival_time': '9:30 AM',
      'current_departure_time': '12:00 PM',
   }


def Test_Schedule_TestPrepareFailure_ExpectSaveResult(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   failure = ItinerarySaveResult(
      status=ItineraryErrorType.SAVE_FAILED,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: failure )

   assert ItineraryEventScheduler.schedule(
      scheduler_conn,
      event_type=ItineraryEventType.LUNCH,
      time_options=ParsedScheduleTimeOptions( start_time='12:00 PM', duration_minutes=30 ),
      itinerary_context=ITINERARY_CONTEXT ) is failure


def Test_Schedule_TestMissingDuration_ExpectSaveFailed(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_event_schedule_flow( monkeypatch )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ItineraryDefaultDurationProvider.fetch_event_default_duration_seconds',
      lambda conn, event_type: None )

   result = ItineraryEventScheduler.schedule(
      scheduler_conn,
      event_type=ItineraryEventType.LUNCH,
      time_options=ParsedScheduleTimeOptions( start_time='12:00 PM', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.SAVE_FAILED


def Test_Schedule_TestSlotError_ExpectErrorResult(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_event_schedule_flow( monkeypatch )
   slot_error = ItinerarySaveResult(
      status=ItineraryErrorType.TIME_OUT_OF_BOUNDS,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.itinerary_event_scheduler.ScheduleSlotTimeResolver.resolve_allowing_visit_extension',
      lambda *args, **kwargs: ( None, slot_error ) )

   result = ItineraryEventScheduler.schedule(
      scheduler_conn,
      event_type=ItineraryEventType.LUNCH,
      time_options=ParsedScheduleTimeOptions( start_time='12:00 PM', duration_minutes=30 ),
      itinerary_context=ITINERARY_CONTEXT )

   assert result is slot_error
