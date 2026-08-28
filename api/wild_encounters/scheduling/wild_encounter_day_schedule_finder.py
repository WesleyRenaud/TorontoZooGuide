from __future__ import annotations

from ..domain.wild_encounter_name_filter import WildEncounterNameFilter
from ...models import WildEncounter
from ...shared.calendar_dates import DateValues
from ...types import Types


class WildEncounterDayScheduleFinder():
   @classmethod
   def find_on_day_schedule(
         cls,
         day_schedule: list[ WildEncounter ],
         encounter_name: str,
         *,
         start_time: Types.ScheduleTimeKey ) -> WildEncounter | None:
      encounter_filter = WildEncounterNameFilter( name=encounter_name )

      if encounter_filter.should_return_empty():
         return None

      normalized_start_time = DateValues.normalize_schedule_time(
         start_time )

      if normalized_start_time is None:
         return None

      for row in day_schedule:
         if not encounter_filter.allows_wild_encounter_name( row.name ):
            continue

         row_start_time = DateValues.normalize_schedule_time(
            row.start_time )

         if row_start_time == normalized_start_time:
            return row

      return None
