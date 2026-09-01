from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.routing.attraction_hours_soft_pin import AttractionHoursSoftPin
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_window_packer import LoopWindowPacker
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.loop_side_cluster_id import LoopSideClusterId
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
KOOKABURRA_NODE_ID = 'n-kookaburra'
ENCOUNTER_NODE_ID = 'n-encounter'
SOUTH_CLUSTER_ID = 'south'
NORTH_CLUSTER_ID = 'north'
TUNDRA_LOOP_ID = 'tundra_trek'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
KANGAROO_OPEN_SECONDS = 11 * 3600
KANGAROO_CLOSE_GENEROUS_SECONDS = 18 * 3600
KANGAROO_CLOSE_TIGHT_SECONDS = 12 * 3600 + 30 * 60
SIDE_CLUSTER_WINDOW_START_SECONDS = 11 * 3600
SIDE_CLUSTER_WINDOW_END_SECONDS = 18 * 3600
INDO_CLUSTER_DWELL_SECONDS = 20 * 60
AFRICA_CLUSTER_DWELL_SECONDS = 30 * 60
TUNDRA_CLUSTER_DWELL_SECONDS = 25 * 60
KANGAROO_CLUSTER_DWELL_SECONDS = 60 * 60
GIRAFFE_ENCOUNTER_START = '11:00 AM'
GIRAFFE_ENCOUNTER_END = '11:45 AM'
RHINO_ENCOUNTER_START = '9:52 AM'
RHINO_ENCOUNTER_END = '10:37 AM'
TINY_TOUR_END_SECONDS = 11 * 3600 + 30 * 60
HYENA_TALK_START_SECONDS = 14 * 3600
ZOOMOBILE_NODE_ID = 'n-zoomobile'
ZOOMOBILE_LOOP_ID = 'zoomobile'
ZOOMOBILE_DWELL_SECONDS = 60 * 60
SAVANNA_LOOP_ID = 'africa_savanna_canadian_domain'
LION_NODE_ID = 'n-lion'
PENGUIN_NODE_ID = 'n-penguin'
SAVANNA_DWELL_SECONDS = 300

CHEETAH_DWELL_SECONDS = 300
CHEETAH_APPROACH_SECONDS = 360
AUSTRALASIA_DWELL_SECONDS = 120
INDO_DWELL_SECONDS = 300
EURASIA_DWELL_SECONDS = 600
ZEBRA_TALK_START_SECONDS = 11 * 3600
BACTRIAN_CAMELS_START_SECONDS = 15 * 3600 + 30 * 60
RHINO_ENCOUNTER_START_SECONDS = 9 * 3600 + 52 * 60


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
      loop_index_in_side_cluster: int | None = None,
      traversal: str | None = None ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=loop_id,
         stops=stops,
         entry_walk_node_id=entry_walk_node_id,
         exit_walk_node_id=exit_walk_node_id,
         side_cluster_id=side_cluster_id,
         loop_index_in_side_cluster=loop_index_in_side_cluster,
         traversal=traversal ),
      occupied_seconds=duration_seconds )


SMART_PACK_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( KOOKABURRA_NODE_ID, 15.0, 0.0 ),
      _node( CHEETAH_NODE_ID, 25.0, 0.0 ),
      _node( ENCOUNTER_NODE_ID, 28.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': KOOKABURRA_NODE_ID,
         'length_px': _edge_length_px( 8 ),
      },
      {
         'from': KOOKABURRA_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
      {
         'from': CHEETAH_NODE_ID,
         'to': ENCOUNTER_NODE_ID,
         'length_px': _edge_length_px( 2 ),
      },
      {
         'from': ENTRANCE_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': _edge_length_px( 10 ),
      },
   ],
}


