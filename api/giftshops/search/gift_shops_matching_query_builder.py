from __future__ import annotations

from ...models import GiftShop
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class GiftShopsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         gift_shops: list[ GiftShop ],
         query: str ) -> list[ GiftShop ]:
      return filter_items_matching_query(
         gift_shops,
         query,
         GiftShop.name_key )


   @classmethod
   def build(
         cls,
         gift_shops: list[ GiftShop ],
         query: str ) -> list[ GiftShop ]:
      return build_matching_query(
         gift_shops,
         query,
         GiftShop.name_key )
