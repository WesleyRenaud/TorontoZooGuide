from __future__ import annotations

from ... import zoo


def gift_shop_name_key( gift_shop: zoo.GiftShop ) -> str:
   return ( gift_shop.name or '' ).strip().lower()


def filter_gift_shops_matching_query(
      gift_shops: list[ zoo.GiftShop ],
      query: str ) -> list[ zoo.GiftShop ]:
   if not query:
      return list( gift_shops )

   query_lower = query.strip().lower()
   return [
      gift_shop for gift_shop in gift_shops
      if query_lower in gift_shop_name_key( gift_shop )
   ]


def build_gift_shops_matching_query(
      gift_shops: list[ zoo.GiftShop ],
      query: str ) -> list[ zoo.GiftShop ]:
   return filter_gift_shops_matching_query(
      gift_shops,
      query )
