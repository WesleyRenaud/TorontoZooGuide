from __future__ import annotations

from ...models import GiftShop
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def gift_shop_name_key( gift_shop: GiftShop ) -> str:
   return normalize_search_key( gift_shop.name )


def filter_gift_shops_matching_query(
      gift_shops: list[ GiftShop ],
      query: str ) -> list[ GiftShop ]:
   return filter_items_matching_query(
      gift_shops,
      query,
      gift_shop_name_key )


def build_gift_shops_matching_query(
      gift_shops: list[ GiftShop ],
      query: str ) -> list[ GiftShop ]:
   return build_matching_query(
      gift_shops,
      query,
      gift_shop_name_key )
