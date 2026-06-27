from __future__ import annotations

from ...models import WildEncounter


def wild_encounter_name_and_start_time_sort_key(
      wild_encounter: WildEncounter,
   ) -> tuple[ str, str ]:
   return (
      ( wild_encounter.name or '' ).lower(),
      wild_encounter.start_time or '',
   )


def sort_wild_encounters_by_name_and_start_time(
      wild_encounters: list[ WildEncounter ],
   ) -> None:
   wild_encounters.sort( key=wild_encounter_name_and_start_time_sort_key )
