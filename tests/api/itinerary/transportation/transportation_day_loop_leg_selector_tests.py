from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_leg_selector import TransportationDayLoopLegSelector
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


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
   assert TransportationDayLoopLegSelector.select( DAY_LOOP, MAIN, MAIN ) == []


def Test_Select_TestMultiHopPath_ExpectOrderedLegs() -> None:
   selected = TransportationDayLoopLegSelector.select( DAY_LOOP, CANADA, TUNDRA )

   assert [
      ( leg.from_station, leg.to_station, leg.duration_minutes )
      for leg in selected
   ] == [
      ( CANADA, AFRICA, 10 ),
      ( AFRICA, TUNDRA, 15 ),
   ]


def Test_Select_TestBrokenGraph_ExpectEmpty() -> None:
   broken = TransportationDayLoop(
      transportation='Zoomobile',
      route='broken',
      main_station=MAIN,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      ],
   )

   assert TransportationDayLoopLegSelector.select( broken, CANADA, AFRICA ) == []


def Test_Select_TestWrapPastEndWithoutTarget_ExpectEmpty() -> None:
   partial = TransportationDayLoop(
      transportation='Zoomobile',
      route='partial',
      main_station=MAIN,
      legs=[
         TransportationRouteLegSegment( MAIN, CANADA, 20 ),
         TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      ],
   )

   assert TransportationDayLoopLegSelector.select( partial, MAIN, TUNDRA ) == []
