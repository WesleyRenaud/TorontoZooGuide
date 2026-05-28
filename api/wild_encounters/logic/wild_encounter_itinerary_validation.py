from __future__ import annotations

from ...itinerary.scheduling import schedule_wild_encounter_for_itinerary
from ...models import WildEncounter
from ...models import WildEncounterDiff
from .wild_encounter_schedule import find_wild_encounter_on_day_schedule


def build_wild_encounter_diff_for_visit_day(
      name: str,
      encounter: WildEncounter | None ) -> WildEncounterDiff:
   return schedule_wild_encounter_for_itinerary( name, encounter )


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
