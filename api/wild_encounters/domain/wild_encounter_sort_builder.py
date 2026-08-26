from __future__ import annotations

from ...models import WildEncounter


class WildEncounterSortBuilder():
   @classmethod
   def name_and_start_time_sort_key(
         cls,
         wild_encounter: WildEncounter,
      ) -> tuple[ str, str ]:
      return (
         ( wild_encounter.name or '' ).lower(),
         wild_encounter.start_time or '',
      )


   @classmethod
   def sort_by_name_and_start_time(
         cls,
         wild_encounters: list[ WildEncounter ],
      ) -> None:
      wild_encounters.sort( key=cls.name_and_start_time_sort_key )
