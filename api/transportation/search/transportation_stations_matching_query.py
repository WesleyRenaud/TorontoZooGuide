from __future__ import annotations

from ...models import TransportationStation
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def transportation_station_name_key( transportation_station: TransportationStation ) -> str:
   return normalize_search_key( transportation_station.name )


def filter_transportation_stations_matching_query(
      transportation_stations: list[ TransportationStation ],
      query: str ) -> list[ TransportationStation ]:
   return filter_items_matching_query(
      transportation_stations,
      query,
      transportation_station_name_key )


def build_transportation_stations_matching_query(
      transportation_stations: list[ TransportationStation ],
      query: str ) -> list[ TransportationStation ]:
   return build_matching_query(
      transportation_stations,
      query,
      transportation_station_name_key )
