from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_slot import LoopScheduleSlot
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_schedule_window_state import LoopScheduleWindowState
from api.itinerary.scheduling.bulk.loop_unit_attraction_hours_scheduler import LoopUnitAttractionHoursScheduler
from api.itinerary.scheduling.bulk.loop_unit_pin_scheduler import LoopUnitPinScheduler
from api.itinerary.scheduling.bulk.loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from api.itinerary.scheduling.bulk.loop_unit_travel_time_calculator import LoopUnitTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_window_packer import LoopWindowPacker
from api.itinerary.scheduling.bulk.master_route_loop_scheduler import MasterRouteLoopScheduler
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode


ENTRANCE_NODE_ID = 'n-1'
GIRAFFE_NODE_ID = 'n-giraffe'
AFRICA_SAVANNA_LOOP_ID = 'africa_savanna'
ZEBRA_TALK_LOOP_ID = 'africa_savanna_zebra_talk'
SPLASH_ISLAND = 'Splash Island'
TALK_START_SECONDS = 11 * 3600
GIRAFFE_DWELL_SECONDS = 8 * 60
GIRAFFE_APPROACH_SECONDS = 6 * 60
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
AUSTRALASIA_LOOP_ID = 'australasia'
ZOOMOBILE_LOOP_ID = 'zoomobile'
KANGAROO_OPEN_SECONDS = 11 * 3600
KANGAROO_CLOSE_SECONDS = 15 * 3600
ZOOMOBILE_OPEN_SECONDS = 10 * 3600
ZOOMOBILE_CLOSE_SECONDS = 18 * 3600
CAMEL_TALK_START_SECONDS = 12 * 3600 + 30 * 60
KANGAROO_DWELL_SECONDS = 60 * 60
ZOOMOBILE_DWELL_SECONDS = 75 * 60
ARRIVAL_SECONDS = 11 * 3600


def _node( node_id: str, x_px: float, y_px: float ) -> WalkGraphNode:
   return {
      'id': node_id,
      'x': x_px / 100.0,
      'y': y_px / 100.0,
      'x_px': x_px,
      'y_px': y_px,
   }


def _edge_length_px( minutes: int ) -> float:
   return minutes * WalkTravelTimeCalculator.WALK_PX_PER_MINUTE


TEST_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( GIRAFFE_NODE_ID, 10.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': GIRAFFE_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
   ],
}


def _loop_unit( loop_id: str | None ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=[],
      entry_walk_node_id=None,
      exit_walk_node_id=None,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def _kangaroo_soft_pin() -> AttractionHoursSoftPin:
   return AttractionHoursSoftPin(
      loop_id=AUSTRALASIA_LOOP_ID,
      viewing_spot_index=1,
      attraction_name=KANGAROO_WALK_THRU,
      open_seconds=KANGAROO_OPEN_SECONDS,
      close_seconds=KANGAROO_CLOSE_SECONDS )


def _zoomobile_soft_pin() -> AttractionHoursSoftPin:
   return AttractionHoursSoftPin(
      loop_id=ZOOMOBILE_LOOP_ID,
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=ZOOMOBILE_OPEN_SECONDS,
      close_seconds=ZOOMOBILE_CLOSE_SECONDS )


def _giraffe_prepared_unit() -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=AFRICA_SAVANNA_LOOP_ID,
         stops=[
            ItineraryAnimalRecord(
               species='Masai Giraffe',
               exhibit='Africa Savanna',
               enclosure_name='Outdoor',
               old_likelihood=None,
               new_likelihood=100 ),
         ],
         entry_walk_node_id=GIRAFFE_NODE_ID,
         exit_walk_node_id=GIRAFFE_NODE_ID,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )


def _zebra_talk_prepared_unit() -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=ZEBRA_TALK_LOOP_ID,
         stops=[],
         entry_walk_node_id=None,
         exit_walk_node_id=None,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=0 )


def _unit_with_stops(
      loop_id: str | None,
      stops: list[ ItineraryAnimalRecord ],
   ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops,
      entry_walk_node_id=ENTRANCE_NODE_ID,
      exit_walk_node_id=ENTRANCE_NODE_ID,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def Test_WaitFillerPackEndSeconds_TestInactiveSoftPins_ExpectReservedPackEnd() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   zoomobile = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, zoomobile ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'face-painting' ),
         occupied_seconds=20 * 60 ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'zoomobile' ),
         occupied_seconds=30 * 60 ),
   ]

   wait_pack_end, planned_active_start = MasterRouteLoopScheduler._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      active_open_seconds=11 * 3600,
      hard_pin_deadline_seconds=None,
      cursor_seconds=9 * 3600 + 15 * 60 )

   assert planned_active_start == 11 * 3600
   assert wait_pack_end == 11 * 3600 - 30 * 60


def Test_WaitFillerPackEndSeconds_TestHardPinDeadline_ExpectCascadedPackEnd() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   carousel = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, carousel ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'face-painting' ),
         occupied_seconds=20 * 60 ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'carousel' ),
         occupied_seconds=15 * 60 ),
   ]

   wait_pack_end, planned_active_start = MasterRouteLoopScheduler._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      active_open_seconds=11 * 3600,
      hard_pin_deadline_seconds=12 * 3600,
      cursor_seconds=9 * 3600 + 15 * 60 )

   assert planned_active_start == 12 * 3600 - 20 * 60
   assert wait_pack_end == planned_active_start - 15 * 60


def Test_WaitFillerPackEndSeconds_TestSplashOpenDeadline_ExpectZoomobilePackedBeforeOpen() -> None:
   splash = AttractionHoursSoftPin(
      loop_id='splash',
      viewing_spot_index=0,
      attraction_name=SPLASH_ISLAND,
      open_seconds=12 * 3600,
      close_seconds=16 * 3600 )
   zoomobile = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=10 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ splash, zoomobile ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'splash' ),
         occupied_seconds=60 * 60 ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( 'zoomobile' ),
         occupied_seconds=75 * 60 ),
   ]

   wait_pack_end, planned_active_start = MasterRouteLoopScheduler._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ 'splash' },
      hard_pinned_loop_ids=set(),
      active_open_seconds=12 * 3600,
      hard_pin_deadline_seconds=None,
      cursor_seconds=10 * 3600 )

   assert planned_active_start == 12 * 3600
   assert wait_pack_end == 12 * 3600 - 75 * 60


def Test_DrainCascadedInactiveSoftPinLoopUnits_TestNoActiveOpen_ExpectNoop() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[] )

   assert MasterRouteLoopScheduler._drain_cascaded_inactive_soft_pin_loop_units(
      object(),
      [],
      schedule_window,
      active_soft_pin_loop_ids=set(),
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      blockers=[],
      cursor_seconds=9 * 3600,
      current_node_id='entrance',
      walk_graph=object(),
      cascade_end_seconds=11 * 3600 ) == ( 9 * 3600, 'entrance' )


def Test_DrainCascadedInactiveSoftPinLoopUnits_TestUnreadyUnit_ExpectNoop() -> None:
   active = AttractionHoursSoftPin(
      loop_id='face-painting',
      viewing_spot_index=0,
      attraction_name='Face Painting',
      open_seconds=11 * 3600,
      close_seconds=16 * 3600 )
   carousel = AttractionHoursSoftPin(
      loop_id='carousel',
      viewing_spot_index=0,
      attraction_name='Conservation Carousel',
      open_seconds=9 * 3600 + 30 * 60,
      close_seconds=18 * 3600 )
   zoomobile = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
      open_seconds=10 * 3600,
      close_seconds=18 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ active, carousel, zoomobile ] )
   unready = PreparedLoopScheduleUnit(
      unit=_loop_unit( 'carousel' ),
      occupied_seconds=15 * 60 )

   assert MasterRouteLoopScheduler._drain_cascaded_inactive_soft_pin_loop_units(
      object(),
      [ unready ],
      schedule_window,
      active_soft_pin_loop_ids={ 'face-painting' },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( unready ): 10 * 3600 },
      blockers=[],
      cursor_seconds=9 * 3600,
      current_node_id='entrance',
      walk_graph=object(),
      cascade_end_seconds=11 * 3600 ) == ( 9 * 3600, 'entrance' )


def Test_EarliestPinnedLoopWaitSeconds_TestMixedPinnedUnits_ExpectEarliestAfterCursor() -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   remaining_units = [ giraffe, zebra_talk ]
   pinned_cache = {
      id( zebra_talk ): TALK_START_SECONDS,
   }

   wait_seconds = MasterRouteLoopScheduler._earliest_pinned_loop_wait_seconds(
      remaining_units,
      { ZEBRA_TALK_LOOP_ID },
      pinned_earliest_start_cache=pinned_cache,
      cursor_seconds=9 * 3600 )

   assert wait_seconds == TALK_START_SECONDS


def Test_EarliestPinnedLoopWaitSeconds_TestNoFuturePin_ExpectNone() -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   pinned_cache = {
      id( zebra_talk ): TALK_START_SECONDS,
   }

   wait_seconds = MasterRouteLoopScheduler._earliest_pinned_loop_wait_seconds(
      [ giraffe, zebra_talk ],
      { ZEBRA_TALK_LOOP_ID },
      pinned_earliest_start_cache=pinned_cache,
      cursor_seconds=TALK_START_SECONDS )

   assert wait_seconds is None


