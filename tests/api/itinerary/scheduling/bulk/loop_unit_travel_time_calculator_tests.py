from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_schedule_unit_builder import LoopScheduleUnitBuilder
from api.itinerary.scheduling.bulk.loop_unit_travel_time_calculator import LoopUnitTravelTimeCalculator
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.walk_graph.domain.walk_graph import WalkGraph
from api.walk_graph.domain.walk_graph_node import WalkGraphNode


ENTRANCE_NODE_ID = 'n-1'
CHEETAH_NODE_ID = 'n-cheetah'
LION_NODE_ID = 'n-lion'

CHEETAH_APPROACH_SECONDS = 360
CHEETAH_TO_LION_SECONDS = 540


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
      _node( LION_NODE_ID, 20.0, 0.0 ),
   ],
   'edges': [
      {
         'from': ENTRANCE_NODE_ID,
         'to': CHEETAH_NODE_ID,
         'length_px': _edge_length_px( 6 ),
      },
      {
         'from': CHEETAH_NODE_ID,
         'to': LION_NODE_ID,
         'length_px': _edge_length_px( 9 ),
      },
   ],
}


def _animal_record(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=None,
      new_likelihood=100,
   )


def _loop_unit(
      *,
      loop_id: str,
      stops: list[ ItineraryAnimalRecord ],
      entry_walk_node_id: str,
      exit_walk_node_id: str,
      ) -> LoopScheduleUnit:
   return LoopScheduleUnit(
      loop_id=loop_id,
      stops=stops,
      entry_walk_node_id=entry_walk_node_id,
      exit_walk_node_id=exit_walk_node_id,
      side_cluster_id=None,
      loop_index_in_side_cluster=None,
      traversal=None )


def _prepared_loop_unit(
      *,
      loop_id: str,
      stops: list[ ItineraryAnimalRecord ],
      entry_walk_node_id: str,
      exit_walk_node_id: str,
      duration_seconds: int,
      ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=_loop_unit(
         loop_id=loop_id,
         stops=stops,
         entry_walk_node_id=entry_walk_node_id,
         exit_walk_node_id=exit_walk_node_id ),
      occupied_seconds=duration_seconds )


def _walk_node_id_for_stop( stop: ItineraryAnimalRecord ) -> str | None:
   return {
      ( 'Cheetah', 'Indo-Malaya Outdoor', None ): CHEETAH_NODE_ID,
      ( 'African Lion', 'Africa Savanna', None ): LION_NODE_ID,
   }.get( ( stop.species, stop.exhibit, stop.enclosure_name ) )


@pytest.fixture
def stub_loop_unit_walk_nodes( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      LoopScheduleUnitBuilder,
      'walk_node_id_for_stop',
      _walk_node_id_for_stop )


def Test_ApproachSecondsToUnit_TestFromEntryNode_ExpectZero() -> None:
   unit = _loop_unit(
      loop_id='indo_malaya',
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      entry_walk_node_id=CHEETAH_NODE_ID,
      exit_walk_node_id=CHEETAH_NODE_ID )

   assert LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      TEST_GRAPH,
      CHEETAH_NODE_ID,
      unit ) == 0


def Test_ApproachSecondsToUnit_TestFromEntrance_ExpectApproachSeconds() -> None:
   unit = _loop_unit(
      loop_id='indo_malaya',
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      entry_walk_node_id=CHEETAH_NODE_ID,
      exit_walk_node_id=CHEETAH_NODE_ID )

   assert LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      TEST_GRAPH,
      ENTRANCE_NODE_ID,
      unit ) == CHEETAH_APPROACH_SECONDS


def Test_InterStopSeconds_TestTwoAnimals_ExpectTravelBetweenStops(
      stub_loop_unit_walk_nodes: None ) -> None:
   stops = [
      _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
      _animal_record( species='African Lion', exhibit='Africa Savanna' ),
   ]
   travels = LoopUnitTravelTimeCalculator.inter_stop_seconds( TEST_GRAPH, stops )

   assert travels == [ 0, CHEETAH_TO_LION_SECONDS ]
   assert LoopUnitTravelTimeCalculator.total_inter_stop_seconds(
      TEST_GRAPH,
      stops ) == CHEETAH_TO_LION_SECONDS
   assert LoopUnitTravelTimeCalculator.inter_stop_seconds(
      TEST_GRAPH,
      stops[ :1 ] ) == [ 0 ]


def Test_PackedUnitsOccupiedSeconds_TestTwoUnits_ExpectApproachAndDwell() -> None:
   indo_unit = _prepared_loop_unit(
      loop_id='indo_malaya',
      stops=[ _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) ],
      entry_walk_node_id=CHEETAH_NODE_ID,
      exit_walk_node_id=CHEETAH_NODE_ID,
      duration_seconds=300 )
   africa_unit = _prepared_loop_unit(
      loop_id='africa_savanna_canadian_domain',
      stops=[ _animal_record( species='African Lion', exhibit='Africa Savanna' ) ],
      entry_walk_node_id=LION_NODE_ID,
      exit_walk_node_id=LION_NODE_ID,
      duration_seconds=480 )

   occupied = LoopUnitTravelTimeCalculator.packed_units_occupied_seconds(
      TEST_GRAPH,
      [ indo_unit, africa_unit ],
      from_node_id=ENTRANCE_NODE_ID )
   first_approach = LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      TEST_GRAPH,
      ENTRANCE_NODE_ID,
      indo_unit.unit )
   second_approach = LoopUnitTravelTimeCalculator.approach_seconds_to_unit(
      TEST_GRAPH,
      CHEETAH_NODE_ID,
      africa_unit.unit )

   assert occupied == first_approach + 300 + second_approach + 480
   assert occupied > 300 + 480
