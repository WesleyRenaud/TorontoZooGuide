from __future__ import annotations

from ..domain.wild_encounter_sort_builder import WildEncounterSortBuilder
from ...itinerary.data_access.itinerary_name_key import itinerary_name_key
from ...itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...models import WildEncounter


class ItineraryWildEncountersBuilder():
   @classmethod
   def build(
         cls,
         wild_encounters: list[ WildEncounter ],
         saved_wild_encounters: list[ ItineraryWildEncounterRecord ] ) -> list[ WildEncounter ]:
      wild_encounter_by_name = {
         saved_encounter.name_key(): saved_encounter
         for saved_encounter in saved_wild_encounters
      }

      for wild_encounter in wild_encounters:
         saved_encounter = wild_encounter_by_name.get(
            itinerary_name_key( wild_encounter.name ) )

         if saved_encounter == None:
            continue

         wild_encounter.start_time = saved_encounter.start_time
         wild_encounter.end_time = saved_encounter.end_time
         wild_encounter.is_deleted = saved_encounter.is_deleted

      WildEncounterSortBuilder.sort_by_name_and_start_time( wild_encounters )

      return wild_encounters