def Test_NonPinnedPackingWindow_TestPinnedTalkBeforeWindowEnd_ExpectCappedEnd() -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   pinned_cache = {
      id( zebra_talk ): TALK_START_SECONDS,
   }

   capped_window = MasterRouteLoopScheduler._non_pinned_packing_window(
      schedule_window,
      remaining_units=[ giraffe, zebra_talk ],
      pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
      pinned_earliest_start_cache=pinned_cache,
      cursor_seconds=9 * 3600 )

   assert capped_window.end_seconds == TALK_START_SECONDS
   assert capped_window.start_seconds == schedule_window.start_seconds


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestFreeLoopBeforeTalk_ExpectRightAlignedPack(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   remaining_units = [ giraffe, zebra_talk ]
   pinned_cache = {
      id( zebra_talk ): TALK_START_SECONDS,
   }
   scheduled_starts: list[ int ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda conn, prepared_unit, **kwargs: (
         scheduled_starts.append( kwargs[ 'start_seconds' ] ) or [] ) )

   next_cursor_seconds, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=remaining_units,
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
         pinned_earliest_start_cache=pinned_cache,
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=LoopScheduleWindowState(
            cursor_seconds=9 * 3600,
            current_node_id=ENTRANCE_NODE_ID,
            departure_side_cluster_id=None ),
         remaining_animals=[] ) )

   assert not should_abort
   assert next_cursor_seconds == TALK_START_SECONDS
   assert scheduled_starts == [ TALK_START_SECONDS - GIRAFFE_DWELL_SECONDS ]
   assert remaining_units == [ zebra_talk ]


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestNoPinnedDeadline_ExpectUnchangedCursor() -> None:
   giraffe = _giraffe_prepared_unit()
   remaining_units = [ giraffe ]
   window_state = LoopScheduleWindowState(
      cursor_seconds=9 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      departure_side_cluster_id=None )

   next_cursor_seconds, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=remaining_units,
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids=set(),
         pinned_earliest_start_cache={},
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=window_state,
         remaining_animals=[] ) )

   assert not should_abort
   assert next_cursor_seconds == 9 * 3600
   assert remaining_units == [ giraffe ]


def Test_ActiveSoftPinLoopIds_TestKangarooAndZoomobile_ExpectKangarooActivated() -> None:
   active_loop_ids = MasterRouteLoopScheduler._active_soft_pin_loop_ids(
      [
         _kangaroo_soft_pin(),
         _zoomobile_soft_pin(),
      ] )

   assert active_loop_ids == { AUSTRALASIA_LOOP_ID }


def Test_InactiveSoftPinLoopIdsBeforeActive_TestZoomobileBeforeKangarooOpen_ExpectZoomobileInactive() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=ARRIVAL_SECONDS,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[
         _kangaroo_soft_pin(),
         _zoomobile_soft_pin(),
      ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
         occupied_seconds=KANGAROO_DWELL_SECONDS ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( ZOOMOBILE_LOOP_ID ),
         occupied_seconds=ZOOMOBILE_DWELL_SECONDS ),
   ]

   inactive_loop_ids = MasterRouteLoopScheduler._inactive_soft_pin_loop_ids_before_active(
      schedule_window,
      remaining_units,
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      active_open_seconds=KANGAROO_OPEN_SECONDS )

   assert inactive_loop_ids == { ZOOMOBILE_LOOP_ID }


def Test_WaitFillerPackEndSeconds_TestKangarooWalkThruAndCamelTalk_ExpectZoomobileReservedBeforeKangarooPlaces() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=ARRIVAL_SECONDS,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[
         _kangaroo_soft_pin(),
         _zoomobile_soft_pin(),
      ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
         occupied_seconds=KANGAROO_DWELL_SECONDS ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( ZOOMOBILE_LOOP_ID ),
         occupied_seconds=ZOOMOBILE_DWELL_SECONDS ),
   ]

   wait_pack_end, planned_active_start = MasterRouteLoopScheduler._wait_filler_pack_end_seconds(
      schedule_window,
      remaining_units=remaining_units,
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      active_open_seconds=KANGAROO_OPEN_SECONDS,
      hard_pin_deadline_seconds=CAMEL_TALK_START_SECONDS,
      cursor_seconds=ARRIVAL_SECONDS )

   assert planned_active_start == CAMEL_TALK_START_SECONDS - KANGAROO_DWELL_SECONDS
   assert wait_pack_end == max(
      ARRIVAL_SECONDS,
      planned_active_start - ZOOMOBILE_DWELL_SECONDS )

LION_ANIMAL = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)
SCHEDULE_START_SECONDS = 9 * 3600
SCHEDULE_END_SECONDS = 17 * 3600
HARD_PIN_LOOP_ID = 'africa_savanna_talk'
HARD_PIN_READY_SECONDS = 11 * 3600
HARD_PIN_DRAIN_CURSOR_SECONDS = 11 * 3600 + 30 * 60

def Test_Schedule_TestPrepareUnitsReturnsNone_ExpectAnimalsReturned(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   loop_units = [ _unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ) ]

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: None )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      loop_units,
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == [ LION_ANIMAL ]
   assert cursor == SCHEDULE_START_SECONDS


def Test_Schedule_TestEmptyWindow_ExpectCursorAtWindowEnd(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ prepared ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ prepared.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_START_SECONDS ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == [ LION_ANIMAL ]
   assert cursor == SCHEDULE_START_SECONDS


def Test_Schedule_TestHardPinReadyDrain_ExpectCursorAdvanced(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   loop_pin = LoopSchedulePin(
      loop_id=HARD_PIN_LOOP_ID,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ GIRAFFE_NODE_ID ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Zebra Talk' ),
      start_seconds=HARD_PIN_READY_SECONDS,
      end_seconds=HARD_PIN_READY_SECONDS + 30 * 60 )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ prepared ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: { id( prepared ): HARD_PIN_READY_SECONDS } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_pack_non_pinned_loops_before_pinned_deadline',
      lambda *_args, **_kwargs: ( HARD_PIN_READY_SECONDS, False ) )
   monkeypatch.setattr(
      LoopUnitPinScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [], HARD_PIN_DRAIN_CURSOR_SECONDS ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ prepared.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            loop_pins=[ loop_pin ] ),
      ],
      schedule_cursor_seconds=HARD_PIN_READY_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == []
   assert cursor == HARD_PIN_DRAIN_CURSOR_SECONDS


def Test_Schedule_TestPersistAbort_ExpectShouldAbortPropagated(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_animal = ItineraryAnimalRecord(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   pinned = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=0 )
   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ free_animal ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   loop_pin = LoopSchedulePin(
      loop_id=HARD_PIN_LOOP_ID,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ GIRAFFE_NODE_ID ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Zebra Talk' ),
      start_seconds=HARD_PIN_READY_SECONDS,
      end_seconds=HARD_PIN_READY_SECONDS + 30 * 60 )

   def _pack_abort(
         *_args: object,
         remaining_animals: list[ ItineraryAnimalRecord ],
         **_kwargs: object,
      ) -> tuple[ int, bool ]:
      remaining_animals.append( free_animal )
      return HARD_PIN_READY_SECONDS, True

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit, pinned ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: { id( pinned ): HARD_PIN_READY_SECONDS } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_pack_non_pinned_loops_before_pinned_deadline',
      _pack_abort )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit, pinned.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            loop_pins=[ loop_pin ] ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert free_animal in remaining
   assert cursor == SCHEDULE_START_SECONDS


def Test_Schedule_TestDeferFreePackingAfterAnchor_ExpectEarlyTrueSkipsAbort(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   anchor_stop = ItineraryStop(
      walk_node_ids=[ GIRAFFE_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Morning Talk',
      start_time='10:00 AM',
      end_time='10:30 AM' )
   defer_calls: list[ bool ] = []

   def _defer( *_args: object, **_kwargs: object ) -> bool:
      defer_calls.append( True )
      return True

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ prepared ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      _defer )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: ( _ for _ in () ).throw(
         AssertionError( 'free packing should be deferred' ) ) )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ prepared.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            anchor_stop=anchor_stop ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert defer_calls == [ True ]
   assert remaining == [ LION_ANIMAL ]
   assert cursor == SCHEDULE_END_SECONDS


def Test_PackingWindowWithActiveSoftPinTailReserve_TestSoftOnlyUnit_ExpectReservedEnd() -> None:
   packing_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )
   kangaroo_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )

   reserved = MasterRouteLoopScheduler._packing_window_with_active_soft_pin_tail_reserve(
      packing_window,
      schedule_window=schedule_window,
      remaining_units=[ kangaroo_unit ],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )

   assert reserved.end_seconds == KANGAROO_CLOSE_SECONDS - KANGAROO_DWELL_SECONDS


def Test_PackingWindowWithActiveSoftPinTailReserve_TestNoSoftUnits_ExpectUnchanged() -> None:
   packing_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )

   reserved = MasterRouteLoopScheduler._packing_window_with_active_soft_pin_tail_reserve(
      packing_window,
      schedule_window=schedule_window,
      remaining_units=[],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )

   assert reserved is packing_window


def Test_PackingWindowWithActiveSoftPinTailReserve_TestHardPinOnly_ExpectUnchanged() -> None:
   packing_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )

   reserved = MasterRouteLoopScheduler._packing_window_with_active_soft_pin_tail_reserve(
      packing_window,
      schedule_window=schedule_window,
      remaining_units=[
         PreparedLoopScheduleUnit(
            unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
            occupied_seconds=KANGAROO_DWELL_SECONDS ),
      ],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids={ AUSTRALASIA_LOOP_ID },
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )

   assert reserved is packing_window


