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
from api.itinerary.scheduling.bulk.loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.shared.calendar_dates import DateValues
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph


SPLASH_ISLAND = 'Splash Island'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
ZOOMOBILE = 'Zoomobile'

SPLASH_OPEN_SECONDS = 12 * 3600
SPLASH_CLOSE_SECONDS = 17 * 3600
ZOO_CLOSE_SECONDS = 19 * 3600
TINY_TOUR_END_SECONDS = 11 * 3600 + 30 * 60
HYENA_TALK_START_SECONDS = 14 * 3600
KANGAROO_CLOSE_TIGHT_SECONDS = 12 * 3600 + 30 * 60
CAMEL_TALK_START_SECONDS = 12 * 3600 + 30 * 60
CAMEL_TALK_END_SECONDS = 13 * 3600
CAMEL_ENCOUNTER_START_SECONDS = 15 * 3600 + 30 * 60
GREENHOUSE = 'Greenhouse'

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


def Test_Schedule_TestZoomobileAfterTinyTourBeforeHyenaTalk_ExpectSlotInMiddleWindow(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( zoomobile ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'zoomobile', [ zoomobile ] ),
      occupied_seconds=60 * 60 )
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
      window_start_seconds=TINY_TOUR_END_SECONDS,
      window_end_seconds=HYENA_TALK_START_SECONDS,
      cursor_seconds=TINY_TOUR_END_SECONDS,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert slot_sink.slots
   start_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 1 ] )
   end_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 2 ] )
   assert start_seconds is not None
   assert end_seconds is not None
   assert start_seconds >= TINY_TOUR_END_SECONDS
   assert end_seconds <= HYENA_TALK_START_SECONDS


def Test_Schedule_TestTightKangarooWalkThruHours_ExpectEndingBeforeClose(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru ] ),
      occupied_seconds=60 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=11 * 3600,
      close_seconds=KANGAROO_CLOSE_TIGHT_SECONDS )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=11 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=11 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert slot_sink.slots
   end_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 2 ] )
   assert end_seconds is not None
   assert end_seconds <= KANGAROO_CLOSE_TIGHT_SECONDS


def Test_Schedule_TestKangarooBeforeCamelTalk_ExpectEndingBeforeTalkStart(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru ] ),
      occupied_seconds=60 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=11 * 3600,
      close_seconds=15 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=11 * 3600,
      window_end_seconds=CAMEL_TALK_START_SECONDS,
      cursor_seconds=11 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert slot_sink.slots
   end_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 2 ] )
   assert end_seconds is not None
   assert end_seconds <= CAMEL_TALK_START_SECONDS


def Test_Schedule_TestLatePlaceZoomobileAfterCamelTalk_ExpectSlotBeforeEncounter(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation=ZOOMOBILE,
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( zoomobile ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'zoomobile', [ zoomobile ] ),
      occupied_seconds=60 * 60 )
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
      window_start_seconds=CAMEL_TALK_END_SECONDS,
      window_end_seconds=CAMEL_ENCOUNTER_START_SECONDS,
      cursor_seconds=CAMEL_TALK_END_SECONDS,
      late_place=True,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert slot_sink.slots
   start_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 1 ] )
   end_seconds = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 2 ] )
   assert start_seconds is not None
   assert end_seconds is not None
   assert start_seconds >= CAMEL_TALK_END_SECONDS
   assert end_seconds <= CAMEL_ENCOUNTER_START_SECONDS


def Test_Schedule_TestGreenhouseNearKangarooWalkThru_ExpectAdjacentToWalkThru(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   greenhouse = ItineraryAttractionRecord(
      attraction=GREENHOUSE,
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( greenhouse ) ] = 30 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ GREENHOUSE ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, greenhouse ] ),
      occupied_seconds=90 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=11 * 3600,
      close_seconds=15 * 3600 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=11 * 3600,
      window_end_seconds=CAMEL_TALK_START_SECONDS,
      cursor_seconds=11 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == []
   assert len( slot_sink.slots ) == 2
   walk_thru_start = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 1 ] )
   walk_thru_end = DateValues.time_value_in_seconds( slot_sink.slots[ 0 ][ 2 ] )
   greenhouse_start = DateValues.time_value_in_seconds( slot_sink.slots[ 1 ][ 1 ] )
   greenhouse_end = DateValues.time_value_in_seconds( slot_sink.slots[ 1 ][ 2 ] )
   assert walk_thru_start is not None
   assert walk_thru_end is not None
   assert greenhouse_start is not None
   assert greenhouse_end is not None
   assert walk_thru_start >= 11 * 3600
   assert greenhouse_end <= CAMEL_TALK_START_SECONDS
   assert (
      abs( greenhouse_start - walk_thru_end ) <= 45 * 60
      or abs( greenhouse_end - walk_thru_start ) <= 45 * 60 )


