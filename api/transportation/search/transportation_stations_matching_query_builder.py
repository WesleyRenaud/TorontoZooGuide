from __future__ import annotations

from ...models import TransportationStation
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class TransportationStationsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         transportation_stations: list[ TransportationStation ],
         query: str ) -> list[ TransportationStation ]:
      return NameMatchingQueryBuilder.filter_matching(
         transportation_stations,
         query,
         TransportationStation.name_key )


   @classmethod
   def build(
         cls,
         transportation_stations: list[ TransportationStation ],
         query: str ) -> list[ TransportationStation ]:
      return NameMatchingQueryBuilder.build(
         transportation_stations,
         query,
         TransportationStation.name_key )
