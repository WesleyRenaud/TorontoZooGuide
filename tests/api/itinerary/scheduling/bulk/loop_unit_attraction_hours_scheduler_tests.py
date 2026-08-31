from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_unit_attraction_hours_scheduler import LoopUnitAttractionHoursScheduler
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit


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


def Test_Schedule_TestEarlyExitCases_ExpectUnchangedCursor() -> None:
   attraction = ItineraryAttractionRecord(
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   prepared = PreparedLoopScheduleUnit(
      unit=_loop_unit( None, [ attraction ] ),
      occupied_seconds=30 * 60 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
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
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
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
      attraction='Zoomobile',
      old_likelihood=None,
      new_likelihood=100 )
   soft_pin = AttractionHoursSoftPin(
      loop_id='zoomobile',
      viewing_spot_index=0,
      attraction_name='Zoomobile',
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
      { 'Zoomobile' } ) is True
   assert LoopUnitAttractionHoursScheduler._still_unscheduled_stops(
      [ attraction ],
      scheduled_stop_ids={ id( attraction ) } ) == []
