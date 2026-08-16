from __future__ import annotations

from ..data_access.transportation import fetch_transportation_records
from ..data_access.transportation_route import fetch_transportation_routes_by_name
from ..domain.transportation import build_transportations
from ..domain.transportation_route import group_transportation_routes
from ...models.transportation import Transportation
from ...request_connection import get_connection


class TransportationCoordinator():
   @classmethod
   def get_transportations( cls ) -> list[ Transportation ]:
      return build_transportations(
         fetch_transportation_records( get_connection() ) )


   @classmethod
   def get_transportation_routes( cls ) -> list[ dict[ str, object ] ]:
      return group_transportation_routes(
         fetch_transportation_routes_by_name( get_connection() ) )
