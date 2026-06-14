from __future__ import annotations

from ...models import ZoomobileStation
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def zoomobile_station_name_key( zoomobile_station: ZoomobileStation ) -> str:
   return normalize_search_key( zoomobile_station.name )


def filter_zoomobile_stations_matching_query(
      zoomobile_stations: list[ ZoomobileStation ],
      query: str ) -> list[ ZoomobileStation ]:
   return filter_items_matching_query(
      zoomobile_stations,
      query,
      zoomobile_station_name_key )


def build_zoomobile_stations_matching_query(
      zoomobile_stations: list[ ZoomobileStation ],
      query: str ) -> list[ ZoomobileStation ]:
   return build_matching_query(
      zoomobile_stations,
      query,
      zoomobile_station_name_key )
