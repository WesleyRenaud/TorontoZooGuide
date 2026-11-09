from __future__ import annotations

from datetime import date
from datetime import timedelta
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.shared.schedule_row_input import SCHEDULE_ROW_WEEKDAY_KEYS
from api.wild_encounters.domain.wild_encounter_schedule import WildEncounterSchedule
from api.wild_encounters.scheduling.wild_encounter_schedule_conflict_resolver import WildEncounterScheduleConflictResolver
from api.wild_encounters.scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput
from .encounter_schedule_correction import EncounterScheduleCorrection
from tools.checks.check_report import CheckReport
from tools.checks.encounter_schedule_slots import EncounterScheduleSlots
from tools.checks.schedule_slot import ScheduleSlot
from tools.checks.schedule_slot_group import ScheduleSlotGroup


class WildEncounterWindowFixer():
   @classmethod
   def weekday_flags( cls, indexes: set[ int ] ) -> dict[ str, bool ]:
      return {
         day: index in indexes
         for index, day in enumerate( SCHEDULE_ROW_WEEKDAY_KEYS )
      }


   @classmethod
   def slots_from_schedules(
         cls,
         name: str,
         schedules: list[ WildEncounterSchedule ] ) -> set[ ScheduleSlot ]:
      slots = set()

      for schedule in schedules:
         if schedule.name != name:
            continue

         parsed = DateValues.parse_time_value( schedule.encounter_time )

         if parsed == None:
            continue

         for index in schedule.weekday_indexes():
            slots.add( ScheduleSlot( weekday=index, time=parsed ) )

      return slots


   @classmethod
   def schedule_slots(
         cls,
         name: str,
         schedules: list[ WildEncounterSchedule ],
         website_slots: EncounterScheduleSlots ) -> set[ ScheduleSlot ]:
      stored = cls.slots_from_schedules( name, schedules )

      if stored != set():
         return stored

      return website_slots.for_name( name )


   @classmethod
   def stored_start(
         cls,
         schedules: list[ WildEncounterSchedule ],
         name: str ) -> date | None:
      starts = [
         schedule.start
         for schedule in schedules
         if schedule.name == name and schedule.start != None
      ]

      if starts == []:
         return None

      return min( starts )


   @classmethod
   def aligned_start(
         cls,
         bookable: list[ date ],
         app_dates: list[ date ],
         schedules: list[ WildEncounterSchedule ],
         name: str,
         first: date ) -> date:
      stored = cls.stored_start( schedules, name )

      if bookable == []:
         if stored == None:
            return first

         return stored

      earliest = min( bookable )

      if stored != None and stored <= earliest and all( day >= earliest for day in app_dates ):
         return stored

      return earliest


   @classmethod
   def aligned_end( cls, bookable: list[ date ], first: date ) -> date:
      if bookable == []:
         return first

      return max( bookable ) + timedelta( days=1 )


   @classmethod
   def detail( cls, correction: EncounterScheduleCorrection ) -> str:
      last = correction.end - timedelta( days=1 )
      lines = [
         CheckReport.detail_item(
            CheckReport.text( 'checks.setScheduleFrom' )
            + DateValues.format_display_date_value( correction.start )
            + CheckReport.text( 'checks.dateThrough' )
            + DateValues.format_display_date_value( last )
            + CheckReport.text( 'checks.period' )
         ),
      ]
      lines.extend(
         CheckReport.detail_item(
            CheckReport.text( 'format.bulletItem' ) + group.description()
         )
         for group in ScheduleSlotGroup.from_slots( correction.slots )
      )
      return CheckReport.join_lines( lines )


   @classmethod
   def write( cls, correction: EncounterScheduleCorrection ) -> None:
      for group in ScheduleSlotGroup.from_slots( correction.slots ):
         encounter_time = DateValues.format_display_time_value( group.time )

         if encounter_time == None:
            continue

         WildEncounterScheduleConflictResolver.save_replacing_overlaps(
            RequestConnectionProvider.get(),
            WildEncounterScheduleInput(
               wild_encounter=correction.name,
               start_date=correction.start.isoformat(),
               end_date=correction.end.isoformat(),
               encounter_time=encounter_time,
               message='',
               **cls.weekday_flags( group.weekdays() ),
            ),
         )


   @classmethod
   def correction(
         cls,
         name: str,
         bookable: list[ date ],
         app_dates: list[ date ],
         schedules: list[ WildEncounterSchedule ],
         website_slots: EncounterScheduleSlots,
         first: date ) -> EncounterScheduleCorrection:
      return EncounterScheduleCorrection(
         name=name,
         start=cls.aligned_start( bookable, app_dates, schedules, name, first ),
         end=cls.aligned_end( bookable, first ),
         slots=cls.schedule_slots( name, schedules, website_slots ),
      )


   @classmethod
   def apply(
         cls,
         database: Path,
         correction: EncounterScheduleCorrection ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.write( correction )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return cls.detail( correction )
