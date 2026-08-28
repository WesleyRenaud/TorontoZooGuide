from __future__ import annotations

from ...request_connection import get_connection
from ...transportation.data_access.transportation_station_provider import TransportationStationProvider
from ...walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from ...walk_graph.walk_node_snapper import WalkNodeSnapper


class TransportationStationWalkNodeResolver():
   @classmethod
   def resolve(
         cls,
         transportation_name: str,
         station_name: str,
         ) -> str | None:
      station = TransportationStationProvider.fetch_transportation_station_record(
         get_connection(),
         transportation_name,
         station_name )

      if station is None:
         return None

      walk_graph = WalkGraphProvider.fetch()
      walk_node_id, _ = WalkNodeSnapper.snap(
         station.x_coord,
         station.y_coord,
         walk_graph )

      return walk_node_id
