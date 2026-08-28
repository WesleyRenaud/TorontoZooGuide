from __future__ import annotations

from ...models import Pavilion
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder
from ...shared.text_values import TextValues


class PavilionsMatchingQueryBuilder():
   @classmethod
   def _name_key( cls, pavilion: Pavilion ) -> str:
      return TextValues.normalize_for_matching( pavilion.name )


   @classmethod
   def filter_matching_query(
         cls,
         pavilions: list[ Pavilion ],
         query: str ) -> list[ Pavilion ]:
      return NameMatchingQueryBuilder.filter_matching(
         pavilions,
         query,
         cls._name_key )


   @classmethod
   def sort_by_name(
         cls,
         pavilions: list[ Pavilion ] ) -> list[ Pavilion ]:
      return NameMatchingQueryBuilder.sort_by_key( pavilions, cls._name_key )


   @classmethod
   def build(
         cls,
         pavilions: list[ Pavilion ],
         query: str ) -> list[ Pavilion ]:
      return NameMatchingQueryBuilder.build(
         pavilions,
         query,
         cls._name_key,
         sort=True )
