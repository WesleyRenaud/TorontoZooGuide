from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.listed_itinerary_item_scheduler import ListedItineraryItemScheduler
from api.itinerary.scheduling.items.listed_schedule_target import ListedScheduleTarget
from api.itinerary.scheduling.items.parsed_schedule_time_options import ParsedScheduleTimeOptions
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.shared.enums import ItineraryErrorType
from api.shared.operating_hours import OperatingHours


VISIT_DATE = date( 2026, 6, 20 )
VISIT_WINDOW = ( 9 * 3600 + 30 * 60, 17 * 3600 )
ZOO_HOURS = OperatingHours.from_schedule_times( '9:30 AM', '5:00 PM' )
assert ZOO_HOURS is not None

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         new_likelihood=100,
      ),
   ],
)

SCHEDULE_ITEM_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
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


@pytest.fixture
def stub_no_suppressed_status( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )


def _stub_listed_schedule_flow(
      monkeypatch: pytest.MonkeyPatch,
      *,
      saved_itinerary: SavedItinerary = SAVED_ITINERARY,
      default_duration_seconds: int = 8 * 60,
      committed_times: list[ tuple[ str, str ] ] | None = None,
      visit_window: tuple[ int, int ] = VISIT_WINDOW,
      day_hours_window: tuple[ int, int ] | None = None,
      ) -> None:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=visit_window,
      visit_date=VISIT_DATE,
      zoo_operating_hours=ZOO_HOURS )
   zoo_hours_prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=day_hours_window or visit_window,
      visit_date=VISIT_DATE,
      zoo_operating_hours=ZOO_HOURS )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_slot_time_resolver.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: zoo_hours_prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleItemPersister.prepare',
      lambda *args, **kwargs: ( [], None ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleTargetResolver.resolve',
      lambda conn, schedule_item_key: ListedScheduleTarget(
         default_duration_seconds=default_duration_seconds ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   if committed_times is None:
      committed_times = []

   def commit(
         conn: sqlite3.Connection,
         *,
         schedule_item_key: AnimalScheduleItemKey,
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
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleItemPersister.commit',
      commit )


def _stub_listed_schedule_window(
      monkeypatch: pytest.MonkeyPatch,
      *,
      saved_itinerary: SavedItinerary = SAVED_ITINERARY,
      visit_window: tuple[ int, int ] = VISIT_WINDOW,
      ) -> None:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=visit_window,
      visit_date=VISIT_DATE,
      zoo_operating_hours=ZOO_HOURS )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_slot_time_resolver.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )


def Test_Schedule_TestHonorsRequestedStartTime_ExpectExplicitStart(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   _stub_listed_schedule_flow( monkeypatch, committed_times=committed_times )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time='10:00', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '10:00 AM', '10:08 AM' ) ]


def Test_Schedule_TestHonorsRequestedDuration_ExpectExplicitEnd(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   _stub_listed_schedule_flow( monkeypatch, committed_times=committed_times )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time='10:00', duration_minutes=20 ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '10:00 AM', '10:20 AM' ) ]


def Test_Schedule_TestRejectedEarlyAdmissionStart_ExpectRequestedTimeNotAvailable(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_listed_schedule_flow(
      monkeypatch,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time=None,
         departure_time='5:00 PM',
         animal_rows=SAVED_ITINERARY.animal_rows,
      ) )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time='09:00', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE


def Test_Schedule_TestAlreadyScheduledAnimal_ExpectItemAlreadyScheduled(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_listed_schedule_flow(
      monkeypatch,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         animal_rows=[
            ItineraryAnimalRecord(
               species='African Lion',
               exhibit='Africa Savanna',
               new_likelihood=100,
               start_time='10:00 AM',
               end_time='10:08 AM',
            ),
         ],
      ) )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.ITEM_ALREADY_SCHEDULED


