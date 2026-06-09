from __future__ import annotations

from ..data_access.pavilion import fetch_pavilions
from ..logic.pavilions_matching_query import build_pavilions_matching_query
from ...models import Pavilion
from ...request_connection import get_connection


class PavilionCoordinator():


   @classmethod
   def get_pavilions( cls ) -> list[ Pavilion ]:
      return fetch_pavilions( get_connection() )


   @classmethod
   def get_pavilions_matching_query( cls, query: str ) -> list[ Pavilion ]:
      return build_pavilions_matching_query(
         cls.get_pavilions(),
         query )
