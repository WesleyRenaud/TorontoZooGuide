from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_window_packer import LoopWindowPacker
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.shared.calendar_dates import DateValues
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode


ENTRANCE_NODE_ID = 'n-1'
CHEETAH_NODE_ID = 'n-cheetah'
INDO_LOOP_ID = 'indo_malaya'

CHEETAH_DWELL_SECONDS = 300
CHEETAH_APPROACH_SECONDS = 360


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
      _node( CHEETAH_NODE_ID, 10.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
   ],
}


def _seconds( schedule_time: str | None ) -> int:
   value = DateValues.time_value_in_seconds( schedule_time )
   assert value is not None

   return value


def _indo_prepared_unit() -> PreparedLoopScheduleUnit:
   cheetah = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
      enclosure_name=None,
      old_likelihood=None,
      new_likelihood=100 )

   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=INDO_LOOP_ID,
         stops=[ cheetah ],
         entry_walk_node_id=CHEETAH_NODE_ID,
         exit_walk_node_id=CHEETAH_NODE_ID,
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=CHEETAH_DWELL_SECONDS )


def Test_Pack_TestWindowTooSmallForApproach_ExpectEmpty() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '9:05 AM' )

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ _indo_prepared_unit() ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert packed_units == []
   assert CHEETAH_APPROACH_SECONDS + CHEETAH_DWELL_SECONDS > (
      window_end_seconds - window_start_seconds )


def Test_Pack_TestWindowCoversApproachAndDwell_ExpectPackedUnit() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '9:11 AM' )

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ _indo_prepared_unit() ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ INDO_LOOP_ID ]


def Test_Pack_TestFromEntryNode_ExpectDwellOnlyFit() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '9:05 AM' )
   indo_unit = _indo_prepared_unit()

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=CHEETAH_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ INDO_LOOP_ID ]
