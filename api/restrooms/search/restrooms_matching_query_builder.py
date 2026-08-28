from __future__ import annotations

from ...models import Restroom
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder
from ...shared.text_values import TextValues


class RestroomsMatchingQueryBuilder():
   @classmethod
   def _title_key( cls, restroom: Restroom ) -> str:
      return TextValues.normalize_for_matching( restroom.title )


   @classmethod
   def filter_matching_query(
         cls,
         restrooms: list[ Restroom ],
         query: str ) -> list[ Restroom ]:
      return NameMatchingQueryBuilder.filter_matching(
         restrooms,
         query,
         cls._title_key )


   @classmethod
   def build(
         cls,
         restrooms: list[ Restroom ],
         query: str ) -> list[ Restroom ]:
      return NameMatchingQueryBuilder.build(
         restrooms,
         query,
         cls._title_key )
