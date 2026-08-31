from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_window_packer import LoopWindowPacker
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.shared.calendar_dates import DateValues
from api.walk_graph.domain.master_route_loop import TWO_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode
from api.walk_graph.shortest_path_calculator import ShortestPathCalculator


ENTRANCE_NODE_ID = 'n-1'
CHEETAH_NODE_ID = 'n-cheetah'
INDO_LOOP_ID = 'indo_malaya'
AUSTRALASIA_LOOP_ID = 'australasia'
TEMPLE_NODE_ID = 'n-temple'
HIGHLAND_NODE_ID = 'n-highland'
TUR_NODE_ID = 'n-tur'
EURASIA_LOOP_ID = 'eurasia'

CHEETAH_DWELL_SECONDS = 300
CHEETAH_APPROACH_SECONDS = 360
AUSTRALASIA_DWELL_SECONDS = 120
INDO_DWELL_SECONDS = 300
EURASIA_DWELL_SECONDS = 600


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

ORIENTATION_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( TEMPLE_NODE_ID, 0.0, 0.0 ),
      _node( HIGHLAND_NODE_ID, 20.0, 0.0 ),
      _node( TUR_NODE_ID, 5.0, 0.0 ),
   ],
   'edges': [
      {
         'from': TEMPLE_NODE_ID,
         'to': HIGHLAND_NODE_ID,
         'length_px': _edge_length_px( 20 ),
      },
      {
         'from': TEMPLE_NODE_ID,
         'to': TUR_NODE_ID,
         'length_px': _edge_length_px( 5 ),
      },
      {
         'from': TUR_NODE_ID,
         'to': HIGHLAND_NODE_ID,
         'length_px': _edge_length_px( 20 ),
      },
   ],
}


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


def _seconds( schedule_time: str | None ) -> int:
   value = DateValues.time_value_in_seconds( schedule_time )
   assert value is not None

   return value


def _prepared_loop_unit(
      *,
      loop_id: str,
      stops: list[ ItineraryAnimalRecord ],
      entry_walk_node_id: str,
      exit_walk_node_id: str,
      duration_seconds: int,
      side_cluster_id: str | None = None,
      traversal: str | None = None ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=loop_id,
         stops=stops,
         entry_walk_node_id=entry_walk_node_id,
         exit_walk_node_id=exit_walk_node_id,
         side_cluster_id=side_cluster_id,
         loop_index_in_side_cluster=None,
         traversal=traversal ),
      occupied_seconds=duration_seconds )


def _australasia_prepared_unit() -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
      loop_id=AUSTRALASIA_LOOP_ID,
      stops=[
         ItineraryAnimalRecord(
            species='Kookaburra',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      entry_walk_node_id='n-kookaburra',
      exit_walk_node_id='n-kookaburra',
      duration_seconds=AUSTRALASIA_DWELL_SECONDS,
      side_cluster_id='south' )


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


def Test_Pack_TestOpenWindow_ExpectGreedyShorterLoopFirst() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   window_end_seconds = _seconds( '12:00 PM' )
   australasia_unit = _australasia_prepared_unit()
   indo_unit = _prepared_loop_unit(
      loop_id=INDO_LOOP_ID,
      stops=[
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor',
            enclosure_name=None,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      entry_walk_node_id=CHEETAH_NODE_ID,
      exit_walk_node_id=CHEETAH_NODE_ID,
      duration_seconds=INDO_DWELL_SECONDS,
      side_cluster_id='south' )

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ australasia_unit, indo_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      INDO_LOOP_ID,
      AUSTRALASIA_LOOP_ID,
   ]


def Test_Pack_TestTwoWayLoop_ExpectShorterApproachOrientation() -> None:
   window_start_seconds = _seconds( '2:00 PM' )
   window_end_seconds = _seconds( '5:00 PM' )
   highland = ItineraryAnimalRecord(
      species='Highland Cattle',
      exhibit='Eurasia Wilds',
      enclosure_name=None,
      old_likelihood=None,
      new_likelihood=100 )
   tur = ItineraryAnimalRecord(
      species='West Caucasian Tur',
      exhibit='Eurasia Wilds',
      enclosure_name=None,
      old_likelihood=None,
      new_likelihood=100 )
   eurasia_unit = _prepared_loop_unit(
      loop_id=EURASIA_LOOP_ID,
      stops=[ highland, tur ],
      entry_walk_node_id=HIGHLAND_NODE_ID,
      exit_walk_node_id=TUR_NODE_ID,
      duration_seconds=EURASIA_DWELL_SECONDS,
      traversal=TWO_WAY_LOOP_TRAVERSAL )

   packed_units = LoopWindowPacker.pack(
      ORIENTATION_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=window_end_seconds ),
      prepared_units=[ eurasia_unit ],
      cursor_seconds=window_start_seconds,
      current_node_id=TEMPLE_NODE_ID,
      departure_side_cluster_id='north' )

   assert len( packed_units ) == 1
   packed_unit = packed_units[ 0 ].unit
   assert packed_unit.loop_id == EURASIA_LOOP_ID
   assert packed_unit.entry_walk_node_id == TUR_NODE_ID
   assert packed_unit.exit_walk_node_id == HIGHLAND_NODE_ID
   assert [ animal.species for animal in packed_unit.stops ] == [
      'West Caucasian Tur',
      'Highland Cattle',
   ]

   forward_approach = ShortestPathCalculator.distance(
      ORIENTATION_GRAPH,
      TEMPLE_NODE_ID,
      HIGHLAND_NODE_ID )
   oriented_approach = ShortestPathCalculator.distance(
      ORIENTATION_GRAPH,
      TEMPLE_NODE_ID,
      packed_unit.entry_walk_node_id )

   assert forward_approach is not None
   assert oriented_approach is not None
   assert oriented_approach < forward_approach
