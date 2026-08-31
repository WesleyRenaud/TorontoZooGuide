from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.schedule_slot_time_resolver import ScheduleSlotTimeResolver
from api.itinerary.scheduling.items.schedule_window_preparer import ScheduleWindowPreparer
from api.models import Animal
from api.shared.enums import ItineraryErrorType

VISIT_WINDOW = ( 16 * 3600, 16 * 3600 + 5 * 60 )
DAY_HOURS_WINDOW = ( 9 * 3600 + 30 * 60, 17 * 3600 )
DURATION_SECONDS = 8 * 60

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='4:00 PM',
   departure_time='4:05 PM' )


@pytest.fixture
def schedule_conn() -> sqlite3.Connection:
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


def Test_EffectiveDurationSeconds_TestDefaultAndOverride_ExpectSeconds() -> None:
   assert ScheduleSlotTimeResolver.effective_duration_seconds(
      None,
      40 * 60 ) == 40 * 60
   assert ScheduleSlotTimeResolver.effective_duration_seconds(
      20,
      40 * 60 ) == 20 * 60
   assert ScheduleSlotTimeResolver.effective_duration_seconds( None, None ) is None


def Test_Resolve_TestRequestedOverlap_ExpectRequestedTimeNotAvailable(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   blocked_itinerary = ItineraryBuilder.build(
      date='2026-06-15',
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: blocked_itinerary )

   slot, error = ScheduleSlotTimeResolver.resolve(
      schedule_conn,
      SAVED_ITINERARY,
      ( 9 * 3600 + 30 * 60, 17 * 3600 ),
      DURATION_SECONDS,
      start_time='10:00',
      itinerary_context={} )

   assert slot is None
   assert error is not None
   assert error.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def Test_Resolve_TestFullVisitWindowWithoutStart_ExpectNoAvailableSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   slot, error = ScheduleSlotTimeResolver.resolve(
      schedule_conn,
      SAVED_ITINERARY,
      VISIT_WINDOW,
      DURATION_SECONDS,
      start_time=None,
      itinerary_context={} )

   assert slot is None
   assert error is not None
   assert error.status == ItineraryErrorType.NO_AVAILABLE_SLOT


def Test_ResolveAllowingVisitExtension_TestShortVisitWindow_ExpectEarlierSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ScheduleWindowPreparer,
      'prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: type(
         'Prepared',
         (),
         { 'window': DAY_HOURS_WINDOW },
      )() )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SAVED_ITINERARY,
      VISIT_WINDOW,
      DURATION_SECONDS,
      start_time=None,
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert error is None
   assert slot is not None
   assert slot[ 1 ] == '4:00 PM'


def Test_ResolveAllowingVisitExtension_TestRequestedStartAfterDeparture_ExpectSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   visit_window = ( 9 * 3600 + 30 * 60, 12 * 3600 )
   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='12:00 PM' ),
      visit_window,
      DURATION_SECONDS,
      start_time='1:00 PM',
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert error is None
   assert slot == ( '1:00 PM', '1:08 PM' )


def Test_ResolveAllowingVisitExtension_TestPackAfterFullVisitWindow_ExpectAfterVisitSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   short_visit_window = ( 9 * 3600 + 30 * 60, 9 * 3600 + 38 * 60 )
   blocked_itinerary = ItineraryBuilder.build(
      date='2026-06-15',
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='9:30 AM',
            end_time='9:38 AM' ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='9:38 AM' )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: blocked_itinerary )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='9:38 AM' ),
      short_visit_window,
      7 * 60,
      start_time=None,
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert error is None
   assert slot == ( '9:38 AM', '9:45 AM' )
