from __future__ import annotations

from ...itinerary.scheduling.core.scheduled_occurrence_builder import ScheduledOccurrenceBuilder
from ...itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from ...models import WildEncounter
from ...models import WildEncounterDiff
from ..scheduling.wild_encounter_day_schedule_finder import WildEncounterDayScheduleFinder
from ...types import ScheduleTimeKey


class WildEncounterItineraryValidator():
   @classmethod
   def build_diff_for_visit_day(
         cls,
         name: str,
         encounter: WildEncounter | None,
         *,
         start_time_override: ScheduleTimeKey = None,
         end_time_override: ScheduleTimeKey = None ) -> WildEncounterDiff:
      return ScheduledOccurrenceBuilder.wild_encounter(
         name,
         encounter,
         start_time_override=start_time_override,
         end_time_override=end_time_override )


   @classmethod
   def validate_for_itinerary(
         cls,
         wild_encounters_to_include: list[ WildEncounterScheduleItemKey ] | None,
         day_schedule: list[ WildEncounter ] ) -> list[ WildEncounterDiff ]:
      diffs: list[ WildEncounterDiff ] = []

      for encounter_key in wild_encounters_to_include or []:
         encounter = WildEncounterDayScheduleFinder.find_on_day_schedule(
            day_schedule,
            encounter_key.name,
            start_time=encounter_key.start_time )
         name = encounter.name if encounter is not None else encounter_key.name

         diffs.append(
            cls.build_diff_for_visit_day(
               name,
               encounter,
               start_time_override=encounter_key.start_time,
               end_time_override=encounter_key.end_time ) )

      return diffs
