from __future__ import annotations

from ..data_access.wild_encounter_schedule_listing_record import WildEncounterScheduleListingRecord
from ...shared.date_values import DateValues
from .wild_encounter_schedule import WildEncounterSchedule


class WildEncounterSchedulesBuilder():
   @classmethod
   def build(
         cls,
         records: list[ WildEncounterScheduleListingRecord ] ) -> list[ WildEncounterSchedule ]:
      return [
         cls._schedule( record )
         for record in records
      ]


   @classmethod
   def _schedule( cls, record: WildEncounterScheduleListingRecord ) -> WildEncounterSchedule:
      return WildEncounterSchedule(
         name=record.wild_encounter,
         start=DateValues.parse_date_value( record.schedule_start_date ),
         end=DateValues.parse_date_value( record.schedule_end_date ),
         encounter_time=record.encounter_time,
         monday=record.monday,
         tuesday=record.tuesday,
         wednesday=record.wednesday,
         thursday=record.thursday,
         friday=record.friday,
         saturday=record.saturday,
         sunday=record.sunday,
      )
