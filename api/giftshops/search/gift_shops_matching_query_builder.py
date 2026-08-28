from __future__ import annotations

from ...models import GiftShop
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class GiftShopsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         gift_shops: list[ GiftShop ],
         query: str ) -> list[ GiftShop ]:
      return NameMatchingQueryBuilder.filter_matching(
         gift_shops,
         query,
         GiftShop.name_key )


   @classmethod
   def build(
         cls,
         gift_shops: list[ GiftShop ],
         query: str ) -> list[ GiftShop ]:
      return NameMatchingQueryBuilder.build(
         gift_shops,
         query,
         GiftShop.name_key )
