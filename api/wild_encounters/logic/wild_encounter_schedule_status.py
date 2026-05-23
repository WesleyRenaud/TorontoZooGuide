from __future__ import annotations

from ...shared.date_values import DateValues
from ...shared.strings import SharedStrings
from ...types import DateInput
from .wild_encounter_schedule_end_input import WildEncounterScheduleEndInput
from .wild_encounter_schedule_input import WildEncounterScheduleInput


def build_wild_encounter_schedule(
      wild_encounter: str,
      start_date: DateInput,
      end_date: DateInput,
      encounter_time: str,
      monday: bool,
      tuesday: bool,
      wednesday: bool,
      thursday: bool,
      friday: bool,
      saturday: bool,
      sunday: bool,
      message: str ) -> WildEncounterScheduleInput:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.WildEncounters.not_scheduled_today(
         wild_encounter )

   return WildEncounterScheduleInput(
      wild_encounter=wild_encounter,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      encounter_time=encounter_time,
      monday=monday,
      tuesday=tuesday,
      wednesday=wednesday,
      thursday=thursday,
      friday=friday,
      saturday=saturday,
      sunday=sunday,
      message=message )


def build_wild_encounter_schedule_end(
      wild_encounter: str,
      schedule_end_date: str ) -> WildEncounterScheduleEndInput:
   return WildEncounterScheduleEndInput(
      wild_encounter=wild_encounter,
      schedule_end_date=schedule_end_date )
