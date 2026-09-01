from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.scheduling.bulk.loop_pin_segment_splitter import LoopPinSegmentSplitter
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.loop_schedule_slot_sink import LoopScheduleSlotSink
from api.itinerary.scheduling.bulk.loop_schedule_stop import LoopScheduleStop
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_unit_attraction_hours_scheduler import LoopUnitAttractionHoursScheduler
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph


SPLASH_ISLAND = 'Splash Island'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
ZOOMOBILE = 'Zoomobile'

SPLASH_OPEN_SECONDS = 12 * 3600
SPLASH_CLOSE_SECONDS = 17 * 3600
ZOO_CLOSE_SECONDS = 19 * 3600

DURATION_SECONDS_BY_STOP: dict[ int, int ] = {}
VIEWING_SPOT_INDEX_BY_ANIMAL: dict[ tuple[ str, str, str | None ], int ] = {}
VIEWING_SPOT_INDEX_BY_ATTRACTION: dict[ str, int ] = {}


def _viewing_spot_index_for_stop(
      loop_id: str,
      stop: LoopScheduleStop.Stop,
      ) -> int | None:
   if isinstance( stop, ItineraryAnimalRecord ):
      return VIEWING_SPOT_INDEX_BY_ANIMAL.get(
         ( stop.species, stop.exhibit, stop.enclosure_name ) )

   if isinstance( stop, ( ItineraryAttractionRecord, ItineraryTransportationRecord ) ):
      return VIEWING_SPOT_INDEX_BY_ATTRACTION.get( stop.attraction )

   return None


def _loop_unit(
      loop_id: str | None,
      stops: list,
   ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops,
      entry_walk_node_id=None,
      exit_walk_node_id=None,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def _splash_attraction() -> ItineraryAttractionRecord:
   return ItineraryAttractionRecord(
      attraction=SPLASH_ISLAND,
      old_likelihood=None,
      new_likelihood=100 )


def _splash_soft_pin(
      *,
      close_seconds: int = SPLASH_CLOSE_SECONDS ) -> AttractionHoursSoftPin:
   return AttractionHoursSoftPin(
      loop_id='splash',
      viewing_spot_index=0,
      attraction_name=SPLASH_ISLAND,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=close_seconds,
   )


@pytest.fixture
def scheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_attraction_hours_scheduling(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   WalkGraphProvider.fetch.cache_clear()
   DURATION_SECONDS_BY_STOP.clear()
   VIEWING_SPOT_INDEX_BY_ANIMAL.clear()
   VIEWING_SPOT_INDEX_BY_ATTRACTION.clear()

   def prepare_stops(
         conn: sqlite3.Connection,
         walk_graph: WalkGraph,
         stops: list[ LoopScheduleStop.Stop ],
      ) -> list[ TimedLoopScheduleStop ]:
      return [
         TimedLoopScheduleStop(
            stop=stop,
            duration_seconds=DURATION_SECONDS_BY_STOP.get( id( stop ), 60 * 60 ),
            travel_before_seconds=0 )
         for stop in stops
      ]

   monkeypatch.setattr( LoopScheduleSlotAssigner, 'prepare_stops', prepare_stops )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'duration_seconds_for_stop',
      lambda conn, stop: DURATION_SECONDS_BY_STOP.get( id( stop ), 60 * 60 ) )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'viewing_spot_index_for_stop',
      _viewing_spot_index_for_stop )


def Test_Schedule_TestEarlyExitCases_ExpectUnchangedCursor() -> None:
   attraction = ItineraryAttractionRecord(
      attraction=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( None, [ attraction ] ),
      occupied_seconds=30 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name=ZOOMOBILE,
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   stops, cursor = LoopUnitAttractionHoursScheduler.schedule(
      object(),
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600

   prepared_with_loop = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'other-loop', [ attraction ] ),
      occupied_seconds=30 * 60 )
   stops, cursor = LoopUnitAttractionHoursScheduler.schedule(
      object(),
      prepared_with_loop,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600

   stops, cursor = LoopUnitAttractionHoursScheduler.schedule(
      object(),
      prepared_with_loop,
      [],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 )
   assert stops == [ attraction ]
   assert cursor == 9 * 3600


def Test_EarliestStartSeconds_TestLoopAndPinCases_ExpectOpenOrNone() -> None:
   attraction = ItineraryAttractionRecord(
      attraction=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name=ZOOMOBILE,
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )

   assert LoopUnitAttractionHoursScheduler.earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( None, [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) is None

   assert LoopUnitAttractionHoursScheduler.earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'other-loop', [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) is None

   assert LoopUnitAttractionHoursScheduler.earliest_start_seconds(
      object(),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'zoomobile', [ attraction ] ),
         occupied_seconds=30 * 60 ),
      [ soft_pin ] ) == 10 * 3600


