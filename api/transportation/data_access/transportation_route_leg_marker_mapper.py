from __future__ import annotations

from .transportation_route_leg_marker_record import TransportationRouteLegMarkerRecord
from ...types import Row


class TransportationRouteLegMarkerMapper():
   @classmethod
   def map_record(
         cls,
         row: Row,
   ) -> TransportationRouteLegMarkerRecord:
      return TransportationRouteLegMarkerRecord(
         from_station=row[ 'FROM_STATION' ],
         to_station=row[ 'TO_STATION' ],
         marker_id=row[ 'MARKER_ID' ],
      )


   @classmethod
   def map_records(
         cls,
         rows: list[ Row ],
   ) -> list[ TransportationRouteLegMarkerRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