SAVANNA_PACK_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( LION_NODE_ID, 10.0, 0.0 ),
      _node( PENGUIN_NODE_ID, 18.0, 0.0 ),
      _node( CHEETAH_NODE_ID, 26.0, 0.0 ),
      _node( ENCOUNTER_NODE_ID, 30.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
      {
         'from': LION_NODE_ID,
         'to': PENGUIN_NODE_ID,
         'length_px': _edge_length_px( 4 ),
      },
      {
         'from': PENGUIN_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': _edge_length_px( 4 ),
      },
      {
         'from': CHEETAH_NODE_ID,
         'to': ENCOUNTER_NODE_ID,
         'length_px': _edge_length_px( 2 ),
      },
   ],
}


ZOOMOBILE_PACK_GRAPH: WalkGraph = {
   'map_width_px': 100,
   'map_height_px': 100,
   'entrance_node_id': ENTRANCE_NODE_ID,
   'nodes': [
      _node( ENTRANCE_NODE_ID, 0.0, 0.0 ),
      _node( ZOOMOBILE_NODE_ID, 12.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': ZOOMOBILE_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
   ],
}


def _encounter_anchor_stop(
      *,
      start_time: str,
      end_time: str ) -> ItineraryStop:
   return ItineraryStop(
      walk_node_ids=[ ENCOUNTER_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key='Masai Giraffe',
      is_fixed_time=True,
      start_time=start_time,
      end_time=end_time )


def _rhino_encounter_anchor_stop() -> ItineraryStop:
   return ItineraryStop(
      walk_node_ids=[ ENCOUNTER_NODE_ID ],
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key='Guardians of White Rhinos',
      meeting_spot='Wild Encounter - Penguin Meeting Spot',
      is_fixed_time=True,
      start_time=RHINO_ENCOUNTER_START,
      end_time=RHINO_ENCOUNTER_END )


def _africa_savanna_prepared_unit() -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
      loop_id=SAVANNA_LOOP_ID,
      stops=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            enclosure_name=None,
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            enclosure_name=None,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      entry_walk_node_id=LION_NODE_ID,
      exit_walk_node_id=CHEETAH_NODE_ID,
      duration_seconds=3 * SAVANNA_DWELL_SECONDS )


def _zoomobile_prepared_unit() -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
      loop_id=ZOOMOBILE_LOOP_ID,
      stops=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            added_as_attraction=True,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      entry_walk_node_id=ZOOMOBILE_NODE_ID,
      exit_walk_node_id=ZOOMOBILE_NODE_ID,
      duration_seconds=ZOOMOBILE_DWELL_SECONDS )


def _kangaroo_soft_pin_schedule_window(
      *,
      close_seconds: int ) -> ItineraryScheduleWindow:
   return ItineraryScheduleWindow(
      start_seconds=SIDE_CLUSTER_WINDOW_START_SECONDS,
      end_seconds=SIDE_CLUSTER_WINDOW_END_SECONDS,
      attraction_hours_soft_pins=[
         AttractionHoursSoftPin(
            loop_id=AUSTRALASIA_LOOP_ID,
            viewing_spot_index=1,
            attraction_name=KANGAROO_WALK_THRU,
            open_seconds=KANGAROO_OPEN_SECONDS,
            close_seconds=close_seconds ),
      ] )


def _cluster_prepared_unit(
      *,
      loop_id: str,
      side_cluster_id: str,
      loop_index_in_side_cluster: int,
      duration_seconds: int ) -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
      loop_id=loop_id,
      stops=[],
      entry_walk_node_id=ENTRANCE_NODE_ID,
      exit_walk_node_id=ENTRANCE_NODE_ID,
      duration_seconds=duration_seconds,
      side_cluster_id=side_cluster_id,
      loop_index_in_side_cluster=loop_index_in_side_cluster )


