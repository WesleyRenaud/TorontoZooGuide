from __future__ import annotations

from ...shared.calendar_dates import DateValues
from ...types import DateInput
from .wild_encounter_schedule_end_input import WildEncounterScheduleEndInput


def build_wild_encounter_schedule_end(
      wild_encounter: str,
      schedule_end_date: DateInput,
      encounter_time: str,
   ) -> WildEncounterScheduleEndInput:
   if not schedule_end_date:
      schedule_end_date = DateValues.today_date_key()

   return WildEncounterScheduleEndInput(
      wild_encounter=wild_encounter,
      schedule_end_date=schedule_end_date,
      encounter_time=encounter_time )
