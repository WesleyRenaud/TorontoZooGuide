from __future__ import annotations

from ...app_strings import format_app_string
from ...shared.calendar_dates import DateValues
from ...types import DateInput
from .wild_encounter_schedule_input import WildEncounterScheduleInput


class WildEncounterScheduleBuilder():
   @classmethod
   def build(
         cls,
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
         message = format_app_string(
            'guestStatus.wildEncounters.notScheduledToday',
            wildEncounter=wild_encounter )

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
