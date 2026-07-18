from __future__ import annotations

from ...itinerary.scheduling import schedule_wild_encounter_for_itinerary
from ...itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from ...models import WildEncounter
from ...models import WildEncounterDiff
from ..scheduling.wild_encounter_schedule import find_wild_encounter_on_day_schedule
from ...types import ScheduleTimeKey


def build_wild_encounter_diff_for_visit_day(
      name: str,
      encounter: WildEncounter | None,
      *,
      start_time_override: ScheduleTimeKey = None,
      end_time_override: ScheduleTimeKey = None ) -> WildEncounterDiff:
   return schedule_wild_encounter_for_itinerary(
      name,
      encounter,
      start_time_override=start_time_override,
      end_time_override=end_time_override )


def validate_wild_encounters_for_itinerary(
      wild_encounters_to_include: list[ WildEncounterScheduleItemKey ] | None,
      day_schedule: list[ WildEncounter ],
   ) -> list[ WildEncounterDiff ]:
   diffs: list[ WildEncounterDiff ] = []

   for encounter_key in wild_encounters_to_include or []:
      encounter = find_wild_encounter_on_day_schedule(
         day_schedule,
         encounter_key.name,
         start_time=encounter_key.start_time )
      name = encounter.name if encounter is not None else encounter_key.name

      diffs.append(
         build_wild_encounter_diff_for_visit_day(
            name,
            encounter,
            start_time_override=encounter_key.start_time,
            end_time_override=encounter_key.end_time ) )

   return diffs
