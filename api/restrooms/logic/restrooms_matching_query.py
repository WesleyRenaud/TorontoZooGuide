def restroom_title_key( restroom ):
   return ( restroom.title or '' ).strip().lower()


def filter_restrooms_matching_query( restrooms, query ):
   if not query:
      return list( restrooms )

   query_lower = query.strip().lower()
   return [
      restroom for restroom in restrooms
      if query_lower in restroom_title_key( restroom )
   ]


def build_restrooms_matching_query( restrooms, query ):
   return filter_restrooms_matching_query(
      restrooms,
      query )
