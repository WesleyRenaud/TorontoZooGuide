from __future__ import annotations

from api.itinerary.data_access.itinerary_walk_route_matcher import ItineraryWalkRouteMatcher
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.enums import ScheduleItemKind


ENTRANCE_STOP = ItineraryWalkRouteStop(
   schedule_item_kind=ScheduleItemKind.ENTRANCE,
   item_key='entrance',
   walk_node_id='n-1' )

LION_STOP = ItineraryWalkRouteStop(
   schedule_item_kind=ScheduleItemKind.ANIMAL,
   item_key='African Lion||Africa Savanna||Outdoor',
   walk_node_id='n-2',
   start_time='10:00 AM',
   end_time='10:30 AM' )

ENTRANCE_POINT = WalkRoutePoint(
   node_id='n-1',
   x=0.0,
   y=0.0,
   x_px=0.0,
   y_px=0.0 )

LION_POINT = WalkRoutePoint(
   node_id='n-2',
   x=10.0,
   y=10.0,
   x_px=10.0,
   y_px=10.0 )

ENTRANCE_TO_LION_LEG = WalkRouteLeg(
   from_item_key='entrance',
   to_item_key='African Lion||Africa Savanna||Outdoor',
   from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
   to_schedule_item_kind=ScheduleItemKind.ANIMAL,
   node_ids=[ 'n-1', 'n-2' ],
   travel_time_minutes=5 )

SAMPLE_ROUTE = ItineraryWalkRoute(
   stops=[ ENTRANCE_STOP, LION_STOP ],
   legs=[ ENTRANCE_TO_LION_LEG ],
   points=[ ENTRANCE_POINT, LION_POINT ] )


def Test_Matches_TestIdenticalRoutes_ExpectTrue() -> None:
   assert ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, SAMPLE_ROUTE )


def Test_Matches_TestDifferentStopCount_ExpectFalse() -> None:
   shorter_route = ItineraryWalkRoute(
      stops=[ ENTRANCE_STOP ],
      legs=SAMPLE_ROUTE.legs,
      points=SAMPLE_ROUTE.points )

   assert not ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, shorter_route )


def Test_Matches_TestDifferentTravelTime_ExpectFalse() -> None:
   altered_route = ItineraryWalkRoute(
      stops=SAMPLE_ROUTE.stops,
      legs=[
         WalkRouteLeg(
            from_item_key=ENTRANCE_TO_LION_LEG.from_item_key,
            to_item_key=ENTRANCE_TO_LION_LEG.to_item_key,
            from_schedule_item_kind=ENTRANCE_TO_LION_LEG.from_schedule_item_kind,
            to_schedule_item_kind=ENTRANCE_TO_LION_LEG.to_schedule_item_kind,
            node_ids=ENTRANCE_TO_LION_LEG.node_ids,
            travel_time_minutes=6 ),
      ],
      points=SAMPLE_ROUTE.points )

   assert not ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, altered_route )
