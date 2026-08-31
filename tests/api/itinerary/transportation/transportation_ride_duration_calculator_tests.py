from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_ride_duration_calculator import TransportationRideDurationCalculator
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'

DAY_LOOP = TransportationDayLoop(
   transportation='Zoomobile',
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, TUNDRA, 15 ),
   ],
)


def Test_Seconds_TestMultiHopPath_ExpectSummedMinutesAsSeconds() -> None:
   assert TransportationRideDurationCalculator.seconds(
      DAY_LOOP,
      CANADA,
      TUNDRA ) == ( 10 + 15 ) * 60


def Test_Seconds_TestSameStation_ExpectZero() -> None:
   assert TransportationRideDurationCalculator.seconds( DAY_LOOP, MAIN, MAIN ) == 0


def Test_Seconds_TestMissingPath_ExpectZero() -> None:
   assert TransportationRideDurationCalculator.seconds(
      DAY_LOOP,
      TUNDRA,
      MAIN ) == 0
