def attraction_name_key( attraction ):
   return ( attraction.name or '' ).strip().lower()


def filter_attractions_matching_query( attractions, query ):
   if not query:
      return list( attractions )

   query_lower = query.strip().lower()
   return [
      attraction for attraction in attractions
      if query_lower in attraction_name_key( attraction )
   ]


def build_attractions_matching_query( attractions, query ):
   return filter_attractions_matching_query(
      attractions,
      query )