def Test_InactiveSoftPinLoopIdsOpeningBeforeActive_TestZoomobileBeforeKangaroo_ExpectZoomobile() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin(), _zoomobile_soft_pin() ] )
   remaining_units = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
         occupied_seconds=KANGAROO_DWELL_SECONDS ),
      PreparedLoopScheduleUnit(
         unit=_loop_unit( ZOOMOBILE_LOOP_ID ),
         occupied_seconds=ZOOMOBILE_DWELL_SECONDS ),
   ]

   inactive = MasterRouteLoopScheduler._inactive_soft_pin_loop_ids_opening_before_active(
      schedule_window,
      remaining_units,
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      cursor_seconds=9 * 3600 )

   assert inactive == { ZOOMOBILE_LOOP_ID }


def Test_BuildConstrainedEarliestStartCache_TestHardAndSoft_ExpectMaxStarts(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   hard_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( HARD_PIN_LOOP_ID ),
      occupied_seconds=30 * 60 )
   soft_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   none_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( None ),
      occupied_seconds=10 * 60 )

   monkeypatch.setattr(
      LoopUnitPinScheduler,
      'earliest_start_seconds',
      lambda *_args, **_kwargs: 11 * 3600 )
   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'earliest_start_seconds',
      lambda *_args, **_kwargs: 10 * 3600 )

   cache = MasterRouteLoopScheduler._build_constrained_earliest_start_cache(
      sqlite3.connect( ':memory:' ),
      [ hard_unit, soft_unit, none_unit ],
      [
         ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600,
            loop_pins=[
               LoopSchedulePin(
                  loop_id=HARD_PIN_LOOP_ID,
                  viewing_spot_index=0,
                  stop=ItineraryStop(
                     walk_node_ids=[ GIRAFFE_NODE_ID ],
                     schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
                     item_key='Talk' ),
                  start_seconds=11 * 3600,
                  end_seconds=11 * 3600 + 30 * 60 ),
            ],
            attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      ] )

   assert cache[ id( hard_unit ) ] == 11 * 3600
   assert cache[ id( soft_unit ) ] == 10 * 3600
   assert id( none_unit ) not in cache


def Test_SideClusterSuccessorLoopIds_TestPinnedNeighbor_ExpectSuccessor() -> None:
   savanna = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id='africa_savanna',
         stops=[],
         entry_walk_node_id=None,
         exit_walk_node_id=None,
         side_cluster_id='south',
         loop_index_in_side_cluster=0,
         traversal=None ),
      occupied_seconds=20 * 60 )
   giraffe = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id='africa_giraffe',
         stops=[],
         entry_walk_node_id=None,
         exit_walk_node_id=None,
         side_cluster_id='south',
         loop_index_in_side_cluster=1,
         traversal=None ),
      occupied_seconds=20 * 60 )

   successors = MasterRouteLoopScheduler._side_cluster_successor_loop_ids(
      [ savanna, giraffe ],
      { 'africa_savanna' } )

   assert successors == { 'africa_giraffe' }


def Test_LaterSameClusterLoopIds_TestGreenhouseAfterWalkThru_ExpectGreenhouse() -> None:
   walk_thru = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=AUSTRALASIA_LOOP_ID,
         stops=[],
         entry_walk_node_id=None,
         exit_walk_node_id=None,
         side_cluster_id='north',
         loop_index_in_side_cluster=0,
         traversal=None ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   greenhouse = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id='greenhouse',
         stops=[],
         entry_walk_node_id=None,
         exit_walk_node_id=None,
         side_cluster_id='north',
         loop_index_in_side_cluster=1,
         traversal=None ),
      occupied_seconds=20 * 60 )

   later = MasterRouteLoopScheduler._later_same_cluster_loop_ids(
      [ walk_thru, greenhouse ],
      { AUSTRALASIA_LOOP_ID } )

   assert later == { 'greenhouse' }


def Test_ShouldPackOpenSoftPinsWithFreeLoops_TestOpenSoftPin_ExpectTrue() -> None:
   free_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
      occupied_seconds=20 * 60 )

   assert MasterRouteLoopScheduler._should_pack_open_soft_pins_with_free_loops(
      remaining_units=[ free_unit ],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      held_constrained_loop_ids={ AUSTRALASIA_LOOP_ID },
      wait_filler_pending=False,
      hard_pin_deadline_seconds=None,
      active_open_seconds=10 * 3600,
      cursor_seconds=11 * 3600 )


def Test_ShouldPackOpenSoftPinsWithFreeLoops_TestWaitFillerPending_ExpectFalse() -> None:
   assert not MasterRouteLoopScheduler._should_pack_open_soft_pins_with_free_loops(
      remaining_units=[],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      held_constrained_loop_ids=set(),
      wait_filler_pending=True,
      hard_pin_deadline_seconds=None,
      active_open_seconds=10 * 3600,
      cursor_seconds=11 * 3600 )


def Test_DrainReadySoftPinLoopUnits_TestReadySoftPin_ExpectRemovedAndCursorAdvanced(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   soft_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   remaining = [ soft_unit ]
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )

   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [], 12 * 3600 ) )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   cursor, node_id = MasterRouteLoopScheduler._drain_ready_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      schedule_window,
      soft_only_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( soft_unit ): 11 * 3600 },
      blockers=[],
      cursor_seconds=11 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH,
      late_place=False )

   assert remaining == []
   assert cursor == 12 * 3600
   assert node_id == ENTRANCE_NODE_ID


def Test_DrainReadySoftPinLoopUnits_TestPartialProgress_ExpectReplacementKept(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   soft_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   remaining = [ soft_unit ]
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [ cheetah ], 11 * 3600 + 20 * 60 ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_keep_partial_soft_pin_loop_progress',
      lambda *_args, **_kwargs: (
         remaining.__setitem__( 0, replacement ) or True ) )

   cursor, _node_id = MasterRouteLoopScheduler._drain_ready_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      schedule_window,
      soft_only_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( soft_unit ): 11 * 3600 },
      blockers=[],
      cursor_seconds=11 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH )

   assert remaining == [ replacement ]
   assert cursor == 11 * 3600 + 20 * 60


def Test_KeepPartialPinnedLoopProgress_TestPartialAnimals_ExpectReplacement(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   remaining = [ prepared ]
   cache: dict[ int, int | None ] = { id( prepared ): 11 * 3600 }
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: replacement )
   monkeypatch.setattr(
      LoopUnitPinScheduler,
      'earliest_start_seconds',
      lambda *_args, **_kwargs: 12 * 3600 )

   kept = MasterRouteLoopScheduler._keep_partial_pinned_loop_progress(
      sqlite3.connect( ':memory:' ),
      remaining,
      prepared,
      unscheduled_animals=[ cheetah ],
      pinned_earliest_start_cache=cache,
      loop_pins=[] )

   assert kept is True
   assert remaining == [ replacement ]
   assert cache[ id( replacement ) ] == 12 * 3600


def Test_KeepPartialPinnedLoopProgress_TestNoProgress_ExpectFalse() -> None:
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   assert not MasterRouteLoopScheduler._keep_partial_pinned_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ prepared ],
      prepared,
      unscheduled_animals=[ LION_ANIMAL ],
      pinned_earliest_start_cache={},
      loop_pins=[] )


def Test_SchedulePreparedLoopUnit_TestPrepareFails_ExpectAnimalsReturned(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: None )

   assert MasterRouteLoopScheduler._schedule_prepared_loop_unit(
      sqlite3.connect( ':memory:' ),
      prepared,
      blockers=[],
      start_seconds=10 * 3600,
      walk_graph=TEST_GRAPH ) == [ LION_ANIMAL ]


def Test_SchedulePreparedLoopUnit_TestSaveFails_ExpectPersistError(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda *_args, **_kwargs: (
         [ LoopScheduleSlot( LION_ANIMAL, '10:00 AM', '10:20 AM' ) ],
         10 * 3600 + 20 * 60,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda *_args, **_kwargs: False )

   with pytest.raises( LoopUnitSchedulePersistError ):
      MasterRouteLoopScheduler._schedule_prepared_loop_unit(
         sqlite3.connect( ':memory:' ),
         prepared,
         blockers=[],
         start_seconds=10 * 3600,
         end_seconds=17 * 3600,
         walk_graph=TEST_GRAPH )


def Test_Schedule_TestSoftPinWaitFillerDrain_ExpectSoftPinScheduled(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ kangaroo ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: { id( kangaroo ): KANGAROO_OPEN_SECONDS } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [], KANGAROO_OPEN_SECONDS + KANGAROO_DWELL_SECONDS ) )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ kangaroo.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      ],
      schedule_cursor_seconds=KANGAROO_OPEN_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == []
   assert cursor == KANGAROO_OPEN_SECONDS + KANGAROO_DWELL_SECONDS


