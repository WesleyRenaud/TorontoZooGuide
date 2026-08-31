from __future__ import annotations

import pytest

from api.itinerary.transportation.timed_transportation_leg_expander import TimedTransportationLegExpander
from api.itinerary.transportation.transportation_route_leg_segment import TransportationRouteLegSegment


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'

SEGMENTS = [
   TransportationRouteLegSegment( MAIN, CANADA, 20 ),
   TransportationRouteLegSegment( CANADA, AFRICA, 10 ),
]


def Test_Expand_TestTimedLegs_ExpectCursorTimesAndEndKey() -> None:
   timed_legs, end_time = TimedTransportationLegExpander.expand(
      'Zoomobile',
      '11:00 AM',
      SEGMENTS,
      added_as_attraction=False )

   assert end_time == '11:30 AM'
   assert [
      ( leg.from_station, leg.to_station, leg.start_time, leg.end_time )
      for leg in timed_legs
   ] == [
      ( MAIN, CANADA, '11:00 AM', '11:20 AM' ),
      ( CANADA, AFRICA, '11:20 AM', '11:30 AM' ),
   ]
   assert all( leg.added_as_attraction is False for leg in timed_legs )


def Test_Expand_TestEmptyLegs_ExpectStartAsEnd() -> None:
   timed_legs, end_time = TimedTransportationLegExpander.expand(
      'Zoomobile',
      '11:00 AM',
      [],
      added_as_attraction=True )

   assert timed_legs == []
   assert end_time == '11:00 AM'


def Test_Expand_TestInvalidStartTime_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='start_time is required' ):
      TimedTransportationLegExpander.expand(
         'Zoomobile',
         None,
         SEGMENTS,
         added_as_attraction=False )