def Test_AttractionStopHelpers_TestSoftPinMatching_ExpectExpectedStop() -> None:
   attraction = ItineraryAttractionRecord(
      attraction=ZOOMOBILE,
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name=ZOOMOBILE,
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   other = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )

   assert LoopUnitAttractionHoursScheduler._attraction_stop_for_soft_pin(
      [ attraction ],
      soft_pin ) is attraction
   assert LoopUnitAttractionHoursScheduler._attraction_stop_for_soft_pin(
      [ attraction ],
      other ) is None
   assert LoopUnitAttractionHoursScheduler._stop_is_soft_pinned_attraction(
      attraction,
      { ZOOMOBILE } ) is True
   assert LoopUnitAttractionHoursScheduler._still_unscheduled_stops(
      [ attraction ],
      scheduled_stop_ids={ id( attraction ) } ) == []


def Test_Schedule_TestSplashBeforeOpen_ExpectHeldUntilOpen(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   splash = _splash_attraction()
   DURATION_SECONDS_BY_STOP[ id( splash ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ splash ] ),
      occupied_seconds=60 * 60 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ _splash_soft_pin() ],
      blockers=[],
      window_start_seconds=9 * 3600 + 30 * 60,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600 + 30 * 60,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert cursor == 13 * 3600
   assert slot_sink.slots == [ ( splash, '12:00 PM', '1:00 PM' ) ]


def Test_Schedule_TestSplashHoursTooShort_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   splash = _splash_attraction()
   DURATION_SECONDS_BY_STOP[ id( splash ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ splash ] ),
      occupied_seconds=60 * 60 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [
         _splash_soft_pin(
            close_seconds=SPLASH_OPEN_SECONDS + 5 * 60 ),
      ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == [ splash ]
   assert cursor == 9 * 3600
   assert slot_sink.slots == []


def Test_Schedule_TestAttractionPastWindowEnd_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   carousel = ItineraryAttractionRecord(
      attraction='Conservation Carousel',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( carousel ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'carousel', [ carousel ] ),
      occupied_seconds=60 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=15 * 3600,
      window_end_seconds=ZOO_CLOSE_SECONDS,
      cursor_seconds=18 * 3600 + 30 * 60,
      slot_sink=slot_sink )

   assert unscheduled == [ carousel ]
   assert cursor == 18 * 3600 + 30 * 60
   assert slot_sink.slots == []


def Test_Schedule_TestBeforeAnimalsPackedContiguously_ExpectEndingAtAttractionOpen(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   wombat = ItineraryAnimalRecord(
      species='Southern Hairy-Nosed Wombat',
      exhibit='Australasia Pavilion',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( wombat ) ] = 30 * 60
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   VIEWING_SPOT_INDEX_BY_ANIMAL[ (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor',
   ) ] = 0
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ wombat, walk_thru ] ),
      occupied_seconds=90 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert cursor == 13 * 3600
   assert slot_sink.slots == [
      ( wombat, '11:30 AM', '12:00 PM' ),
      ( walk_thru, '12:00 PM', '1:00 PM' ),
   ]


def Test_Schedule_TestLatePlaceZoomobile_ExpectRightAlignedBeforeDeadline(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( zoomobile ) ] = 75 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'zoomobile', [ zoomobile ] ),
      occupied_seconds=75 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name=ZOOMOBILE,
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=SPLASH_OPEN_SECONDS,
      cursor_seconds=10 * 3600,
      late_place=True,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert cursor == SPLASH_OPEN_SECONDS
   assert slot_sink.slots == [ ( zoomobile, '10:45 AM', '12:00 PM' ) ]


def Test_Schedule_TestWeaveAnimalsAroundWalkThru_ExpectBeforeAfterOrdering(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   wombat = ItineraryAnimalRecord(
      species='Southern Hairy-Nosed Wombat',
      exhibit='Australasia Pavilion',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( wombat ) ] = 30 * 60
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 8 * 60
   VIEWING_SPOT_INDEX_BY_ANIMAL[ (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor',
   ) ] = 0
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit(
         'australasia',
         [ wombat, walk_thru, tiger ] ),
      occupied_seconds=98 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert cursor == 13 * 3600 + 8 * 60
   assert slot_sink.slots == [
      ( wombat, '11:30 AM', '12:00 PM' ),
      ( walk_thru, '12:00 PM', '1:00 PM' ),
      ( tiger, '1:00 PM', '1:08 PM' ),
   ]
