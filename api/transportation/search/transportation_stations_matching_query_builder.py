from __future__ import annotations

from ...models import TransportationStation
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class TransportationStationsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         transportation_stations: list[ TransportationStation ],
         query: str ) -> list[ TransportationStation ]:
      return filter_items_matching_query(
         transportation_stations,
         query,
         TransportationStation.name_key )


   @classmethod
   def build(
         cls,
         transportation_stations: list[ TransportationStation ],
         query: str ) -> list[ TransportationStation ]:
      return build_matching_query(
         transportation_stations,
         query,
         TransportationStation.name_key )
