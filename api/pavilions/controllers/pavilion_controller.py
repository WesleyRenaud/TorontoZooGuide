from __future__ import annotations

from ...models import Pavilion
from ..data_access.pavilion import fetch_pavilions
from ..logic.pavilions_matching_query import build_pavilions_matching_query
from ...request_connection import get_connection


class PavilionController():


   @classmethod
   def get_pavilions( cls ) -> list[ Pavilion ]:
      return fetch_pavilions( get_connection() )


   @classmethod
   def get_pavilions_matching_query( cls, query: str ) -> list[ Pavilion ]:
      return build_pavilions_matching_query(
         cls.get_pavilions(),
         query )
