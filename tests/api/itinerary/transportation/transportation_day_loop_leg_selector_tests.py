from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_leg_selector import TransportationDayLoopLegSelector
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.enums.position import Position


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'

DAY_LOOP = TransportationDayLoop(
   transportation='Zoomobile',
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
      TransportationRouteLegSegment( TUNDRA, EURASIA, 15 ),
      TransportationRouteLegSegment( EURASIA, MAIN, 15 ),
   ],
)


def Test_Select_TestSameStation_ExpectEmpty() -> None:
   from_station = MAIN
   to_station = MAIN

   selected = TransportationDayLoopLegSelector.select(
      DAY_LOOP,
      from_station,
      to_station )

   assert selected == []


def Test_Select_TestMultiHopPath_ExpectOrderedLegs() -> None:
   from_station = CANADA
   to_station = TUNDRA

   selected = TransportationDayLoopLegSelector.select(
      DAY_LOOP,
      from_station,
      to_station )

   assert [
      ( leg.from_station, leg.to_station, leg.duration_minutes )
      for leg in selected
   ] == [
      (
         DAY_LOOP.legs[ Position.SECOND ].from_station,
         DAY_LOOP.legs[ Position.SECOND ].to_station,
         DAY_LOOP.legs[ Position.SECOND ].duration_minutes ),
      (
         DAY_LOOP.legs[ Position.THIRD ].from_station,
         DAY_LOOP.legs[ Position.THIRD ].to_station,
         DAY_LOOP.legs[ Position.THIRD ].duration_minutes ),
   ]


def Test_Select_TestBrokenGraph_ExpectEmpty() -> None:
   from_station = CANADA
   to_station = AFRICA
   broken = TransportationDayLoop(
      transportation='Zoomobile',
      route='broken',
      main_station=MAIN,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      ] )

   selected = TransportationDayLoopLegSelector.select(
      broken,
      from_station,
      to_station )

   assert selected == []


def Test_Select_TestWrapPastEndWithoutTarget_ExpectEmpty() -> None:
   from_station = MAIN
   to_station = TUNDRA
   partial = TransportationDayLoop(
      transportation='Zoomobile',
      route='partial',
      main_station=MAIN,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
         TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      ] )

   selected = TransportationDayLoopLegSelector.select(
      partial,
      from_station,
      to_station )

   assert selected == []
