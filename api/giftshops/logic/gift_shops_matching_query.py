def gift_shop_name_key( gift_shop ):
   return ( gift_shop.name or '' ).strip().lower()


def filter_gift_shops_matching_query( gift_shops, query ):
   if not query:
      return list( gift_shops )

   query_lower = query.strip().lower()
   return [
      gift_shop for gift_shop in gift_shops
      if query_lower in gift_shop_name_key( gift_shop )
   ]


def build_gift_shops_matching_query( gift_shops, query ):
   return filter_gift_shops_matching_query(
      gift_shops,
      query )