def Test_DrainCascadedInactiveSoftPinLoopUnits_TestReadyInactive_ExpectPlaced(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin(), _zoomobile_soft_pin() ] )
   zoomobile = PreparedLoopScheduleUnit(
      unit=_loop_unit( ZOOMOBILE_LOOP_ID ),
      occupied_seconds=ZOOMOBILE_DWELL_SECONDS )
   remaining = [ zoomobile ]
   match_calls = { 'n': 0 }

   def _matching(
         remaining_units: list[ PreparedLoopScheduleUnit ],
         loop_ids: set[ str ],
      ) -> list[ PreparedLoopScheduleUnit ]:
      match_calls[ 'n' ] += 1

      if match_calls[ 'n' ] == 1:
         return [ zoomobile ]

      return []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_soft_pin_loop_units',
      lambda *_args, **_kwargs: ( 11 * 3600, 'n-exit' ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_units_matching_loop_ids',
      _matching )

   cursor, node_id = MasterRouteLoopScheduler._drain_cascaded_inactive_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      schedule_window,
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( zoomobile ): ZOOMOBILE_OPEN_SECONDS },
      blockers=[],
      cursor_seconds=9 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH,
      cascade_end_seconds=KANGAROO_OPEN_SECONDS )

   assert cursor == 11 * 3600
   assert node_id == 'n-exit'


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestFitsInLaterGap_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
      occupied_seconds=30 * 60 )
   anchor_stop = ItineraryStop(
      walk_node_ids=[ GIRAFFE_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Morning Talk',
      start_time='10:00 AM',
      end_time='10:30 AM' )
   morning = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=10 * 3600,
      anchor_stop=anchor_stop )
   later = ItineraryScheduleWindow(
      start_seconds=10 * 3600 + 30 * 60,
      end_seconds=17 * 3600,
      opens_after_fixed_time_stop=True,
      loop_pins=[
         LoopSchedulePin(
            loop_id=HARD_PIN_LOOP_ID,
            viewing_spot_index=0,
            stop=ItineraryStop(
               walk_node_ids=[ GIRAFFE_NODE_ID ],
               schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
               item_key='Later Talk' ),
            start_seconds=12 * 3600,
            end_seconds=12 * 3600 + 30 * 60 ),
      ] )
   pinned = PreparedLoopScheduleUnit(
      unit=_loop_unit( HARD_PIN_LOOP_ID ),
      occupied_seconds=30 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_pinned_loop_wait_seconds',
      lambda *_args, **_kwargs: 12 * 3600 )

   assert MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      morning,
      later_schedule_windows=[ later ],
      remaining_units=[ free_unit, pinned ],
      held_pinned_loop_ids={ HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={ id( pinned ): 12 * 3600 },
      cursor_seconds=9 * 3600 )


def Test_EarliestHardPinDeadlineSeconds_TestCachedDeadline_ExpectMin() -> None:
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( HARD_PIN_LOOP_ID ),
      occupied_seconds=20 * 60 )

   assert MasterRouteLoopScheduler._earliest_hard_pin_deadline_seconds(
      [ prepared ],
      { HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={ id( prepared ): 11 * 3600 } ) == 11 * 3600


def Test_UnitsMatchingLoopIds_TestEmptyIds_ExpectEmpty() -> None:
   assert MasterRouteLoopScheduler._units_matching_loop_ids(
      [
         PreparedLoopScheduleUnit(
            unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
            occupied_seconds=10 * 60 ),
      ],
      set() ) == []


def Test_KeepPartialSoftPinLoopProgress_TestPartialStops_ExpectReplacement(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   remaining = [ prepared ]
   cache: dict[ int, int | None ] = { id( prepared ): 11 * 3600 }
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: replacement )
   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'earliest_start_seconds',
      lambda *_args, **_kwargs: 12 * 3600 )

   kept = MasterRouteLoopScheduler._keep_partial_soft_pin_loop_progress(
      sqlite3.connect( ':memory:' ),
      remaining,
      prepared,
      unscheduled_stops=[ cheetah ],
      pinned_earliest_start_cache=cache,
      soft_pins=[ _kangaroo_soft_pin() ] )

   assert kept is True
   assert remaining == [ replacement ]
   assert cache[ id( replacement ) ] == 12 * 3600


def Test_PreparedLoopUnitFromStops_TestPrepareFails_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: None )

   assert MasterRouteLoopScheduler._prepared_loop_unit_from_stops(
      sqlite3.connect( ':memory:' ),
      _unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      [ LION_ANIMAL ] ) is None


def Test_PreparedLoopUnitFromStops_TestPrepared_ExpectOccupiedSeconds(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )

   prepared = MasterRouteLoopScheduler._prepared_loop_unit_from_stops(
      sqlite3.connect( ':memory:' ),
      _unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      [ LION_ANIMAL ] )

   assert prepared is not None
   assert prepared.occupied_seconds == 20 * 60
   assert prepared.unit.stops == [ LION_ANIMAL ]


def Test_ScheduleStartSecondsForPackedUnits_TestRightAlign_ExpectWindowEndMinusOccupied(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=12 * 3600 )
   packed = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
         occupied_seconds=30 * 60 ),
   ]

   monkeypatch.setattr(
      LoopUnitTravelTimeCalculator,
      'packed_units_occupied_seconds',
      lambda *_args, **_kwargs: 30 * 60 )

   start = MasterRouteLoopScheduler._schedule_start_seconds_for_packed_units(
      schedule_window,
      packed_units=packed,
      cursor_seconds=9 * 3600,
      walk_graph=TEST_GRAPH,
      current_node_id=ENTRANCE_NODE_ID,
      right_align_to_window_end=True )

   assert start == 12 * 3600 - 30 * 60


def Test_ScheduleStartSecondsForPackedUnits_TestLeftAlign_ExpectWindowStart() -> None:
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=12 * 3600 )
   packed = [
      PreparedLoopScheduleUnit(
         unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
         occupied_seconds=30 * 60 ),
   ]

   start = MasterRouteLoopScheduler._schedule_start_seconds_for_packed_units(
      schedule_window,
      packed_units=packed,
      cursor_seconds=9 * 3600 + 15 * 60,
      walk_graph=TEST_GRAPH,
      current_node_id=ENTRANCE_NODE_ID,
      right_align_to_window_end=False )

   assert start == 9 * 3600 + 15 * 60


def Test_Schedule_TestWaitFillerFreePackThenCascadeSoftPins_ExpectFreeScheduledAndCascaded(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_animal = ItineraryAnimalRecord(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   kangaroo_animal = ItineraryAnimalRecord(
      species='Red Kangaroo',
      exhibit='Australasia',
      old_likelihood=None,
      new_likelihood=100 )
   zoomobile_animal = ItineraryAnimalRecord(
      species='Zoomobile Rider',
      exhibit='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ free_animal ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ kangaroo_animal ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   zoomobile = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( ZOOMOBILE_LOOP_ID, [ zoomobile_animal ] ),
      occupied_seconds=ZOOMOBILE_DWELL_SECONDS )
   cursor_seconds = 9 * 3600 + 15 * 60
   cascade_calls: list[ int ] = []
   soft_drain_calls: list[ dict[ str, object ] ] = []
   pack_calls = { 'n': 0 }

   def _pack( *_args: object, **_kwargs: object ) -> list[ PreparedLoopScheduleUnit ]:
      pack_calls[ 'n' ] += 1

      if pack_calls[ 'n' ] == 1:
         return [ free_unit ]

      return []

   def _drain_cascade(
         *_args: object,
         remaining_units: list[ PreparedLoopScheduleUnit ] | None = None,
         **kwargs: object,
      ) -> tuple[ int, str ]:
      units = remaining_units if remaining_units is not None else _args[ 1 ]
      cascade_calls.append( int( kwargs[ 'cascade_end_seconds' ] ) )
      units[ : ] = [
         prepared_unit
         for prepared_unit in units
         if prepared_unit.unit.loop_id != ZOOMOBILE_LOOP_ID
      ]
      return ( KANGAROO_OPEN_SECONDS, ENTRANCE_NODE_ID )

   def _drain_soft(
         *_args: object,
         remaining_units: list[ PreparedLoopScheduleUnit ] | None = None,
         **kwargs: object,
      ) -> tuple[ int, str ]:
      units = remaining_units if remaining_units is not None else _args[ 1 ]
      soft_drain_calls.append( {
         'late_place': kwargs.get( 'late_place' ),
         'window_end_seconds': kwargs.get( 'window_end_seconds' ),
      } )
      units[ : ] = [
         prepared_unit
         for prepared_unit in units
         if prepared_unit.unit.loop_id != AUSTRALASIA_LOOP_ID
      ]
      return ( KANGAROO_OPEN_SECONDS + KANGAROO_DWELL_SECONDS, ENTRANCE_NODE_ID )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit, kangaroo, zoomobile ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {
         id( kangaroo ): KANGAROO_OPEN_SECONDS,
         id( zoomobile ): ZOOMOBILE_OPEN_SECONDS,
      } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr( LoopWindowPacker, 'pack', _pack )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_cascaded_inactive_soft_pin_loop_units',
      _drain_cascade )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_soft_pin_loop_units',
      _drain_soft )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit, kangaroo.unit, zoomobile.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            attraction_hours_soft_pins=[
               _kangaroo_soft_pin(),
               _zoomobile_soft_pin(),
            ] ),
      ],
      schedule_cursor_seconds=cursor_seconds,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == []
   assert cascade_calls
   assert soft_drain_calls
   assert soft_drain_calls[ 0 ][ 'late_place' ] is False
   assert cursor == KANGAROO_OPEN_SECONDS + KANGAROO_DWELL_SECONDS


