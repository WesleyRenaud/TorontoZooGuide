from __future__ import annotations

from ...models import GuardiansTalk
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def guardians_talk_name_key( guardians_talk: GuardiansTalk ) -> str:
   return normalize_search_key( guardians_talk.name )


def filter_guardians_talks_matching_query(
      guardians_talks: list[ GuardiansTalk ],
      query: str ) -> list[ GuardiansTalk ]:
   return filter_items_matching_query(
      guardians_talks,
      query,
      guardians_talk_name_key )


def build_guardians_talks_matching_query(
      guardians_talks: list[ GuardiansTalk ],
      query: str ) -> list[ GuardiansTalk ]:
   return build_matching_query(
      guardians_talks,
      query,
      guardians_talk_name_key )
