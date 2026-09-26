from __future__ import annotations

import pytest

from api.itinerary.transportation.timed_transportation_leg_expander import TimedTransportationLegExpander
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from api.shared.calendar_dates import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

SEGMENTS = [
   TransportationRouteLegSegment( MAIN, CANADA, 20 ),
   TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
]


def Test_Expand_TestTimedLegs_ExpectCursorTimesAndEndKey() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '11:00 AM'
   added_as_attraction = False
   first_end = DateValues.add_minutes_to_time(
      start_time,
      SEGMENTS[ Position.FIRST ].duration_minutes )
   second_end = DateValues.add_minutes_to_time(
      first_end,
      SEGMENTS[ Position.SECOND ].duration_minutes )

   timed_legs, end_time = TimedTransportationLegExpander.expand(
      transportation,
      start_time,
      SEGMENTS,
      added_as_attraction=added_as_attraction )

   assert end_time == second_end
   assert [
      ( leg.from_station, leg.to_station, leg.start_time, leg.end_time )
      for leg in timed_legs
   ] == [
      (
         SEGMENTS[ Position.FIRST ].from_station,
         SEGMENTS[ Position.FIRST ].to_station,
         start_time,
         first_end ),
      (
         SEGMENTS[ Position.SECOND ].from_station,
         SEGMENTS[ Position.SECOND ].to_station,
         first_end,
         second_end ),
   ]
   assert all(
      leg.added_as_attraction is added_as_attraction
      for leg in timed_legs )


def Test_Expand_TestEmptyLegs_ExpectStartAsEnd() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '11:00 AM'
   added_as_attraction = True

   timed_legs, end_time = TimedTransportationLegExpander.expand(
      transportation,
      start_time,
      [],
      added_as_attraction=added_as_attraction )

   assert timed_legs == []
   assert end_time == start_time


def Test_Expand_TestInvalidStartTime_ExpectValueError() -> None:
   start_time = None

   with pytest.raises( ValueError, match='start_time is required' ):
      TimedTransportationLegExpander.expand(
         TransportationName.ZOOMOBILE,
         start_time,
         SEGMENTS,
         added_as_attraction=False )
