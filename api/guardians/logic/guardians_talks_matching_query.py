def guardians_talk_name_key( guardians_talk ):
   return ( guardians_talk.name or '' ).strip().lower()


def filter_guardians_talks_matching_query( guardians_talks, query ):
   if not query:
      return list( guardians_talks )

   query_lower = query.strip().lower()
   return [
      guardians_talk for guardians_talk in guardians_talks
      if query_lower in guardians_talk_name_key( guardians_talk )
   ]


def build_guardians_talks_matching_query( guardians_talks, query ):
   return filter_guardians_talks_matching_query(
      guardians_talks,
      query )
