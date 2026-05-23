from __future__ import annotations

from ...models import ZoomobileStation


def zoomobile_station_name_key( zoomobile_station: ZoomobileStation ) -> str:
   return ( zoomobile_station.name or '' ).strip().lower()


def filter_zoomobile_stations_matching_query(
      zoomobile_stations: list[ ZoomobileStation ],
      query: str ) -> list[ ZoomobileStation ]:
   if not query:
      return list( zoomobile_stations )

   query_lower = query.strip().lower()
   return [
      zoomobile_station for zoomobile_station in zoomobile_stations
      if query_lower in zoomobile_station_name_key( zoomobile_station )
   ]


def build_zoomobile_stations_matching_query(
      zoomobile_stations: list[ ZoomobileStation ],
      query: str ) -> list[ ZoomobileStation ]:
   return filter_zoomobile_stations_matching_query(
      zoomobile_stations,
      query )
