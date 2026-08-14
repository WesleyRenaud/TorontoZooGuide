from __future__ import annotations

from .transportation_route_record import TransportationRouteRecord
from ...types import Row


def map_transportation_route_record( row: Row ) -> TransportationRouteRecord:
   return TransportationRouteRecord(
      transportation=row[ 'NAME' ],
      route=row[ 'ROUTE' ] )


def map_transportation_route_records(
      rows: list[ Row ] ) -> list[ TransportationRouteRecord ]:
   return [
      map_transportation_route_record( row )
      for row in rows
   ]
