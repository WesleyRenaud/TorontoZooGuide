from __future__ import annotations

from ..data_access.pavilion_provider import PavilionProvider
from ...models import Pavilion
from ...request_connection import get_connection
from ..search.pavilions_matching_query_builder import PavilionsMatchingQueryBuilder


class PavilionCoordinator():
   @classmethod
   def get_pavilions( cls ) -> list[ Pavilion ]:
      return PavilionProvider.fetch_pavilions( get_connection() )


   @classmethod
   def get_pavilions_matching_query( cls, query: str ) -> list[ Pavilion ]:
      return PavilionsMatchingQueryBuilder.build(
         cls.get_pavilions(),
         query )
