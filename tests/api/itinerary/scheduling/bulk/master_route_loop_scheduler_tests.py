from __future__ import annotations

from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.master_route_loop_scheduler import MasterRouteLoopScheduler
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit


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