def Test_Schedule_TestWaitFillerFreePackWithHardPin_ExpectLatePlaceSoftPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_animal = ItineraryAnimalRecord(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   kangaroo_animal = ItineraryAnimalRecord(
      species='Red Kangaroo',
      exhibit='Australasia',
      old_likelihood=None,
      new_likelihood=100 )
   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ free_animal ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ kangaroo_animal ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   hard_pin = LoopSchedulePin(
      loop_id=HARD_PIN_LOOP_ID,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ GIRAFFE_NODE_ID ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Camel Talk' ),
      start_seconds=CAMEL_TALK_START_SECONDS,
      end_seconds=CAMEL_TALK_START_SECONDS + 30 * 60 )
   soft_drain_calls: list[ dict[ str, object ] ] = []

   def _drain_cascade(
         *_args: object,
         remaining_units: list[ PreparedLoopScheduleUnit ] | None = None,
         **_kwargs: object,
      ) -> tuple[ int, str ]:
      units = remaining_units if remaining_units is not None else _args[ 1 ]
      return ( KANGAROO_OPEN_SECONDS, units and ENTRANCE_NODE_ID or ENTRANCE_NODE_ID )

   def _drain_soft(
         *_args: object,
         remaining_units: list[ PreparedLoopScheduleUnit ] | None = None,
         **kwargs: object,
      ) -> tuple[ int, str ]:
      units = remaining_units if remaining_units is not None else _args[ 1 ]
      soft_drain_calls.append( {
         'late_place': kwargs.get( 'late_place' ),
         'window_end_seconds': kwargs.get( 'window_end_seconds' ),
      } )
      units[ : ] = [
         prepared_unit
         for prepared_unit in units
         if prepared_unit.unit.loop_id != AUSTRALASIA_LOOP_ID
      ]
      return ( CAMEL_TALK_START_SECONDS, ENTRANCE_NODE_ID )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit, kangaroo ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {
         id( kangaroo ): KANGAROO_OPEN_SECONDS,
      } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: CAMEL_TALK_START_SECONDS )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_cascaded_inactive_soft_pin_loop_units',
      _drain_cascade )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_soft_pin_loop_units',
      _drain_soft )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_pinned_loop_units',
      lambda *_args, **_kwargs: CAMEL_TALK_START_SECONDS )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit, kangaroo.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            loop_pins=[ hard_pin ],
            attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      ],
      schedule_cursor_seconds=9 * 3600 + 15 * 60,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == []
   assert soft_drain_calls
   assert soft_drain_calls[ 0 ][ 'late_place' ] is True
   assert soft_drain_calls[ 0 ][ 'window_end_seconds' ] == CAMEL_TALK_START_SECONDS
   assert cursor == CAMEL_TALK_START_SECONDS


def Test_Schedule_TestSnapsStartWalkNodeAndSkipsEmptyWindow_ExpectPackSeesSnappedNode(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   seen_nodes: list[ str ] = []

   def _pack(
         *_args: object,
         current_node_id: str,
         **_kwargs: object,
      ) -> list[ PreparedLoopScheduleUnit ]:
      seen_nodes.append( current_node_id )
      return []

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ prepared ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr( LoopWindowPacker, 'pack', _pack )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ prepared.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=10 * 3600,
            end_seconds=10 * 3600,
            start_walk_node_id=GIRAFFE_NODE_ID ),
         ItineraryScheduleWindow(
            start_seconds=10 * 3600,
            end_seconds=SCHEDULE_END_SECONDS ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert GIRAFFE_NODE_ID in seen_nodes
   assert remaining == [ LION_ANIMAL ]
   assert cursor == SCHEDULE_END_SECONDS


def Test_Schedule_TestPinnedWaitAdvancesCursor_ExpectSoftOpenWait(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   seen_cursors: list[ int ] = []

   def _soft_schedule( *_args: object, **kwargs: object ) -> tuple[ list, int ]:
      cursor_seconds = int( kwargs.get( 'cursor_seconds', 0 ) )
      seen_cursors.append( cursor_seconds )
      return ( [], cursor_seconds + KANGAROO_DWELL_SECONDS )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ kangaroo ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: { id( kangaroo ): KANGAROO_OPEN_SECONDS } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr( LoopWindowPacker, 'pack', lambda *_args, **_kwargs: [] )
   monkeypatch.setattr( LoopUnitAttractionHoursScheduler, 'schedule', _soft_schedule )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ kangaroo.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      ],
      schedule_cursor_seconds=9 * 3600 + 15 * 60,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remaining == []
   assert seen_cursors
   assert seen_cursors[ 0 ] >= KANGAROO_OPEN_SECONDS
   assert cursor == KANGAROO_OPEN_SECONDS + KANGAROO_DWELL_SECONDS


def Test_ProcessScheduleWindow_TestOpenSoftPinHardPinDeadline_ExpectLatePlace(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   remaining = [ kangaroo ]
   soft_drain_kwargs: list[ dict[ str, object ] ] = []

   def _drain_soft( *_args: object, **kwargs: object ) -> tuple[ int, str ]:
      soft_drain_kwargs.append( dict( kwargs ) )
      remaining.clear()
      return ( CAMEL_TALK_START_SECONDS, ENTRANCE_NODE_ID )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_pack_non_pinned_loops_before_pinned_deadline',
      lambda *_args, **_kwargs: ( KANGAROO_OPEN_SECONDS, False ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_pinned_loop_units',
      lambda *_args, **_kwargs: KANGAROO_OPEN_SECONDS )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: CAMEL_TALK_START_SECONDS )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_soft_pin_loop_units',
      _drain_soft )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_pack_open_soft_pins_with_free_loops',
      lambda **_kwargs: False )
   monkeypatch.setattr( LoopWindowPacker, 'pack', lambda *_args, **_kwargs: [] )

   window_state = LoopScheduleWindowState(
      cursor_seconds=KANGAROO_OPEN_SECONDS,
      current_node_id=ENTRANCE_NODE_ID,
      departure_side_cluster_id=None )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=SCHEDULE_START_SECONDS,
      end_seconds=SCHEDULE_END_SECONDS,
      loop_pins=[],
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )

   ok = MasterRouteLoopScheduler._process_schedule_window(
      sqlite3.connect( ':memory:' ),
      remaining_units=remaining,
      schedule_window=schedule_window,
      later_schedule_windows=[],
      pinned_loop_ids={ HARD_PIN_LOOP_ID },
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      held_constrained_loop_ids={ HARD_PIN_LOOP_ID, AUSTRALASIA_LOOP_ID },
      pinned_earliest_start_cache={ id( kangaroo ): KANGAROO_OPEN_SECONDS },
      hours_by_attraction_name={},
      blockers=[],
      walk_graph=TEST_GRAPH,
      window_state=window_state,
      remaining_animals=[] )

   assert ok is True
   assert soft_drain_kwargs
   assert soft_drain_kwargs[ 0 ].get( 'late_place' ) is True
   assert soft_drain_kwargs[ 0 ].get( 'window_end_seconds' ) == CAMEL_TALK_START_SECONDS