def Test_Schedule_TestPersistErrorFromMissingDuration_ExpectStopsAndUnchangedCursor(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = _splash_attraction()
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ splash ] ),
      occupied_seconds=60 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'duration_seconds_for_stop',
      lambda conn, stop: None )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ _splash_soft_pin() ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ splash ]
   assert cursor == 9 * 3600


def Test_EarliestStartSeconds_TestBeforeStopsPrepared_ExpectOpenMinusOccupied(
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
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )

   earliest = LoopUnitAttractionHoursScheduler.earliest_start_seconds(
      scheduler_conn,
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'australasia', [ wombat, walk_thru ] ),
         occupied_seconds=90 * 60 ),
      [ soft_pin ] )

   assert earliest == SPLASH_OPEN_SECONDS - 30 * 60


def Test_EarliestStartSeconds_TestBeforeStopsPrepareFails_ExpectNone(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   VIEWING_SPOT_INDEX_BY_ANIMAL[ (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor',
   ) ] = 0
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda conn, walk_graph, stops: None )

   assert LoopUnitAttractionHoursScheduler.earliest_start_seconds(
      scheduler_conn,
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'australasia', [ wombat, walk_thru ] ),
         occupied_seconds=90 * 60 ),
      [ soft_pin ] ) is None


def Test_Schedule_TestMissingAttractionStop_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   animal = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( animal ) ] = 5 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ animal ] ),
      occupied_seconds=5 * 60 )
   slot_sink = LoopScheduleSlotSink( persist=False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ _splash_soft_pin() ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600,
      slot_sink=slot_sink )

   assert unscheduled == [ animal ]
   assert cursor == 9 * 3600
   assert slot_sink.slots == []


def Test_Schedule_TestBeforeStopsSaveFails_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, stop_slots, *, slot_sink=None: False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ wombat, walk_thru ]
   assert cursor == 10 * 3600


def Test_Schedule_TestAfterStopsWontFit_ExpectAttractionScheduledAfterUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 60 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, tiger ] ),
      occupied_seconds=120 * 60 )
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
      window_start_seconds=SPLASH_OPEN_SECONDS,
      window_end_seconds=SPLASH_OPEN_SECONDS + 60 * 60,
      cursor_seconds=SPLASH_OPEN_SECONDS,
      slot_sink=slot_sink )

   assert unscheduled == [ tiger ]
   assert cursor == SPLASH_OPEN_SECONDS + 60 * 60
   assert slot_sink.slots == [ ( walk_thru, '12:00 PM', '1:00 PM' ) ]


def Test_Schedule_TestAfterStopsSaveFails_ExpectAttractionKeptAfterUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 8 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, tiger ] ),
      occupied_seconds=68 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   save_results = [ True, False ]

   def save(
         conn: sqlite3.Connection,
         blockers: list,
         stop_slots: list,
         *,
         slot_sink: LoopScheduleSlotSink | None = None ) -> bool:
      return save_results.pop( 0 )

   monkeypatch.setattr( LoopScheduleSlotAssigner, 'save', save )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=SPLASH_OPEN_SECONDS,
      window_end_seconds=17 * 3600,
      cursor_seconds=SPLASH_OPEN_SECONDS,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ tiger ]
   assert cursor == SPLASH_OPEN_SECONDS + 60 * 60 + 8 * 60


def Test_ScheduleStopsAroundAttractionHours_TestNoneLoopId_ExpectPersistError(
      scheduler_conn: sqlite3.Connection ) -> None:
   splash = _splash_attraction()
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( None, [ splash ] ),
      occupied_seconds=60 * 60 )

   with pytest.raises( LoopUnitSchedulePersistError ) as raised:
      LoopUnitAttractionHoursScheduler._schedule_stops_around_attraction_hours(
         scheduler_conn,
         prepared,
         [ _splash_soft_pin() ],
         blockers=[],
         window_start_seconds=9 * 3600,
         window_end_seconds=17 * 3600,
         cursor_seconds=9 * 3600 )

   assert raised.value.stops == [ splash ]


def Test_Schedule_TestBeforeStopsPrepareFails_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda conn, walk_graph, stops: None )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ wombat, walk_thru ]
   assert cursor == 10 * 3600


def Test_Schedule_TestBeforeStopsAssignNone_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_ending_by',
      lambda prepared_stops, *, end_seconds: None )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=10 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ wombat, walk_thru ]
   assert cursor == 10 * 3600


