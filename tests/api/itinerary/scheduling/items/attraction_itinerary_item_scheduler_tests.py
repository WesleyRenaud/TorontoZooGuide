from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.attractions.scheduling.attraction_hours_schedule_adjustment import AttractionHoursScheduleAdjustment
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.attraction_itinerary_item_scheduler import AttractionItineraryItemScheduler
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.shared.enums import ItineraryErrorType
from api.shared.operating_hours import OperatingHours


SPLASH_ISLAND = 'Splash Island'
VISIT_DATE = date( 2026, 6, 20 )
WEEKEND_HOURS = OperatingHours.from_schedule_times( '12:00 PM', '5:00 PM' )
assert WEEKEND_HOURS is not None

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction=SPLASH_ISLAND,
         old_likelihood=None,
         new_likelihood=100,
      ),
   ],
)

SCHEDULE_ITEM_KEY = AttractionScheduleItemKey( name=SPLASH_ISLAND )

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


def Test_AttractionHoursAdjustmentForRequestedTime_TestBeforeOpen_ExpectBeforeOpen() -> None:
   assert AttractionItineraryItemScheduler._attraction_hours_adjustment_for_requested_time(
      '10:00 AM',
      duration_seconds=60 * 60,
      attraction_hours=WEEKEND_HOURS ) == AttractionHoursScheduleAdjustment.BEFORE_OPEN


def Test_AttractionHoursAdjustmentForRequestedTime_TestAfterClose_ExpectAfterClose() -> None:
   assert AttractionItineraryItemScheduler._attraction_hours_adjustment_for_requested_time(
      '5:30 PM',
      duration_seconds=60 * 60,
      attraction_hours=WEEKEND_HOURS ) == AttractionHoursScheduleAdjustment.AFTER_CLOSE


def Test_AttractionHoursAdjustmentForRequestedTime_TestOverrunClose_ExpectAfterClose() -> None:
   assert AttractionItineraryItemScheduler._attraction_hours_adjustment_for_requested_time(
      '4:30 PM',
      duration_seconds=60 * 60,
      attraction_hours=WEEKEND_HOURS ) == AttractionHoursScheduleAdjustment.AFTER_CLOSE


def Test_AttractionHoursAdjustmentForRequestedTime_TestWithinHours_ExpectNone() -> None:
   assert AttractionItineraryItemScheduler._attraction_hours_adjustment_for_requested_time(
      '1:00 PM',
      duration_seconds=60 * 60,
      attraction_hours=WEEKEND_HOURS ) is None


def Test_ResolveAdjustedAttractionSlot_TestAfterClose_ExpectSlotEndingAtClose(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   slot, error = AttractionItineraryItemScheduler._resolve_adjusted_attraction_slot(
      scheduler_conn,
      SAVED_ITINERARY,
      (
         WEEKEND_HOURS.open_seconds,
         WEEKEND_HOURS.close_seconds,
      ),
      60 * 60,
      hours_adjustment=AttractionHoursScheduleAdjustment.AFTER_CLOSE,
      itinerary_context=ITINERARY_CONTEXT )

   assert error is None
   assert slot == ( '4:00 PM', '5:00 PM' )


def Test_Schedule_TestBeforeOpenWithoutConfirmation_ExpectOutsideHours(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=SAVED_ITINERARY,
      window=( WEEKEND_HOURS.open_seconds, WEEKEND_HOURS.close_seconds ),
      visit_date=VISIT_DATE,
      zoo_operating_hours=WEEKEND_HOURS )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction_name, *, visit_date, zoo_operating_hours: WEEKEND_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ListedScheduleItemPersister.prepare',
      lambda *args, **kwargs: ( [], None ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.AttractionOrTransportationDurationResolver.default_seconds',
      lambda conn, attraction_name: 60 * 60 )

   result = AttractionItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time='10:00 AM', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False )

   assert result.status == ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS


def Test_Schedule_TestCollapsedAttractionWindow_ExpectNoAvailableSlot(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=SAVED_ITINERARY,
      window=( 16 * 3600 + 20 * 60, 16 * 3600 + 25 * 60 ),
      visit_date=VISIT_DATE,
      zoo_operating_hours=OperatingHours.from_schedule_times( '4:00 PM', '4:15 PM' ) )

   assert prepared_window.zoo_operating_hours is not None

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction_name, *, visit_date, zoo_operating_hours: (
         OperatingHours.from_schedule_times( '4:00 PM', '4:15 PM' )
      ) )

   result = AttractionItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False )

   assert result.status == ItineraryErrorType.NO_AVAILABLE_SLOT


def Test_Schedule_TestDefaultTimeAtAttractionOpen_ExpectOpenStart(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoo_hours = OperatingHours.from_schedule_times( '9:30 AM', '5:00 PM' )
   assert zoo_hours is not None
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=SAVED_ITINERARY,
      window=( zoo_hours.open_seconds, zoo_hours.close_seconds ),
      visit_date=VISIT_DATE,
      zoo_operating_hours=zoo_hours )
   committed_times: list[ tuple[ str, str ] ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.AttractionOperatingHoursResolver.fetch_configured_operating_hours_seconds',
      lambda conn, attraction_name, *, visit_date, zoo_operating_hours: WEEKEND_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ListedScheduleItemPersister.prepare',
      lambda *args, **kwargs: ( [], None ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.AttractionOrTransportationDurationResolver.default_seconds',
      lambda conn, attraction_name: 60 * 60 )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_slot_time_resolver.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )

   def commit(
         conn: sqlite3.Connection,
         *,
         schedule_item_key: AttractionScheduleItemKey,
         start_time: str,
         end_time: str,
         insert_if_missing: bool,
         itinerary_context: dict[ str, object ] ) -> ItinerarySaveResult:
      committed_times.append( ( start_time, end_time ) )
      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.attraction_itinerary_item_scheduler.ListedScheduleItemPersister.commit',
      commit )

   result = AttractionItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False,
      confirming_attraction_outside_operating_hours=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '12:00 PM', '1:00 PM' ) ]
