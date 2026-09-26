from __future__ import annotations

from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.itinerary.routing.walk_route_polyline_builder import WalkRoutePolylineBuilder
from api.shared.enums import Position, ScheduleItemKind


def _point( node_id: str ) -> WalkRoutePoint:
   return WalkRoutePoint(
      node_id=node_id,
      x=0.0,
      y=0.0,
      x_px=0.0,
      y_px=0.0 )


CONTINUOUS_LEG_A = WalkRouteLeg(
   from_item_key='entrance',
   to_item_key='lion',
   from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
   to_schedule_item_kind=ScheduleItemKind.ANIMAL,
   node_ids=[ 'n-1', 'n-2', 'n-3' ],
   travel_time_minutes=1,
)

CONTINUOUS_LEG_B = WalkRouteLeg(
   from_item_key='lion',
   to_item_key='cheetah',
   from_schedule_item_kind=ScheduleItemKind.ANIMAL,
   to_schedule_item_kind=ScheduleItemKind.ANIMAL,
   node_ids=[ 'n-3', 'n-4' ],
   travel_time_minutes=1,
)

DISCONNECTED_LEG = WalkRouteLeg(
   from_item_key='cheetah',
   to_item_key='entrance',
   from_schedule_item_kind=ScheduleItemKind.ANIMAL,
   to_schedule_item_kind=ScheduleItemKind.ENTRANCE,
   node_ids=[ 'n-5', 'n-6' ],
   travel_time_minutes=1,
)

CONTINUOUS_POINTS = [
   _point( 'n-1' ),
   _point( 'n-2' ),
   _point( 'n-3' ),
   _point( 'n-4' ),
]

DISCONNECTED_POINTS = [
   _point( 'n-1' ),
   _point( 'n-2' ),
   _point( 'n-3' ),
   _point( 'n-4' ),
   _point( 'n-5' ),
   _point( 'n-6' ),
]


def Test_AppendNodeId_TestDuplicateConsecutive_ExpectStoredOnce() -> None:
   route_node_ids: list[ str ] = []
   first_node_id = CONTINUOUS_POINTS[ Position.FIRST ].node_id
   second_node_id = CONTINUOUS_POINTS[ Position.SECOND ].node_id

   WalkRoutePolylineBuilder.append_node_id( route_node_ids, first_node_id )
   WalkRoutePolylineBuilder.append_node_id( route_node_ids, first_node_id )
   WalkRoutePolylineBuilder.append_node_id( route_node_ids, second_node_id )

   assert route_node_ids == [ first_node_id, second_node_id ]


def Test_AppendLegNodeIds_TestSharedJoinNode_ExpectStoredOnce() -> None:
   route_node_ids: list[ str ] = []

   WalkRoutePolylineBuilder.append_leg_node_ids(
      route_node_ids,
      CONTINUOUS_LEG_A.node_ids )
   WalkRoutePolylineBuilder.append_leg_node_ids(
      route_node_ids,
      CONTINUOUS_LEG_B.node_ids )

   assert route_node_ids == [ point.node_id for point in CONTINUOUS_POINTS ]


def Test_InclusivePointSlicesForLegs_TestContinuousLegs_ExpectSharedJoinIndex() -> None:
   legs = [ CONTINUOUS_LEG_A, CONTINUOUS_LEG_B ]
   first_from_sequence = Position.FIRST
   first_to_sequence = (
      first_from_sequence
      + len( CONTINUOUS_LEG_A.node_ids )
      + Position.LAST )
   second_from_sequence = first_to_sequence
   second_to_sequence = (
      second_from_sequence
      + len( CONTINUOUS_LEG_B.node_ids )
      + Position.LAST )

   slices = WalkRoutePolylineBuilder.inclusive_point_slices_for_legs( legs )

   assert slices == [
      ( first_from_sequence, first_to_sequence ),
      ( second_from_sequence, second_to_sequence ),
   ]


def Test_InclusivePointSlicesForLegs_TestDisconnectedLeg_ExpectGapBetweenSlices() -> None:
   legs = [ CONTINUOUS_LEG_A, CONTINUOUS_LEG_B, DISCONNECTED_LEG ]
   first_to_sequence = (
      Position.FIRST
      + len( CONTINUOUS_LEG_A.node_ids )
      + Position.LAST )
   second_to_sequence = (
      first_to_sequence
      + len( CONTINUOUS_LEG_B.node_ids )
      + Position.LAST )
   disconnected_from_sequence = second_to_sequence + Position.SECOND
   disconnected_to_sequence = (
      disconnected_from_sequence
      + len( DISCONNECTED_LEG.node_ids )
      + Position.LAST )

   slices = WalkRoutePolylineBuilder.inclusive_point_slices_for_legs( legs )

   assert slices[ Position.LAST ] == (
      disconnected_from_sequence,
      disconnected_to_sequence )


def Test_NodeIdsForPointSlice_TestContinuousLegs_ExpectMatchingNodeIds() -> None:
   legs = [ CONTINUOUS_LEG_A, CONTINUOUS_LEG_B ]
   slices = WalkRoutePolylineBuilder.inclusive_point_slices_for_legs( legs )

   sliced_node_ids = [
      WalkRoutePolylineBuilder.node_ids_for_point_slice(
         CONTINUOUS_POINTS,
         from_point_sequence=from_point_sequence,
         to_point_sequence=to_point_sequence )
      for from_point_sequence, to_point_sequence in slices
   ]

   assert sliced_node_ids == [ leg.node_ids for leg in legs ]


def Test_NodeIdsForPointSlice_TestDisconnectedLegs_ExpectMatchingNodeIds() -> None:
   legs = [ CONTINUOUS_LEG_A, CONTINUOUS_LEG_B, DISCONNECTED_LEG ]
   slices = WalkRoutePolylineBuilder.inclusive_point_slices_for_legs( legs )

   sliced_node_ids = [
      WalkRoutePolylineBuilder.node_ids_for_point_slice(
         DISCONNECTED_POINTS,
         from_point_sequence=from_point_sequence,
         to_point_sequence=to_point_sequence )
      for from_point_sequence, to_point_sequence in slices
   ]

   assert sliced_node_ids == [ leg.node_ids for leg in legs ]
