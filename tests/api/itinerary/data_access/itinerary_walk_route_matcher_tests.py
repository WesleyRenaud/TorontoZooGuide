from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.itinerary_walk_route_matcher import ItineraryWalkRouteMatcher
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.walk_route_leg import WalkRouteLeg
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.shared.date_values import DateValues
from api.shared.enums import ScheduleItemKind


ENTRANCE_ITEM_KEY = 'entrance'
ENTRANCE_NODE_ID = 'n-1'
LION_NODE_ID = 'n-2'
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
LION_ENCLOSURE = 'Outdoor'
LION_ITEM_KEY = AnimalScheduleItemKey.wire(
   species=LION_SPECIES,
   exhibit=LION_EXHIBIT,
   enclosure_name=LION_ENCLOSURE )
LION_START_TIME = '10:00 AM'
LION_DURATION_MINUTES = 30
LION_END_TIME = DateValues.add_minutes_to_time(
   LION_START_TIME,
   LION_DURATION_MINUTES )
TRAVEL_TIME_MINUTES = 5

ENTRANCE_STOP = ItineraryWalkRouteStop(
   schedule_item_kind=ScheduleItemKind.ENTRANCE,
   item_key=ENTRANCE_ITEM_KEY,
   walk_node_id=ENTRANCE_NODE_ID )

LION_STOP = ItineraryWalkRouteStop(
   schedule_item_kind=ScheduleItemKind.ANIMAL,
   item_key=LION_ITEM_KEY,
   walk_node_id=LION_NODE_ID,
   start_time=LION_START_TIME,
   end_time=LION_END_TIME )

ENTRANCE_POINT = WalkRoutePoint(
   node_id=ENTRANCE_NODE_ID,
   x=0.0,
   y=0.0,
   x_px=0.0,
   y_px=0.0 )

LION_POINT = WalkRoutePoint(
   node_id=LION_NODE_ID,
   x=10.0,
   y=10.0,
   x_px=10.0,
   y_px=10.0 )

ENTRANCE_TO_LION_LEG = WalkRouteLeg(
   from_item_key=ENTRANCE_ITEM_KEY,
   to_item_key=LION_ITEM_KEY,
   from_schedule_item_kind=ScheduleItemKind.ENTRANCE,
   to_schedule_item_kind=ScheduleItemKind.ANIMAL,
   node_ids=[ ENTRANCE_NODE_ID, LION_NODE_ID ],
   travel_time_minutes=TRAVEL_TIME_MINUTES )

SAMPLE_ROUTE = ItineraryWalkRoute(
   stops=[ ENTRANCE_STOP, LION_STOP ],
   legs=[ ENTRANCE_TO_LION_LEG ],
   points=[ ENTRANCE_POINT, LION_POINT ] )


def Test_Matches_TestIdenticalRoutes_ExpectTrue() -> None:
   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, SAMPLE_ROUTE )

   assert matches


def Test_Matches_TestDifferentLegCount_ExpectFalse() -> None:
   shorter_legs_route = ItineraryWalkRoute(
      stops=SAMPLE_ROUTE.stops,
      legs=[],
      points=SAMPLE_ROUTE.points )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, shorter_legs_route )

   assert not matches


def Test_Matches_TestDifferentPointCount_ExpectFalse() -> None:
   shorter_points_route = ItineraryWalkRoute(
      stops=SAMPLE_ROUTE.stops,
      legs=SAMPLE_ROUTE.legs,
      points=[ ENTRANCE_POINT ] )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, shorter_points_route )

   assert not matches


def Test_Matches_TestDifferentStop_ExpectFalse() -> None:
   tiger_species = 'Amur Tiger'
   tiger_exhibit = 'Eurasia Wilds'
   tiger_enclosure = 'Outdoor'
   altered_stop_route = ItineraryWalkRoute(
      stops=[
         ENTRANCE_STOP,
         ItineraryWalkRouteStop(
            schedule_item_kind=ScheduleItemKind.ANIMAL,
            item_key=AnimalScheduleItemKey.wire(
               species=tiger_species,
               exhibit=tiger_exhibit,
               enclosure_name=tiger_enclosure ),
            walk_node_id='n-3',
            start_time=LION_START_TIME,
            end_time=LION_END_TIME ),
      ],
      legs=SAMPLE_ROUTE.legs,
      points=SAMPLE_ROUTE.points )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, altered_stop_route )

   assert not matches


def Test_Matches_TestDifferentPoint_ExpectFalse() -> None:
   altered_x = 11.0
   altered_point_route = ItineraryWalkRoute(
      stops=SAMPLE_ROUTE.stops,
      legs=SAMPLE_ROUTE.legs,
      points=[
         ENTRANCE_POINT,
         WalkRoutePoint(
            node_id=LION_POINT.node_id,
            x=altered_x,
            y=LION_POINT.y,
            x_px=altered_x,
            y_px=LION_POINT.y_px ),
      ] )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, altered_point_route )

   assert not matches


def Test_Matches_TestDifferentStopCount_ExpectFalse() -> None:
   shorter_route = ItineraryWalkRoute(
      stops=[ ENTRANCE_STOP ],
      legs=SAMPLE_ROUTE.legs,
      points=SAMPLE_ROUTE.points )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, shorter_route )

   assert not matches


def Test_Matches_TestDifferentTravelTime_ExpectFalse() -> None:
   altered_travel_time_minutes = 6
   altered_route = ItineraryWalkRoute(
      stops=SAMPLE_ROUTE.stops,
      legs=[
         WalkRouteLeg(
            from_item_key=ENTRANCE_TO_LION_LEG.from_item_key,
            to_item_key=ENTRANCE_TO_LION_LEG.to_item_key,
            from_schedule_item_kind=ENTRANCE_TO_LION_LEG.from_schedule_item_kind,
            to_schedule_item_kind=ENTRANCE_TO_LION_LEG.to_schedule_item_kind,
            node_ids=ENTRANCE_TO_LION_LEG.node_ids,
            travel_time_minutes=altered_travel_time_minutes ),
      ],
      points=SAMPLE_ROUTE.points )

   matches = ItineraryWalkRouteMatcher.matches( SAMPLE_ROUTE, altered_route )

   assert not matches
