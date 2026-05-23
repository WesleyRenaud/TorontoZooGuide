from __future__ import annotations

from ... import zoo


def guardians_talk_name_key( guardians_talk: zoo.GuardiansTalk ) -> str:
   return ( guardians_talk.name or '' ).strip().lower()


def filter_guardians_talks_matching_query(
      guardians_talks: list[ zoo.GuardiansTalk ],
      query: str ) -> list[ zoo.GuardiansTalk ]:
   if not query:
      return list( guardians_talks )

   query_lower = query.strip().lower()
   return [
      guardians_talk for guardians_talk in guardians_talks
      if query_lower in guardians_talk_name_key( guardians_talk )
   ]


def build_guardians_talks_matching_query(
      guardians_talks: list[ zoo.GuardiansTalk ],
      query: str ) -> list[ zoo.GuardiansTalk ]:
   return filter_guardians_talks_matching_query(
      guardians_talks,
      query )
