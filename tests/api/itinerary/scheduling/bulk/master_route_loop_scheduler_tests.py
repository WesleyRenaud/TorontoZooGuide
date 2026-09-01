from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_schedule_window_state import LoopScheduleWindowState
from api.itinerary.scheduling.bulk.master_route_loop_scheduler import MasterRouteLoopScheduler
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
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