def _side_cluster_prepared_units() -> list[ PreparedLoopScheduleUnit ]:
   return [
      _cluster_prepared_unit(
         loop_id=INDO_LOOP_ID,
         side_cluster_id=SOUTH_CLUSTER_ID,
         loop_index_in_side_cluster=3,
         duration_seconds=INDO_CLUSTER_DWELL_SECONDS ),
      _cluster_prepared_unit(
         loop_id=SAVANNA_LOOP_ID,
         side_cluster_id=SOUTH_CLUSTER_ID,
         loop_index_in_side_cluster=0,
         duration_seconds=AFRICA_CLUSTER_DWELL_SECONDS ),
      _cluster_prepared_unit(
         loop_id=TUNDRA_LOOP_ID,
         side_cluster_id=NORTH_CLUSTER_ID,
         loop_index_in_side_cluster=1,
         duration_seconds=TUNDRA_CLUSTER_DWELL_SECONDS ),
      _cluster_prepared_unit(
         loop_id=AUSTRALASIA_LOOP_ID,
         side_cluster_id=NORTH_CLUSTER_ID,
         loop_index_in_side_cluster=0,
         duration_seconds=KANGAROO_CLUSTER_DWELL_SECONDS ),
   ]


def _south_australasia_prepared_unit() -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
      loop_id=AUSTRALASIA_LOOP_ID,
      stops=[
         ItineraryAnimalRecord(
            species='Demoiselle Crane',
            exhibit='Australasia Pavilion',
            enclosure_name='Indoor',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      entry_walk_node_id=KOOKABURRA_NODE_ID,
      exit_walk_node_id=KOOKABURRA_NODE_ID,
      duration_seconds=AUSTRALASIA_DWELL_SECONDS,
      side_cluster_id=SOUTH_CLUSTER_ID,
      loop_index_in_side_cluster=0 )


def _south_indo_prepared_unit() -> PreparedLoopScheduleUnit:
   return _prepared_loop_unit(
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
      duration_seconds=CHEETAH_DWELL_SECONDS,
      side_cluster_id=SOUTH_CLUSTER_ID,
      loop_index_in_side_cluster=1 )


def _anchored_pre_encounter_window(
      *,
      start_time: str,
      end_time: str ) -> ItineraryScheduleWindow:
   return ItineraryScheduleWindow(
      start_seconds=_seconds( start_time ),
      end_seconds=_seconds( end_time ),
      anchor_stop=_encounter_anchor_stop(
         start_time=end_time,
         end_time=GIRAFFE_ENCOUNTER_END ) )


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


def Test_PackAllBeforeDeadline_TestSavannaLoopBeforeRhinoEncounter_ExpectPacked() -> None:
   savanna_unit = _africa_savanna_prepared_unit()

   packed_units = LoopWindowPacker.pack_all_before_deadline(
      SAVANNA_PACK_GRAPH,
      prepared_units=[ savanna_unit ],
      window_start_seconds=_seconds( '9:00 AM' ),
      deadline_seconds=RHINO_ENCOUNTER_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   assert packed_units is not None
   assert [ unit.unit.loop_id for unit in packed_units ] == [ SAVANNA_LOOP_ID ]


def Test_Pack_TestRhinoEncounterWindow_ExpectSavannaLoopPackedBeforeAnchor() -> None:
   window_start_seconds = _seconds( '9:00 AM' )

   packed_units = LoopWindowPacker.pack(
      SAVANNA_PACK_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=_seconds( RHINO_ENCOUNTER_START ),
         anchor_stop=_rhino_encounter_anchor_stop() ),
      prepared_units=[ _africa_savanna_prepared_unit() ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ SAVANNA_LOOP_ID ]


def Test_Pack_TestTinyTourToHyenaWindow_ExpectZoomobilePacked() -> None:
   window_start_seconds = TINY_TOUR_END_SECONDS

   packed_units = LoopWindowPacker.pack(
      ZOOMOBILE_PACK_GRAPH,
      ItineraryScheduleWindow(
         start_seconds=window_start_seconds,
         end_seconds=HYENA_TALK_START_SECONDS ),
      prepared_units=[ _zoomobile_prepared_unit() ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ ZOOMOBILE_LOOP_ID ]


def Test_PackAllBeforeDeadline_TestUnitsFitBeforePinnedTalk_ExpectAllPacked() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   indo_unit = _indo_prepared_unit()

   packed_units = LoopWindowPacker.pack_all_before_deadline(
      TEST_GRAPH,
      prepared_units=[ indo_unit ],
      window_start_seconds=window_start_seconds,
      deadline_seconds=ZEBRA_TALK_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   assert packed_units is not None
   assert [ unit.unit.loop_id for unit in packed_units ] == [ INDO_LOOP_ID ]


def Test_PackAllBeforeDeadline_TestUnitsTooLarge_ExpectNone() -> None:
   window_start_seconds = _seconds( '10:50 AM' )
   indo_unit = _indo_prepared_unit()

   packed_units = LoopWindowPacker.pack_all_before_deadline(
      TEST_GRAPH,
      prepared_units=[ indo_unit ],
      window_start_seconds=window_start_seconds,
      deadline_seconds=ZEBRA_TALK_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   assert packed_units is None


def Test_PackAllBeforeDeadline_TestUnpinnedAfternoonEncounter_ExpectPackedToEncounterStart() -> None:
   window_start_seconds = _seconds( '9:30 AM' )
   indo_unit = _indo_prepared_unit()

   packed_units = LoopWindowPacker.pack_all_before_deadline(
      TEST_GRAPH,
      prepared_units=[ indo_unit ],
      window_start_seconds=window_start_seconds,
      deadline_seconds=BACTRIAN_CAMELS_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   assert packed_units is not None
   assert [ unit.unit.loop_id for unit in packed_units ] == [ INDO_LOOP_ID ]


def Test_Pack_TestAnchoredEncounterWindow_ExpectSouthPrefixThenIndoTerminal() -> None:
   window_start_seconds = _seconds( '9:00 AM' )
   packed_units = LoopWindowPacker.pack(
      SMART_PACK_GRAPH,
      _anchored_pre_encounter_window(
         start_time='9:00 AM',
         end_time=GIRAFFE_ENCOUNTER_START ),
      prepared_units=[
         _south_australasia_prepared_unit(),
         _south_indo_prepared_unit(),
      ],
      cursor_seconds=window_start_seconds,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      AUSTRALASIA_LOOP_ID,
      INDO_LOOP_ID,
   ]


def Test_PackLoopsWithTerminalUnit_TestShortWindow_ExpectOnlyTerminalSouthLoop() -> None:
   window_start_seconds = _seconds( '9:30 AM' )
   window_end_seconds = window_start_seconds + 15 * 60
   indo = _south_indo_prepared_unit()

   packed_units = LoopWindowPacker._pack_loops_with_terminal_unit(
      SMART_PACK_GRAPH,
      [ indo ],
      terminal_unit=indo,
      window_start_seconds=window_start_seconds,
      window_end_seconds=window_end_seconds,
      current_node_id=ENTRANCE_NODE_ID,
      anchor_node_id=ENCOUNTER_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [ INDO_LOOP_ID ]


def Test_PackLoopsWithTerminalUnit_TestTightWindowWithPrefixCandidate_ExpectEmpty() -> None:
   window_start_seconds = _seconds( '9:30 AM' )
   window_end_seconds = window_start_seconds + 15 * 60

   packed_units = LoopWindowPacker._pack_loops_with_terminal_unit(
      SMART_PACK_GRAPH,
      [
         _south_australasia_prepared_unit(),
         _south_indo_prepared_unit(),
      ],
      terminal_unit=_south_indo_prepared_unit(),
      window_start_seconds=window_start_seconds,
      window_end_seconds=window_end_seconds,
      current_node_id=ENTRANCE_NODE_ID,
      anchor_node_id=ENCOUNTER_NODE_ID )

   assert packed_units == []


def Test_PackLoopsWithTerminalUnit_TestPrefixAndTerminalFit_ExpectContiguousSouthOrder() -> None:
   window_start_seconds = _seconds( '9:30 AM' )
   window_end_seconds = _seconds( '10:42 AM' )
   australasia = _south_australasia_prepared_unit()
   indo = _south_indo_prepared_unit()

   packed_units = LoopWindowPacker._pack_loops_with_terminal_unit(
      SMART_PACK_GRAPH,
      [ australasia, indo ],
      terminal_unit=indo,
      window_start_seconds=window_start_seconds,
      window_end_seconds=window_end_seconds,
      current_node_id=ENTRANCE_NODE_ID,
      anchor_node_id=ENCOUNTER_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      AUSTRALASIA_LOOP_ID,
      INDO_LOOP_ID,
   ]


def Test_ChooseSideClusterPackingOrder_TestGenerousKangarooHours_ExpectSoftPinClusterLast() -> None:
   prepared_units = _side_cluster_prepared_units()

   sequence, prefer_soft_pin_loop_ids = LoopWindowPacker._choose_side_cluster_packing_order(
      _kangaroo_soft_pin_schedule_window(
         close_seconds=KANGAROO_CLOSE_GENEROUS_SECONDS ),
      prepared_units=prepared_units,
      walk_graph=TEST_GRAPH,
      current_node_id=ENTRANCE_NODE_ID,
      cursor_seconds=SIDE_CLUSTER_WINDOW_START_SECONDS )

   assert sequence == [ LoopSideClusterId.SOUTH, LoopSideClusterId.NORTH ]
   assert prefer_soft_pin_loop_ids is None


def Test_ChooseSideClusterPackingOrder_TestTightKangarooHours_ExpectSoftPinClusterFirst() -> None:
   prepared_units = _side_cluster_prepared_units()

   sequence, prefer_soft_pin_loop_ids = LoopWindowPacker._choose_side_cluster_packing_order(
      _kangaroo_soft_pin_schedule_window(
         close_seconds=KANGAROO_CLOSE_TIGHT_SECONDS ),
      prepared_units=prepared_units,
      walk_graph=TEST_GRAPH,
      current_node_id=ENTRANCE_NODE_ID,
      cursor_seconds=SIDE_CLUSTER_WINDOW_START_SECONDS )

   assert sequence == [ LoopSideClusterId.NORTH, LoopSideClusterId.SOUTH ]
   assert prefer_soft_pin_loop_ids == [ AUSTRALASIA_LOOP_ID ]


def Test_Pack_TestGenerousKangarooHours_ExpectSouthLoopsBeforeAustralasiaSoftPin() -> None:
   prepared_units = _side_cluster_prepared_units()

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      _kangaroo_soft_pin_schedule_window(
         close_seconds=KANGAROO_CLOSE_GENEROUS_SECONDS ),
      prepared_units=prepared_units,
      cursor_seconds=SIDE_CLUSTER_WINDOW_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   packed_loop_ids = [ unit.unit.loop_id for unit in packed_units ]
   south_indices = [
      packed_loop_ids.index( SAVANNA_LOOP_ID ),
      packed_loop_ids.index( INDO_LOOP_ID ),
   ]
   north_indices = [
      packed_loop_ids.index( TUNDRA_LOOP_ID ),
      packed_loop_ids.index( AUSTRALASIA_LOOP_ID ),
   ]

   assert max( south_indices ) < min( north_indices )


def Test_Pack_TestTightKangarooHours_ExpectKangarooAndTundraBeforeAfrica() -> None:
   prepared_units = _side_cluster_prepared_units()

   packed_units = LoopWindowPacker.pack(
      TEST_GRAPH,
      _kangaroo_soft_pin_schedule_window(
         close_seconds=KANGAROO_CLOSE_TIGHT_SECONDS ),
      prepared_units=prepared_units,
      cursor_seconds=SIDE_CLUSTER_WINDOW_START_SECONDS,
      current_node_id=ENTRANCE_NODE_ID )

   assert [ unit.unit.loop_id for unit in packed_units ] == [
      AUSTRALASIA_LOOP_ID,
      TUNDRA_LOOP_ID,
      SAVANNA_LOOP_ID,
      INDO_LOOP_ID,
   ]
