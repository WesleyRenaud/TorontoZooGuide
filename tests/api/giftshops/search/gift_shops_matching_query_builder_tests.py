from __future__ import annotations

from api.giftshops.search.gift_shops_matching_query_builder import GiftShopsMatchingQueryBuilder
from api.models.gift_shop import GiftShop


def Test_Build_TestMatchingQuery_ExpectMatchingGiftShopOnly() -> None:
   gift_shops = [
      GiftShop( name='Zootique', location='Learning & Engagement Centre' ),
      GiftShop( name='Africa Gift Shop', location='Africa' ),
   ]

   matches = GiftShopsMatchingQueryBuilder.build( gift_shops, 'zootique' )

   assert [ shop.name for shop in matches ] == [ 'Zootique' ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingGiftShopOnly() -> None:
   gift_shops = [
      GiftShop( name='Zootique', location='Learning & Engagement Centre' ),
      GiftShop( name='Africa Gift Shop', location='Africa' ),
   ]

   matches = GiftShopsMatchingQueryBuilder.filter_matching_query(
      gift_shops,
      'zootique' )

   assert [ shop.name for shop in matches ] == [ 'Zootique' ]
