from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_day_loop_leg_selector import TransportationDayLoopLegSelector
from api.itinerary.transportation.transportation_ride_duration_calculator import TransportationRideDurationCalculator
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.duration_values import DurationValues


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
   from_station = CANADA
   to_station = TUNDRA

   seconds = TransportationRideDurationCalculator.seconds(
      DAY_LOOP,
      from_station,
      to_station )

   assert seconds == DurationValues.minutes_to_seconds(
      sum(
         leg.duration_minutes
         for leg in TransportationDayLoopLegSelector.select(
            DAY_LOOP,
            from_station,
            to_station ) ) )


def Test_Seconds_TestSameStation_ExpectZero() -> None:
   from_station = MAIN
   to_station = MAIN

   seconds = TransportationRideDurationCalculator.seconds(
      DAY_LOOP,
      from_station,
      to_station )

   assert seconds == 0


def Test_Seconds_TestMissingPath_ExpectZero() -> None:
   from_station = TUNDRA
   to_station = MAIN

   seconds = TransportationRideDurationCalculator.seconds(
      DAY_LOOP,
      from_station,
      to_station )

   assert seconds == 0