def Test_ProcessScheduleWindow_TestPackOpenSoftPins_ExpectHoldsReleased(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   kangaroo = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   packed_loop_ids: list[ list[ str | None ] ] = []

   def _pack(
         *_args: object,
         prepared_units: list[ PreparedLoopScheduleUnit ],
         **_kwargs: object,
      ) -> list[ PreparedLoopScheduleUnit ]:
      packed_loop_ids.append( [ unit.unit.loop_id for unit in prepared_units ] )
      return []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr( LoopWindowPacker, 'pack', _pack )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_soft_pin_loop_units',
      lambda *_args, **_kwargs: ( KANGAROO_OPEN_SECONDS, ENTRANCE_NODE_ID ) )

   window_state = LoopScheduleWindowState(
      cursor_seconds=KANGAROO_OPEN_SECONDS,
      current_node_id=ENTRANCE_NODE_ID,
      departure_side_cluster_id=None )

   MasterRouteLoopScheduler._process_schedule_window(
      sqlite3.connect( ':memory:' ),
      remaining_units=[ free_unit, kangaroo ],
      schedule_window=ItineraryScheduleWindow(
         start_seconds=SCHEDULE_START_SECONDS,
         end_seconds=SCHEDULE_END_SECONDS,
         attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      later_schedule_windows=[],
      pinned_loop_ids=set(),
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      held_constrained_loop_ids={ AUSTRALASIA_LOOP_ID },
      pinned_earliest_start_cache={ id( kangaroo ): KANGAROO_OPEN_SECONDS },
      hours_by_attraction_name={},
      blockers=[],
      walk_graph=TEST_GRAPH,
      window_state=window_state,
      remaining_animals=[] )

   assert packed_loop_ids
   assert AUSTRALASIA_LOOP_ID in packed_loop_ids[ 0 ]
   assert AFRICA_SAVANNA_LOOP_ID in packed_loop_ids[ 0 ]


def Test_ProcessScheduleWindow_TestRemainingHardPin_ExpectLaterSameClusterHeld(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   hard_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )
   later_calls: list[ set[ str ] ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_pack_non_pinned_loops_before_pinned_deadline',
      lambda *_args, **_kwargs: ( HARD_PIN_READY_SECONDS, False ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_pinned_loop_units',
      lambda *_args, **_kwargs: HARD_PIN_READY_SECONDS )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_later_same_cluster_loop_ids',
      lambda remaining_units, loop_ids: later_calls.append( set( loop_ids ) ) or { 'greenhouse' } )
   monkeypatch.setattr( LoopWindowPacker, 'pack', lambda *_args, **_kwargs: [] )

   MasterRouteLoopScheduler._process_schedule_window(
      sqlite3.connect( ':memory:' ),
      remaining_units=[ hard_unit ],
      schedule_window=ItineraryScheduleWindow(
         start_seconds=SCHEDULE_START_SECONDS,
         end_seconds=SCHEDULE_END_SECONDS ),
      later_schedule_windows=[],
      pinned_loop_ids={ HARD_PIN_LOOP_ID },
      active_soft_pin_loop_ids=set(),
      held_constrained_loop_ids={ HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={ id( hard_unit ): HARD_PIN_READY_SECONDS },
      hours_by_attraction_name={},
      blockers=[],
      walk_graph=TEST_GRAPH,
      window_state=LoopScheduleWindowState(
         cursor_seconds=HARD_PIN_READY_SECONDS,
         current_node_id=ENTRANCE_NODE_ID,
         departure_side_cluster_id=None ),
      remaining_animals=[] )

   assert later_calls == [ { HARD_PIN_LOOP_ID } ]


def Test_ProcessScheduleWindow_TestOpensAfterFixed_ExpectSuccessorHolds(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   successor_calls: list[ set[ str ] ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_side_cluster_successor_loop_ids',
      lambda remaining_units, held: (
         successor_calls.append( set( held ) ) or { AFRICA_SAVANNA_LOOP_ID } ) )
   monkeypatch.setattr( LoopWindowPacker, 'pack', lambda *_args, **_kwargs: [] )

   MasterRouteLoopScheduler._process_schedule_window(
      sqlite3.connect( ':memory:' ),
      remaining_units=[ free_unit ],
      schedule_window=ItineraryScheduleWindow(
         start_seconds=SCHEDULE_START_SECONDS,
         end_seconds=SCHEDULE_END_SECONDS,
         opens_after_fixed_time_stop=True ),
      later_schedule_windows=[],
      pinned_loop_ids=set(),
      active_soft_pin_loop_ids=set(),
      held_constrained_loop_ids={ HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={},
      hours_by_attraction_name={},
      blockers=[],
      walk_graph=TEST_GRAPH,
      window_state=LoopScheduleWindowState(
         cursor_seconds=SCHEDULE_START_SECONDS,
         current_node_id=ENTRANCE_NODE_ID,
         departure_side_cluster_id=None ),
      remaining_animals=[] )

   assert successor_calls == [ { HARD_PIN_LOOP_ID } ]


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestOpensAfterFixed_ExpectFalse() -> None:
   assert not MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=10 * 3600,
         opens_after_fixed_time_stop=True ),
      later_schedule_windows=[],
      remaining_units=[],
      held_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestNoAnchor_ExpectFalse() -> None:
   assert not MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=10 * 3600 ),
      later_schedule_windows=[],
      remaining_units=[],
      held_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestBadEndTime_ExpectFalse() -> None:

   anchor_stop = ItineraryStop(
      walk_node_ids=[ GIRAFFE_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Morning Talk',
      start_time='10:00 AM',
      end_time=None )

   assert not MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=10 * 3600,
         anchor_stop=anchor_stop ),
      later_schedule_windows=[],
      remaining_units=[
         PreparedLoopScheduleUnit(
            unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
            occupied_seconds=30 * 60 ),
      ],
      held_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestNoFreeUnits_ExpectFalse() -> None:

   anchor_stop = ItineraryStop(
      walk_node_ids=[ GIRAFFE_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Morning Talk',
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert not MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=10 * 3600,
         anchor_stop=anchor_stop ),
      later_schedule_windows=[],
      remaining_units=[
         PreparedLoopScheduleUnit(
            unit=_loop_unit( HARD_PIN_LOOP_ID ),
            occupied_seconds=30 * 60 ),
      ],
      held_pinned_loop_ids={ HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )


def Test_ShouldDeferFreePackingUntilAfterAnchor_TestGapMismatch_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
      occupied_seconds=30 * 60 )
   anchor_stop = ItineraryStop(
      walk_node_ids=[ GIRAFFE_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Morning Talk',
      start_time='10:00 AM',
      end_time='10:30 AM' )
   morning = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=10 * 3600,
      anchor_stop=anchor_stop )
   # start does not match anchor end -> continue / eventually False
   later_wrong_start = ItineraryScheduleWindow(
      start_seconds=11 * 3600,
      end_seconds=17 * 3600,
      opens_after_fixed_time_stop=True,
      loop_pins=[
         LoopSchedulePin(
            loop_id=HARD_PIN_LOOP_ID,
            viewing_spot_index=0,
            stop=ItineraryStop(
               walk_node_ids=[ GIRAFFE_NODE_ID ],
               schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
               item_key='Later Talk' ),
            start_seconds=12 * 3600,
            end_seconds=12 * 3600 + 30 * 60 ),
      ] )
   later_not_after_fixed = ItineraryScheduleWindow(
      start_seconds=10 * 3600 + 30 * 60,
      end_seconds=17 * 3600,
      opens_after_fixed_time_stop=False,
      loop_pins=[
         LoopSchedulePin(
            loop_id=HARD_PIN_LOOP_ID,
            viewing_spot_index=0,
            stop=ItineraryStop(
               walk_node_ids=[ GIRAFFE_NODE_ID ],
               schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
               item_key='Later Talk' ),
            start_seconds=12 * 3600,
            end_seconds=12 * 3600 + 30 * 60 ),
      ] )
   later_no_pins = ItineraryScheduleWindow(
      start_seconds=10 * 3600 + 30 * 60,
      end_seconds=17 * 3600,
      opens_after_fixed_time_stop=True,
      loop_pins=[] )
   later_no_reserve = ItineraryScheduleWindow(
      start_seconds=10 * 3600 + 30 * 60,
      end_seconds=17 * 3600,
      opens_after_fixed_time_stop=True,
      loop_pins=[
         LoopSchedulePin(
            loop_id=HARD_PIN_LOOP_ID,
            viewing_spot_index=0,
            stop=ItineraryStop(
               walk_node_ids=[ GIRAFFE_NODE_ID ],
               schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
               item_key='Later Talk' ),
            start_seconds=12 * 3600,
            end_seconds=12 * 3600 + 30 * 60 ),
      ] )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_pinned_loop_wait_seconds',
      lambda *_args, **_kwargs: None )

   assert not MasterRouteLoopScheduler._should_defer_free_packing_until_after_anchor(
      morning,
      later_schedule_windows=[
         later_wrong_start,
         later_not_after_fixed,
         later_no_pins,
         later_no_reserve,
      ],
      remaining_units=[ free_unit ],
      held_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=9 * 3600 )


def Test_PackingWindowWithActiveSoftPinTailReserve_TestHardPinClamp_ExpectMinDeadline() -> None:
   packing_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )
   kangaroo_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   hard_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( HARD_PIN_LOOP_ID ),
      occupied_seconds=30 * 60 )
   hard_start = 12 * 3600

   reserved = MasterRouteLoopScheduler._packing_window_with_active_soft_pin_tail_reserve(
      packing_window,
      schedule_window=schedule_window,
      remaining_units=[ kangaroo_unit, hard_unit ],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids={ HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={ id( hard_unit ): hard_start },
      cursor_seconds=9 * 3600 )

   assert reserved.end_seconds == hard_start - KANGAROO_DWELL_SECONDS


def Test_PackingWindowWithActiveSoftPinTailReserve_TestTooTight_ExpectUnchanged() -> None:
   packing_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600 )
   schedule_window = ItineraryScheduleWindow(
      start_seconds=9 * 3600,
      end_seconds=17 * 3600,
      attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] )
   kangaroo_unit = PreparedLoopScheduleUnit(
      unit=_loop_unit( AUSTRALASIA_LOOP_ID ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   cursor = KANGAROO_CLOSE_SECONDS - KANGAROO_DWELL_SECONDS

   reserved = MasterRouteLoopScheduler._packing_window_with_active_soft_pin_tail_reserve(
      packing_window,
      schedule_window=schedule_window,
      remaining_units=[ kangaroo_unit ],
      active_soft_pin_loop_ids={ AUSTRALASIA_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={},
      cursor_seconds=cursor )

   assert reserved is packing_window


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestOpensAfterFixed_ExpectSuccessorHeld(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   successor_calls: list[ set[ str ] ] = []
   scheduled_starts: list[ int ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_side_cluster_successor_loop_ids',
      lambda remaining_units, pinned: (
         successor_calls.append( set( pinned ) ) or set() ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda conn, prepared_unit, **kwargs: (
         scheduled_starts.append( kwargs[ 'start_seconds' ] ) or [] ) )

   next_cursor, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=[ giraffe, zebra_talk ],
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600,
            opens_after_fixed_time_stop=True ),
         pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
         pinned_earliest_start_cache={ id( zebra_talk ): TALK_START_SECONDS },
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=LoopScheduleWindowState(
            cursor_seconds=9 * 3600,
            current_node_id=ENTRANCE_NODE_ID,
            departure_side_cluster_id=None ),
         remaining_animals=[] ) )

   assert not should_abort
   assert successor_calls == [ { ZEBRA_TALK_LOOP_ID } ]
   assert next_cursor == 9 * 3600 + GIRAFFE_DWELL_SECONDS + GIRAFFE_APPROACH_SECONDS
   assert scheduled_starts == [ 9 * 3600 + GIRAFFE_APPROACH_SECONDS ]


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestEmptyNonPinned_ExpectUnchangedCursor() -> None:
   pinned = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )
   window_state = LoopScheduleWindowState(
      cursor_seconds=9 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      departure_side_cluster_id=None )

   next_cursor, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=[ pinned ],
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids={ HARD_PIN_LOOP_ID },
         pinned_earliest_start_cache={ id( pinned ): 11 * 3600 },
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=window_state,
         remaining_animals=[] ) )

   assert not should_abort
   assert next_cursor == 9 * 3600


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestPackFail_ExpectUnchangedCursor(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()

   monkeypatch.setattr(
      LoopWindowPacker,
      'pack_all_before_deadline',
      lambda *_args, **_kwargs: None )

   next_cursor, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=[ giraffe, zebra_talk ],
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
         pinned_earliest_start_cache={ id( zebra_talk ): TALK_START_SECONDS },
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=LoopScheduleWindowState(
            cursor_seconds=9 * 3600,
            current_node_id=ENTRANCE_NODE_ID,
            departure_side_cluster_id=None ),
         remaining_animals=[] ) )

   assert not should_abort
   assert next_cursor == 9 * 3600


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestPersistError_ExpectAbort(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   remaining_animals: list[ ItineraryAnimalRecord ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: ( _ for _ in () ).throw(
         LoopUnitSchedulePersistError( list( giraffe.unit.stops ) ) ) )

   next_cursor, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=[ giraffe, zebra_talk ],
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
         pinned_earliest_start_cache={ id( zebra_talk ): TALK_START_SECONDS },
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=LoopScheduleWindowState(
            cursor_seconds=9 * 3600,
            current_node_id=ENTRANCE_NODE_ID,
            departure_side_cluster_id=None ),
         remaining_animals=remaining_animals ) )

   assert should_abort is True
   assert next_cursor == 9 * 3600
   assert giraffe.unit.stops[ 0 ] in remaining_animals


