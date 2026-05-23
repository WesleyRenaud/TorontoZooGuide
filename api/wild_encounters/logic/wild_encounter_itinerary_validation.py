from __future__ import annotations

from ... import zoo
from .wild_encounter_schedule import find_wild_encounter_on_day_schedule


def build_wild_encounter_diff_for_visit_day(
      name: str,
      encounter: zoo.WildEncounter | None ) -> zoo.WildEncounterDiff:
   if encounter is None:
      return zoo.WildEncounterDiff(
         name=name,
         is_deleted=True,
         start_time=None,
         end_time=None,
      )

   end_time = zoo.ZooUtil.add_minutes_to_time(
      encounter.start_time,
      encounter.maximum_duration )

   return zoo.WildEncounterDiff(
      name=name,
      is_deleted=not encounter.is_available,
      start_time=encounter.start_time,
      end_time=end_time,
   )


def validate_wild_encounters_for_itinerary(
      wild_encounters_to_include: list[ str ] | None,
      day_schedule: list[ zoo.WildEncounter ] ) -> list[ zoo.WildEncounterDiff ]:

   diffs: list[ zoo.WildEncounterDiff ] = []

   for encounter_name in wild_encounters_to_include or []:
      encounter = find_wild_encounter_on_day_schedule(
         day_schedule,
         encounter_name )
      name = encounter.name if encounter is not None else encounter_name

      diffs.append(
         build_wild_encounter_diff_for_visit_day( name, encounter )
      )

   return diffs
