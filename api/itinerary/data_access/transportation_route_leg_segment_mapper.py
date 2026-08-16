from __future__ import annotations

from ..transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import Row


def map_transportation_route_leg_segment(
      row: Row ) -> TransportationRouteLegSegment:
   return TransportationRouteLegSegment(
      from_station=row[ 'FROM_STATION' ],
      to_station=row[ 'TO_STATION' ],
      duration_minutes=int( row[ 'DURATION_MINUTES' ] ) )


def map_transportation_route_leg_segments(
      rows: list[ Row ] ) -> list[ TransportationRouteLegSegment ]:
   return [
      map_transportation_route_leg_segment( row )
      for row in rows
   ]
