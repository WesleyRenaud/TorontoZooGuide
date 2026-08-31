from __future__ import annotations

from api.itinerary.transportation.transportation_day_loop import TransportationDayLoop
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


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
   assert DAY_LOOP.duration_minutes() == 75


def Test_DurationSeconds_TestOwnedLegs_ExpectMinutesAsSeconds() -> None:
   assert DAY_LOOP.duration_seconds() == 75 * 60