def Test_PackNonPinnedLoopsBeforePinnedDeadline_TestUnscheduledAnimals_ExpectStop(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   giraffe = _giraffe_prepared_unit()
   zebra_talk = _zebra_talk_prepared_unit()
   remaining_units = [ giraffe, zebra_talk ]
   remaining_animals: list[ ItineraryAnimalRecord ] = []

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: list( giraffe.unit.stops ) )

   next_cursor, should_abort = (
      MasterRouteLoopScheduler._pack_non_pinned_loops_before_pinned_deadline(
         sqlite3.connect( ':memory:' ),
         remaining_units=remaining_units,
         schedule_window=ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
         pinned_loop_ids={ ZEBRA_TALK_LOOP_ID },
         pinned_earliest_start_cache={ id( zebra_talk ): TALK_START_SECONDS },
         hours_by_attraction_name={},
         blockers=[],
         walk_graph=TEST_GRAPH,
         window_state=LoopScheduleWindowState(
            cursor_seconds=9 * 3600,
            current_node_id=ENTRANCE_NODE_ID,
            departure_side_cluster_id=None ),
         remaining_animals=remaining_animals ) )

   assert not should_abort
   assert next_cursor == 9 * 3600
   assert remaining_animals == list( giraffe.unit.stops )
   assert giraffe in remaining_units


def Test_BuildConstrainedEarliestStartCache_TestNoPins_ExpectEmpty() -> None:
   assert MasterRouteLoopScheduler._build_constrained_earliest_start_cache(
      sqlite3.connect( ':memory:' ),
      [
         PreparedLoopScheduleUnit(
            unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
            occupied_seconds=10 * 60 ),
      ],
      [
         ItineraryScheduleWindow(
            start_seconds=9 * 3600,
            end_seconds=17 * 3600 ),
      ] ) == {}


def Test_DrainReadyPinnedLoopUnits_TestPartialProgress_ExpectCursorAdvanced(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   remaining = [ prepared ]
   cache: dict[ int, int | None ] = { id( prepared ): HARD_PIN_READY_SECONDS }
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )
   loop_pin = LoopSchedulePin(
      loop_id=HARD_PIN_LOOP_ID,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ GIRAFFE_NODE_ID ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Talk' ),
      start_seconds=HARD_PIN_READY_SECONDS,
      end_seconds=HARD_PIN_READY_SECONDS + 30 * 60 )

   monkeypatch.setattr(
      LoopUnitPinScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [ cheetah ], HARD_PIN_READY_SECONDS + 10 * 60 ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_keep_partial_pinned_loop_progress',
      lambda *_args, **_kwargs: (
         remaining.__setitem__( 0, replacement ) or True ) )

   cursor = MasterRouteLoopScheduler._drain_ready_pinned_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      ItineraryScheduleWindow(
         start_seconds=SCHEDULE_START_SECONDS,
         end_seconds=SCHEDULE_END_SECONDS,
         loop_pins=[ loop_pin ] ),
      pinned_earliest_start_cache=cache,
      blockers=[],
      cursor_seconds=HARD_PIN_READY_SECONDS )

   assert cursor == HARD_PIN_READY_SECONDS + 10 * 60
   assert remaining == [ replacement ]


def Test_DrainReadySoftPinLoopUnits_TestSoftOnlyNone_ExpectUsesWindowSoftPins(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   soft_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=KANGAROO_DWELL_SECONDS )
   remaining = [ soft_unit ]

   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [], 12 * 3600 ) )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   cursor, node_id = MasterRouteLoopScheduler._drain_ready_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=17 * 3600,
         attraction_hours_soft_pins=[ _kangaroo_soft_pin() ] ),
      soft_only_loop_ids=None,
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( soft_unit ): 11 * 3600 },
      blockers=[],
      cursor_seconds=11 * 3600,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH )

   assert remaining == []
   assert cursor == 12 * 3600
   assert node_id == ENTRANCE_NODE_ID


def Test_DrainReadySoftPinLoopUnits_TestTransportationApproach_ExpectExitNodeUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   zoomobile_stop = ItineraryTransportationRecord(
      transportation='Zoomobile',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   soft_unit = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=ZOOMOBILE_LOOP_ID,
         stops=[ zoomobile_stop ],
         entry_walk_node_id=GIRAFFE_NODE_ID,
         exit_walk_node_id=GIRAFFE_NODE_ID,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=ZOOMOBILE_DWELL_SECONDS )
   remaining = [ soft_unit ]

   monkeypatch.setattr(
      LoopUnitTravelTimeCalculator,
      'approach_seconds_to_unit',
      lambda *_args, **_kwargs: 6 * 60 )
   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [], 12 * 3600 ) )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda remaining_units, prepared_unit: remaining_units.clear() )

   cursor, node_id = MasterRouteLoopScheduler._drain_ready_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=17 * 3600,
         attraction_hours_soft_pins=[ _zoomobile_soft_pin() ] ),
      soft_only_loop_ids={ ZOOMOBILE_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( soft_unit ): ZOOMOBILE_OPEN_SECONDS },
      blockers=[],
      cursor_seconds=ZOOMOBILE_OPEN_SECONDS,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH )

   assert remaining == []
   assert cursor == 12 * 3600
   assert node_id == GIRAFFE_NODE_ID


def Test_DrainReadySoftPinLoopUnits_TestPartialWithApproach_ExpectExitNodeUpdated(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   zoomobile_stop = ItineraryTransportationRecord(
      transportation='Zoomobile',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   leftover = ItineraryTransportationRecord(
      transportation='Zoomobile Leg 2',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )
   soft_unit = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=ZOOMOBILE_LOOP_ID,
         stops=[ zoomobile_stop, leftover ],
         entry_walk_node_id=GIRAFFE_NODE_ID,
         exit_walk_node_id=GIRAFFE_NODE_ID,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=ZOOMOBILE_DWELL_SECONDS )
   remaining = [ soft_unit ]
   replacement = PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=ZOOMOBILE_LOOP_ID,
         stops=[ leftover ],
         entry_walk_node_id=GIRAFFE_NODE_ID,
         exit_walk_node_id=GIRAFFE_NODE_ID,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=30 * 60 )

   monkeypatch.setattr(
      LoopUnitTravelTimeCalculator,
      'approach_seconds_to_unit',
      lambda *_args, **_kwargs: 6 * 60 )
   monkeypatch.setattr(
      LoopUnitAttractionHoursScheduler,
      'schedule',
      lambda *_args, **_kwargs: ( [ leftover ], 11 * 3600 ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_keep_partial_soft_pin_loop_progress',
      lambda *_args, **_kwargs: (
         remaining.__setitem__( 0, replacement ) or True ) )

   cursor, node_id = MasterRouteLoopScheduler._drain_ready_soft_pin_loop_units(
      sqlite3.connect( ':memory:' ),
      remaining,
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=17 * 3600,
         attraction_hours_soft_pins=[ _zoomobile_soft_pin() ] ),
      soft_only_loop_ids={ ZOOMOBILE_LOOP_ID },
      hard_pinned_loop_ids=set(),
      pinned_earliest_start_cache={ id( soft_unit ): ZOOMOBILE_OPEN_SECONDS },
      blockers=[],
      cursor_seconds=ZOOMOBILE_OPEN_SECONDS,
      current_node_id=ENTRANCE_NODE_ID,
      walk_graph=TEST_GRAPH )

   assert cursor == 11 * 3600
   assert node_id == GIRAFFE_NODE_ID
   assert remaining == [ replacement ]


def Test_KeepPartialPinnedLoopProgress_TestReplacementNone_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: None )

   assert not MasterRouteLoopScheduler._keep_partial_pinned_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ prepared ],
      prepared,
      unscheduled_animals=[ cheetah ],
      pinned_earliest_start_cache={},
      loop_pins=[] )


def Test_KeepPartialPinnedLoopProgress_TestUnitMissing_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   other = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ lion ] ),
      occupied_seconds=20 * 60 )
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: replacement )

   assert not MasterRouteLoopScheduler._keep_partial_pinned_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ other ],
      prepared,
      unscheduled_animals=[ cheetah ],
      pinned_earliest_start_cache={},
      loop_pins=[] )


def Test_KeepPartialSoftPinLoopProgress_TestNoProgress_ExpectFalse() -> None:
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   assert not MasterRouteLoopScheduler._keep_partial_soft_pin_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ prepared ],
      prepared,
      unscheduled_stops=[ LION_ANIMAL ],
      pinned_earliest_start_cache={},
      soft_pins=[] )