def Test_Schedule_TestAttractionScheduleTimeInvalid_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = _splash_attraction()
   DURATION_SECONDS_BY_STOP[ id( splash ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ splash ] ),
      occupied_seconds=60 * 60 )
   monkeypatch.setattr(
      DateValues,
      'schedule_time_key_from_seconds',
      lambda seconds: None )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ _splash_soft_pin() ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ splash ]
   assert cursor == 9 * 3600


def Test_Schedule_TestAttractionSaveFails_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = _splash_attraction()
   DURATION_SECONDS_BY_STOP[ id( splash ) ] = 60 * 60
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'splash', [ splash ] ),
      occupied_seconds=60 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, stop_slots, *, slot_sink=None: False )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ _splash_soft_pin() ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=9 * 3600,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ splash ]
   assert cursor == 9 * 3600


def Test_Schedule_TestAfterStopsPrepareFails_ExpectAttractionUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 8 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, tiger ] ),
      occupied_seconds=68 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )

   def prepare_stops(
         conn: sqlite3.Connection,
         walk_graph: WalkGraph,
         stops: list[ LoopScheduleStop.Stop ],
      ) -> list[ TimedLoopScheduleStop ] | None:
      if any(
            isinstance( stop, ItineraryAnimalRecord ) and stop.species == 'Amur Tiger'
            for stop in stops ):
         return None
      return [
         TimedLoopScheduleStop(
            stop=stop,
            duration_seconds=DURATION_SECONDS_BY_STOP.get( id( stop ), 60 * 60 ),
            travel_before_seconds=0 )
         for stop in stops
      ]

   monkeypatch.setattr( LoopScheduleSlotAssigner, 'prepare_stops', prepare_stops )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=SPLASH_OPEN_SECONDS,
      window_end_seconds=17 * 3600,
      cursor_seconds=SPLASH_OPEN_SECONDS,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ tiger ]
   assert cursor == SPLASH_OPEN_SECONDS + 60 * 60


def Test_Schedule_TestAfterStopsAssignEmpty_ExpectAttractionUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 8 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, tiger ] ),
      occupied_seconds=68 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda prepared_stops, *, start_seconds, hours_by_attraction_name: ( [], start_seconds ) )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=SPLASH_OPEN_SECONDS,
      window_end_seconds=17 * 3600,
      cursor_seconds=SPLASH_OPEN_SECONDS,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == [ tiger ]
   assert cursor == SPLASH_OPEN_SECONDS + 60 * 60


def Test_Schedule_TestCursorPastWindowEnd_ExpectUnscheduled(
      scheduler_conn: sqlite3.Connection,
      stub_attraction_hours_scheduling: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   walk_thru = ItineraryAttractionRecord(
      attraction=KANGAROO_WALK_THRU,
      old_likelihood=None,
      new_likelihood=100 )
   tiger = ItineraryAnimalRecord(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
      old_likelihood=None,
      new_likelihood=100 )
   DURATION_SECONDS_BY_STOP[ id( walk_thru ) ] = 60 * 60
   DURATION_SECONDS_BY_STOP[ id( tiger ) ] = 8 * 60
   VIEWING_SPOT_INDEX_BY_ATTRACTION[ KANGAROO_WALK_THRU ] = 1
   VIEWING_SPOT_INDEX_BY_ANIMAL[ ( 'Amur Tiger', 'Eurasia Wilds', None ) ] = 2
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'australasia', [ walk_thru, tiger ] ),
      occupied_seconds=68 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='australasia',
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=SPLASH_OPEN_SECONDS,
      close_seconds=16 * 3600 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda prepared_stops, *, start_seconds, hours_by_attraction_name: (
         [
            ( tiger, '1:00 PM', '1:08 PM' ),
         ],
         17 * 3600 + 30 * 60,
      ) )

   unscheduled, cursor = LoopUnitAttractionHoursScheduler.schedule(
      scheduler_conn,
      prepared,
      [ soft_pin ],
      blockers=[],
      window_start_seconds=SPLASH_OPEN_SECONDS,
      window_end_seconds=17 * 3600,
      cursor_seconds=SPLASH_OPEN_SECONDS,
      slot_sink=LoopScheduleSlotSink( persist=False ) )

   assert unscheduled == []
   assert cursor == 17 * 3600 + 30 * 60


def Test_DurationSecondsOrRaise_TestMissingDuration_ExpectPersistError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = _splash_attraction()
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'duration_seconds_for_stop',
      lambda conn, stop: None )

   with pytest.raises( LoopUnitSchedulePersistError ) as raised:
      LoopUnitAttractionHoursScheduler._duration_seconds_or_raise(
         object(),
         splash,
         all_stops=[ splash ] )

   assert raised.value.stops == [ splash ]
