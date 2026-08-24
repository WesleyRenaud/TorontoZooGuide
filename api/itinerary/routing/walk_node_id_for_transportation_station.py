from __future__ import annotations

from ...request_connection import get_connection
from ...transportation.data_access.transportation_station import fetch_transportation_station_record
from ...walk_graph.data_access.load_walk_graph import load_walk_graph
from ...walk_graph.snap_point import snap_point_to_nearest_walk_node


def walk_node_id_for_transportation_station(
      transportation_name: str,
      station_name: str,
) -> str | None:
   station = fetch_transportation_station_record(
      get_connection(),
      transportation_name,
      station_name )

   if station is None:
      return None

   walk_graph = load_walk_graph()
   walk_node_id, _ = snap_point_to_nearest_walk_node(
      station.x_coord,
      station.y_coord,
      walk_graph )

   return walk_node_id
