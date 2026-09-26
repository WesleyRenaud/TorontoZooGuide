from __future__ import annotations

from api.giftshops.search.gift_shops_matching_query_builder import GiftShopsMatchingQueryBuilder
from api.models.gift_shop import GiftShop


def Test_Build_TestMatchingQuery_ExpectMatchingGiftShopOnly() -> None:
   zootique = GiftShop( name='Zootique', location='Learning & Engagement Centre' )
   africa_gift_shop = GiftShop( name='Africa Gift Shop', location='Africa' )
   gift_shops = [ zootique, africa_gift_shop ]
   query = 'zootique'

   matches = GiftShopsMatchingQueryBuilder.build( gift_shops, query )

   assert [ shop.name for shop in matches ] == [ zootique.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingGiftShopOnly() -> None:
   zootique = GiftShop( name='Zootique', location='Learning & Engagement Centre' )
   africa_gift_shop = GiftShop( name='Africa Gift Shop', location='Africa' )
   gift_shops = [ zootique, africa_gift_shop ]
   query = 'zootique'

   matches = GiftShopsMatchingQueryBuilder.filter_matching_query(
      gift_shops,
      query )

   assert [ shop.name for shop in matches ] == [ zootique.name ]