def Test_KeepPartialSoftPinLoopProgress_TestReplacementNone_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: None )

   assert not MasterRouteLoopScheduler._keep_partial_soft_pin_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ prepared ],
      prepared,
      unscheduled_stops=[ cheetah ],
      pinned_earliest_start_cache={},
      soft_pins=[] )


def Test_KeepPartialSoftPinLoopProgress_TestUnitMissing_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ lion, cheetah ] ),
      occupied_seconds=40 * 60 )
   other = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ lion ] ),
      occupied_seconds=20 * 60 )
   replacement = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AUSTRALASIA_LOOP_ID, [ cheetah ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_prepared_loop_unit_from_stops',
      lambda *_args, **_kwargs: replacement )

   assert not MasterRouteLoopScheduler._keep_partial_soft_pin_loop_progress(
      sqlite3.connect( ':memory:' ),
      [ other ],
      prepared,
      unscheduled_stops=[ cheetah ],
      pinned_earliest_start_cache={},
      soft_pins=[] )


def Test_SoftPinLoopIdsInWindow_TestSoftPins_ExpectLoopIds() -> None:
   assert MasterRouteLoopScheduler._soft_pin_loop_ids_in_window(
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=17 * 3600,
         attraction_hours_soft_pins=[
            _kangaroo_soft_pin(),
            _zoomobile_soft_pin(),
         ] ) ) == { AUSTRALASIA_LOOP_ID, ZOOMOBILE_LOOP_ID }


def Test_EarliestPinnedLoopWaitSeconds_TestNoneCacheEntry_ExpectSkipped() -> None:
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( HARD_PIN_LOOP_ID ),
      occupied_seconds=20 * 60 )

   assert MasterRouteLoopScheduler._earliest_pinned_loop_wait_seconds(
      [ prepared ],
      { HARD_PIN_LOOP_ID },
      pinned_earliest_start_cache={ id( prepared ): None },
      cursor_seconds=9 * 3600 ) is None


def Test_LaterSameClusterLoopIds_TestEmptySoftPins_ExpectEmpty() -> None:
   assert MasterRouteLoopScheduler._later_same_cluster_loop_ids(
      [
         PreparedLoopScheduleUnit(
            unit=_loop_unit( AFRICA_SAVANNA_LOOP_ID ),
            occupied_seconds=10 * 60 ),
      ],
      set() ) == set()


def Test_SchedulePreparedLoopUnit_TestExceedsEndByDuration_ExpectAnimalsReturned(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )

   assert MasterRouteLoopScheduler._schedule_prepared_loop_unit(
      sqlite3.connect( ':memory:' ),
      prepared,
      blockers=[],
      start_seconds=10 * 3600,
      end_seconds=10 * 3600 + 10 * 60,
      walk_graph=TEST_GRAPH ) == [ LION_ANIMAL ]


def Test_SchedulePreparedLoopUnit_TestEmptySlots_ExpectAnimalsReturned(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda *_args, **_kwargs: ( [], 10 * 3600 ) )

   assert MasterRouteLoopScheduler._schedule_prepared_loop_unit(
      sqlite3.connect( ':memory:' ),
      prepared,
      blockers=[],
      start_seconds=10 * 3600,
      end_seconds=17 * 3600,
      walk_graph=TEST_GRAPH ) == [ LION_ANIMAL ]


def Test_SchedulePreparedLoopUnit_TestSlotEndPastWindow_ExpectAnimalsReturned(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda *_args, **_kwargs: (
         [ LoopScheduleSlot( LION_ANIMAL, '10:00 AM', '10:40 AM' ) ],
         10 * 3600 + 40 * 60,
      ) )

   assert MasterRouteLoopScheduler._schedule_prepared_loop_unit(
      sqlite3.connect( ':memory:' ),
      prepared,
      blockers=[],
      start_seconds=10 * 3600,
      end_seconds=10 * 3600 + 30 * 60,
      walk_graph=TEST_GRAPH ) == [ LION_ANIMAL ]


def Test_SchedulePreparedLoopUnit_TestSaveSucceeds_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   prepared = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=20 * 60 )

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         TimedLoopScheduleStop(
            stop=LION_ANIMAL,
            duration_seconds=20 * 60,
            travel_before_seconds=0 ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 20 * 60 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_respecting_attraction_hours',
      lambda *_args, **_kwargs: (
         [ LoopScheduleSlot( LION_ANIMAL, '10:00 AM', '10:20 AM' ) ],
         10 * 3600 + 20 * 60,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda *_args, **_kwargs: True )

   assert MasterRouteLoopScheduler._schedule_prepared_loop_unit(
      sqlite3.connect( ':memory:' ),
      prepared,
      blockers=[],
      start_seconds=10 * 3600,
      end_seconds=17 * 3600,
      walk_graph=TEST_GRAPH ) == []


def Test_Schedule_TestFreePackPersistError_ExpectAbort(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: ( _ for _ in () ).throw(
         LoopUnitSchedulePersistError( [ LION_ANIMAL ] ) ) )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert LION_ANIMAL in remaining
   assert cursor == SCHEDULE_START_SECONDS


def Test_Schedule_TestFreePackOverflow_ExpectBreakWithoutScheduling(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   oversized = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=8 * 3600 )
   schedule_calls = { 'n': 0 }

   def _schedule( *_args: object, **_kwargs: object ) -> list:
      schedule_calls[ 'n' ] += 1
      return []

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ oversized ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [ oversized ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_start_seconds_for_packed_units',
      lambda *_args, **_kwargs: SCHEDULE_START_SECONDS )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      _schedule )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ oversized.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_START_SECONDS + 30 * 60 ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert schedule_calls[ 'n' ] == 0
   assert remaining == [ LION_ANIMAL ]
   assert cursor == SCHEDULE_START_SECONDS + 30 * 60


def Test_Schedule_TestFreePackUnscheduledAnimals_ExpectContinueWithoutRemove(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   remove_calls = { 'n': 0 }

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: {} )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: [ LION_ANIMAL ] )
   monkeypatch.setattr(
      LoopWindowPacker,
      'remove_matching',
      lambda *_args, **_kwargs: remove_calls.__setitem__( 'n', remove_calls[ 'n' ] + 1 ) )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert remove_calls[ 'n' ] == 0
   assert LION_ANIMAL in remaining
   assert cursor == SCHEDULE_END_SECONDS


def Test_Schedule_TestFreePackThenDrainHardPin_ExpectMidPackDrain(
      monkeypatch: pytest.MonkeyPatch ) -> None:

   free_animal = ItineraryAnimalRecord(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   free_unit = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( AFRICA_SAVANNA_LOOP_ID, [ free_animal ] ),
      occupied_seconds=GIRAFFE_DWELL_SECONDS )
   pinned = PreparedLoopScheduleUnit(
      unit=_unit_with_stops( HARD_PIN_LOOP_ID, [ LION_ANIMAL ] ),
      occupied_seconds=30 * 60 )
   loop_pin = LoopSchedulePin(
      loop_id=HARD_PIN_LOOP_ID,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ GIRAFFE_NODE_ID ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Zebra Talk' ),
      start_seconds=HARD_PIN_READY_SECONDS,
      end_seconds=HARD_PIN_READY_SECONDS + 30 * 60 )
   mid_pack_drains = { 'n': 0 }

   def _drain_pinned( *_args: object, **_kwargs: object ) -> int:
      mid_pack_drains[ 'n' ] += 1
      return HARD_PIN_DRAIN_CURSOR_SECONDS

   monkeypatch.setattr(
      LoopWindowPacker,
      'prepare_units',
      lambda *_args, **_kwargs: [ free_unit, pinned ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_build_constrained_earliest_start_cache',
      lambda *_args, **_kwargs: { id( pinned ): HARD_PIN_READY_SECONDS } )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_pack_non_pinned_loops_before_pinned_deadline',
      lambda *_args, **_kwargs: ( SCHEDULE_START_SECONDS, False ) )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_should_defer_free_packing_until_after_anchor',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_earliest_hard_pin_deadline_seconds',
      lambda *_args, **_kwargs: None )
   monkeypatch.setattr(
      LoopWindowPacker,
      'pack',
      lambda *_args, **_kwargs: [ free_unit ] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_schedule_prepared_loop_unit',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr(
      MasterRouteLoopScheduler,
      '_drain_ready_pinned_loop_units',
      _drain_pinned )

   def _remove_matching(
         remaining_units: list[ PreparedLoopScheduleUnit ],
         prepared_unit: PreparedLoopScheduleUnit,
      ) -> None:
      remaining_units[ : ] = [
         unit
         for unit in remaining_units
         if unit is not prepared_unit
      ]

   monkeypatch.setattr( LoopWindowPacker, 'remove_matching', _remove_matching )

   remaining, cursor = MasterRouteLoopScheduler.schedule(
      sqlite3.connect( ':memory:' ),
      [ free_unit.unit, pinned.unit ],
      blockers=[],
      schedule_windows=[
         ItineraryScheduleWindow(
            start_seconds=SCHEDULE_START_SECONDS,
            end_seconds=SCHEDULE_END_SECONDS,
            loop_pins=[ loop_pin ] ),
      ],
      schedule_cursor_seconds=SCHEDULE_START_SECONDS,
      walk_graph=TEST_GRAPH,
      start_node_id=ENTRANCE_NODE_ID )

   assert mid_pack_drains[ 'n' ] >= 2
   assert free_animal not in remaining
