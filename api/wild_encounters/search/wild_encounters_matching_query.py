from __future__ import annotations

from ...models import WildEncounter
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def wild_encounter_name_key( wild_encounter: WildEncounter ) -> str:
   return normalize_search_key( wild_encounter.name )


def filter_wild_encounters_matching_query(
      wild_encounters: list[ WildEncounter ],
      query: str ) -> list[ WildEncounter ]:
   return filter_items_matching_query(
      wild_encounters,
      query,
      wild_encounter_name_key )


def build_wild_encounters_matching_query(
      wild_encounters: list[ WildEncounter ],
      query: str ) -> list[ WildEncounter ]:
   return build_matching_query(
      wild_encounters,
      query,
      wild_encounter_name_key )
