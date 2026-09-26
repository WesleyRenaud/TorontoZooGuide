from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.duration_values import DurationValues


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

DAY_LOOP = TransportationDayLoop(
   transportation='Zoomobile',
   route='summer',
   main_station=MAIN,
   legs=[
      TransportationRouteLegSegment( MAIN, CANADA, 20 ),
      TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
      TransportationRouteLegSegment( AFRICA, MAIN, 45 ),
   ],
)


def Test_DurationMinutes_TestOwnedLegs_ExpectSum() -> None:
   minutes = DAY_LOOP.duration_minutes()

   assert minutes == sum( leg.duration_minutes for leg in DAY_LOOP.legs )


def Test_DurationSeconds_TestOwnedLegs_ExpectMinutesAsSeconds() -> None:
   seconds = DAY_LOOP.duration_seconds()

   assert seconds == DurationValues.minutes_to_seconds( DAY_LOOP.duration_minutes() )
