from __future__ import annotations

from ..transportation.transportation_route_leg_segment import TransportationRouteLegSegment
from ...types import Types


class TransportationRouteLegSegmentMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> TransportationRouteLegSegment:
      return TransportationRouteLegSegment(
         from_station=row[ 'FROM_STATION' ],
         to_station=row[ 'TO_STATION' ],
         duration_minutes=int( row[ 'DURATION_MINUTES' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ TransportationRouteLegSegment ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