def Test_Schedule_TestItemNotOnItinerary_ExpectError(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      stub_no_suppressed_status: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_listed_schedule_window(
      monkeypatch,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.ITEM_NOT_ON_ITINERARY


def Test_Schedule_TestSuppressedItemNotOnItinerary_ExpectSuccess(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   _stub_listed_schedule_window(
      monkeypatch,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, error_type: error_type == ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleTargetResolver.resolve',
      lambda conn, schedule_item_key: ListedScheduleTarget(
         default_duration_seconds=8 * 60 ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel',
      lambda *args, **kwargs: None )

   def commit(
         conn: sqlite3.Connection,
         *,
         schedule_item_key: AnimalScheduleItemKey,
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
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleItemPersister.commit',
      commit )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert result.suppressed_warnings == [ ItineraryErrorType.ITEM_NOT_ON_ITINERARY ]
   assert committed_times == [ ( '9:30 AM', '9:38 AM' ) ]


def Test_Schedule_TestHonorsDurationWithoutTime_ExpectAutoStart(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   _stub_listed_schedule_flow( monkeypatch, committed_times=committed_times )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=20 ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '9:30 AM', '9:50 AM' ) ]


def Test_Schedule_TestRequestedStartAfterDeparture_ExpectExplicitStart(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   _stub_listed_schedule_flow(
      monkeypatch,
      committed_times=committed_times,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='12:00 PM',
         animal_rows=SAVED_ITINERARY.animal_rows,
      ),
      visit_window=( 9 * 3600 + 30 * 60, 12 * 3600 ),
      day_hours_window=( 9 * 3600 + 30 * 60, 17 * 3600 ),
   )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time='1:00 PM', duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '1:00 PM', '1:08 PM' ) ]


def Test_Schedule_TestEarlyAdmissionWindow_ExpectNineAmStart(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   committed_times: list[ tuple[ str, str ] ] = []
   early_admission_window = ( 9 * 3600, 17 * 3600 )
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=SavedItinerary(
         date_value='2026-06-20',
         arrival_time=None,
         departure_time='5:00 PM',
         animal_rows=SAVED_ITINERARY.animal_rows,
      ),
      window=early_admission_window,
      visit_date=VISIT_DATE,
      zoo_operating_hours=ZOO_HOURS )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-20',
         arrival_time=None,
         departure_time='5:00 PM',
         animal_rows=SAVED_ITINERARY.animal_rows,
      ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_slot_time_resolver.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleItemPersister.prepare',
      lambda *args, **kwargs: ( [], None ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleTargetResolver.resolve',
      lambda conn, schedule_item_key: ListedScheduleTarget(
         default_duration_seconds=8 * 60 ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )

   def commit(
         conn: sqlite3.Connection,
         *,
         schedule_item_key: AnimalScheduleItemKey,
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
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ListedScheduleItemPersister.commit',
      commit )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert committed_times == [ ( '9:00 AM', '9:08 AM' ) ]


def Test_Schedule_TestPrepareWindowFailed_ExpectPropagatedResult(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_itinerary_item_scheduler.ScheduleWindowPreparer.prepare',
      lambda conn, saved_itinerary, **context: ItinerarySaveResult(
         status=ItineraryErrorType.ITINERARY_DATE_NOT_SET,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_Schedule_TestMissingDefaultDuration_ExpectSaveFailed(
      scheduler_conn: sqlite3.Connection,
      stub_save_result: None,
      stub_no_suppressed_status: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _stub_listed_schedule_flow(
      monkeypatch,
      default_duration_seconds=None )

   result = ListedItineraryItemScheduler.schedule(
      scheduler_conn,
      SCHEDULE_ITEM_KEY,
      ParsedScheduleTimeOptions( start_time=None, duration_minutes=None ),
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert result.status == ItineraryErrorType.SAVE_FAILED


def Test_WalkNodeIdForListedItem_TestAttractionAlsoTransportation_ExpectTransportNode(
      scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionAlsoTransportationProvider,
      'attraction_is_also_transportation',
      lambda conn, name: True )
   monkeypatch.setattr(
      TransportationWalkNodeResolver,
      'resolve',
      lambda name, legs=None, endpoint=None: 'n-onboard' )

   node_id = ListedItineraryItemScheduler._walk_node_id_for_listed_item(
      scheduler_conn,
      AttractionScheduleItemKey( name='Zoomobile' ) )

   assert node_id == 'n-onboard'


def Test_WalkNodeIdForListedItem_TestAttraction_ExpectAttractionNode(
      scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionAlsoTransportationProvider,
      'attraction_is_also_transportation',
      lambda conn, name: False )
   monkeypatch.setattr(
      ScheduleItemTravelTimeCalculator,
      'walk_node_id_for_attraction',
      lambda name: 'n-carousel' )

   node_id = ListedItineraryItemScheduler._walk_node_id_for_listed_item(
      scheduler_conn,
      AttractionScheduleItemKey( name='Conservation Carousel' ) )

   assert node_id == 'n-carousel'


def Test_WalkNodeIdForListedItem_TestUnknownKey_ExpectNone(
      scheduler_conn: sqlite3.Connection ) -> None:

   assert ListedItineraryItemScheduler._walk_node_id_for_listed_item(
      scheduler_conn,
      GuardiansTalkScheduleItemKey(
         name='African Lion',
         start_time='2:00 PM',
      ),
   ) is None
