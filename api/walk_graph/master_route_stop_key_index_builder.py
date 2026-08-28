from __future__ import annotations

from .domain.master_route import MasterRoute
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
            stop_key = stop.master_route_key()

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
            indexes.setdefault( stop.master_route_key(), loop_index )

      return indexes


   @classmethod
   def loop_id(
         cls,
         master_route: MasterRoute ) -> dict[ MasterRouteStopKey, str ]:
      indexes: dict[ MasterRouteStopKey, str ] = {}

      for loop in master_route.loops:
         for stop in loop.viewing_spots:
            indexes.setdefault( stop.master_route_key(), loop.loop_id )

      return indexes
