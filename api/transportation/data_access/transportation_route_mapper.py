from __future__ import annotations

from .transportation_route_record import TransportationRouteRecord
from ...types import Types


class TransportationRouteMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> TransportationRouteRecord:
      return TransportationRouteRecord(
         transportation=row[ 'NAME' ],
         route=row[ 'ROUTE' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ] ) -> list[ TransportationRouteRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
