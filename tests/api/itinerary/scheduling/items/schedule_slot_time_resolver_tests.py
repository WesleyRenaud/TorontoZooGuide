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
from api.shared.calendar_dates import DateValues
from api.shared.duration_values import DurationValues
from api.shared.enums import ItineraryErrorType, Position

DURATION_MINUTES = 8
VISIT_ARRIVAL = '4:00 PM'
VISIT_DEPARTURE = '4:05 PM'
DAY_OPEN = '9:30 AM'
DAY_CLOSE = '5:00 PM'
VISIT_WINDOW = (
   DateValues.time_value_in_seconds( VISIT_ARRIVAL ),
   DateValues.time_value_in_seconds( VISIT_DEPARTURE ) )
DAY_HOURS_WINDOW = (
   DateValues.time_value_in_seconds( DAY_OPEN ),
   DateValues.time_value_in_seconds( DAY_CLOSE ) )
DURATION_SECONDS = DurationValues.minutes_to_seconds( DURATION_MINUTES )

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time=VISIT_ARRIVAL,
   departure_time=VISIT_DEPARTURE )


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


def Test_EffectiveDurationSeconds_TestDefault_ExpectDefaultSeconds() -> None:
   default_minutes = 40

   seconds = ScheduleSlotTimeResolver.effective_duration_seconds(
      None,
      DurationValues.minutes_to_seconds( default_minutes ) )

   assert seconds == DurationValues.minutes_to_seconds( default_minutes )


def Test_EffectiveDurationSeconds_TestOverride_ExpectOverrideSeconds() -> None:
   override_minutes = 20
   default_minutes = 40

   seconds = ScheduleSlotTimeResolver.effective_duration_seconds(
      override_minutes,
      DurationValues.minutes_to_seconds( default_minutes ) )

   assert seconds == DurationValues.minutes_to_seconds( override_minutes )


def Test_EffectiveDurationSeconds_TestMissing_ExpectNone() -> None:
   seconds = ScheduleSlotTimeResolver.effective_duration_seconds( None, None )

   assert seconds is None


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
            end_time=DateValues.add_minutes_to_time( '10:00 AM', DURATION_MINUTES ) ),
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
      ( DateValues.time_value_in_seconds( '9:30 AM' ), DateValues.time_value_in_seconds( '5:00 PM' ) ),
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
   assert slot[ Position.SECOND ] == SAVED_ITINERARY.arrival_time


def Test_ResolveAllowingVisitExtension_TestRequestedStartAfterDeparture_ExpectSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   requested_start = '1:00 PM'
   visit_window = (
      DateValues.time_value_in_seconds( DAY_OPEN ),
      DateValues.time_value_in_seconds( '12:00 PM' ) )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SavedItinerary(
         date_value='2026-06-15',
         arrival_time=DAY_OPEN,
         departure_time='12:00 PM' ),
      visit_window,
      DURATION_SECONDS,
      start_time=requested_start,
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert error is None
   assert slot == (
      DateValues.normalize_schedule_time( requested_start ),
      DateValues.add_minutes_to_time( requested_start, DURATION_MINUTES ) )


def Test_ResolveAllowingVisitExtension_TestPackAfterFullVisitWindow_ExpectAfterVisitSlot(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion_start = DAY_OPEN
   lion_end = DateValues.add_minutes_to_time( lion_start, DURATION_MINUTES )
   duration_minutes = 7
   short_visit_window = (
      DateValues.time_value_in_seconds( lion_start ),
      DateValues.time_value_in_seconds( lion_end ) )
   blocked_itinerary = ItineraryBuilder.build(
      date='2026-06-15',
      selected_exhibits=[],
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time=lion_start,
            end_time=lion_end ),
      ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=lion_start,
      departure_time=lion_end )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: blocked_itinerary )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SavedItinerary(
         date_value='2026-06-15',
         arrival_time=lion_start,
         departure_time=lion_end ),
      short_visit_window,
      DurationValues.minutes_to_seconds( duration_minutes ),
      start_time=None,
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert error is None
   assert slot == (
      lion_end,
      DateValues.add_minutes_to_time( lion_end, duration_minutes ) )


def Test_Resolve_TestPackAfterScheduledLion_ExpectLaterSlot(
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
            end_time=DateValues.add_minutes_to_time( '10:00 AM', DURATION_MINUTES ) ),
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

   lion_start = '10:00 AM'
   lion_end = DateValues.add_minutes_to_time( lion_start, DURATION_MINUTES )
   duration_minutes = 7

   slot, error = ScheduleSlotTimeResolver.resolve(
      schedule_conn,
      SavedItinerary(
         date_value='2026-06-15',
         arrival_time=DAY_OPEN,
         departure_time=DAY_CLOSE ),
      (
         DateValues.time_value_in_seconds( DAY_OPEN ),
         DateValues.time_value_in_seconds( DAY_CLOSE ) ),
      DurationValues.minutes_to_seconds( duration_minutes ),
      start_time=None,
      itinerary_context={},
      earliest_start_seconds=DateValues.time_value_in_seconds( lion_end ) )

   assert error is None
   assert slot == (
      lion_end,
      DateValues.add_minutes_to_time( lion_end, duration_minutes ) )


def Test_ResolveAllowingVisitExtension_TestUnexpectedResolveError_ExpectPropagated(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   unexpected_error = ItinerarySaveResult(
      status=ItineraryErrorType.SAVE_FAILED,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ScheduleSlotTimeResolver,
      'resolve',
      lambda conn, saved_itinerary, window, duration_seconds, **kwargs: ( None, unexpected_error ) )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SAVED_ITINERARY,
      VISIT_WINDOW,
      DURATION_SECONDS,
      start_time=None,
      itinerary_context={} )

   assert slot is None
   assert error is not None
   assert error.status == ItineraryErrorType.SAVE_FAILED


def Test_ResolveAllowingVisitExtension_TestZooHoursPrepareFailure_ExpectOriginalError(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   original_error = ItinerarySaveResult(
      status=ItineraryErrorType.NO_AVAILABLE_SLOT,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ScheduleSlotTimeResolver,
      'resolve',
      lambda conn, saved_itinerary, window, duration_seconds, **kwargs: ( None, original_error ) )
   monkeypatch.setattr(
      ScheduleWindowPreparer,
      'prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: original_error )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SAVED_ITINERARY,
      VISIT_WINDOW,
      DURATION_SECONDS,
      start_time=None,
      itinerary_context={} )

   assert slot is None
   assert error is not None
   assert error.status == ItineraryErrorType.NO_AVAILABLE_SLOT


def Test_ResolveAllowingVisitExtension_TestExtensionSearchFails_ExpectOriginalError(
      schedule_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   original_error = ItinerarySaveResult(
      status=ItineraryErrorType.NO_AVAILABLE_SLOT,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ScheduleSlotTimeResolver,
      'resolve',
      lambda conn, saved_itinerary, window, duration_seconds, **kwargs: ( None, original_error ) )
   monkeypatch.setattr(
      ScheduleSlotTimeResolver,
      '_resolve_extension_slot_before_or_after_visit',
      lambda saved_itinerary, **kwargs: None )

   slot, error = ScheduleSlotTimeResolver.resolve_allowing_visit_extension(
      schedule_conn,
      SAVED_ITINERARY,
      VISIT_WINDOW,
      DURATION_SECONDS,
      start_time=None,
      itinerary_context={},
      day_hours_window=DAY_HOURS_WINDOW )

   assert slot is None
   assert error is not None
   assert error.status == ItineraryErrorType.NO_AVAILABLE_SLOT
