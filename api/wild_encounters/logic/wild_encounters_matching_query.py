from __future__ import annotations

from ... import zoo


def wild_encounter_name_key( wild_encounter: zoo.WildEncounter ) -> str:
   return ( wild_encounter.name or '' ).strip().lower()


def filter_wild_encounters_matching_query(
      wild_encounters: list[ zoo.WildEncounter ],
      query: str ) -> list[ zoo.WildEncounter ]:
   if not query:
      return list( wild_encounters )

   query_lower = query.strip().lower()
   return [
      wild_encounter for wild_encounter in wild_encounters
      if query_lower in wild_encounter_name_key( wild_encounter )
   ]


def build_wild_encounters_matching_query(
      wild_encounters: list[ zoo.WildEncounter ],
      query: str ) -> list[ zoo.WildEncounter ]:
   return filter_wild_encounters_matching_query(
      wild_encounters,
      query )
