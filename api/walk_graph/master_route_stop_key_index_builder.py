from __future__ import annotations

from .domain.master_route import MasterRoute
from .domain.master_route_stop import master_route_stop_key
from .domain.master_route_stop_key import MasterRouteStopKey


class MasterRouteStopKeyIndexBuilder():
   @classmethod
   def route_index(
         cls,
         master_route: MasterRoute ) -> dict[ MasterRouteStopKey, int ]:
      indexes: dict[ MasterRouteStopKey, int ] = {}
      route_index = 0

      for loop in master_route.loops:
         for stop in loop.viewing_spots:
            stop_key = master_route_stop_key( stop )

            if stop_key in indexes:
               continue

            indexes[ stop_key ] = route_index
            route_index += 1

      return indexes


   @classmethod
   def loop_index(
         cls,
         master_route: MasterRoute ) -> dict[ MasterRouteStopKey, int ]:
      indexes: dict[ MasterRouteStopKey, int ] = {}

      for loop_index, loop in enumerate( master_route.loops ):
         for stop in loop.viewing_spots:
            indexes.setdefault( master_route_stop_key( stop ), loop_index )

      return indexes


   @classmethod
   def loop_id(
         cls,
         master_route: MasterRoute ) -> dict[ MasterRouteStopKey, str ]:
      indexes: dict[ MasterRouteStopKey, str ] = {}

      for loop in master_route.loops:
         for stop in loop.viewing_spots:
            indexes.setdefault( master_route_stop_key( stop ), loop.loop_id )

      return indexes
