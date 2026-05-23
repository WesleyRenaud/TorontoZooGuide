from __future__ import annotations

from ...models import WildEncounter
from ...models import WildEncounterDiff
from ...zoo_util import ZooUtil
from .wild_encounter_schedule import find_wild_encounter_on_day_schedule


def build_wild_encounter_diff_for_visit_day(
      name: str,
      encounter: WildEncounter | None ) -> WildEncounterDiff:
   if encounter is None:
      return WildEncounterDiff(
         name=name,
         is_deleted=True,
         start_time=None,
         end_time=None,
      )

   end_time = ZooUtil.add_minutes_to_time(
      encounter.start_time,
      encounter.maximum_duration )

   return WildEncounterDiff(
      name=name,
      is_deleted=not encounter.is_available,
      start_time=encounter.start_time,
      end_time=end_time,
   )


def validate_wild_encounters_for_itinerary(
      wild_encounters_to_include: list[ str ] | None,
      day_schedule: list[ WildEncounter ] ) -> list[ WildEncounterDiff ]:

   diffs: list[ WildEncounterDiff ] = []

   for encounter_name in wild_encounters_to_include or []:
      encounter = find_wild_encounter_on_day_schedule(
         day_schedule,
         encounter_name )
      name = encounter.name if encounter is not None else encounter_name

      diffs.append(
         build_wild_encounter_diff_for_visit_day( name, encounter )
      )

   return diffs
