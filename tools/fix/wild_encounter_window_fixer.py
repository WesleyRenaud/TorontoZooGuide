from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.shared.schedule_row_input import SCHEDULE_ROW_WEEKDAY_KEYS
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from api.wild_encounters.scheduling.wild_encounter_schedule_conflict_resolver import WildEncounterScheduleConflictResolver
from api.wild_encounters.scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput
from .encounter_schedule_correction import EncounterScheduleCorrection
from tools.checks.check_report import CheckReport
from tools.checks.schedule_slot_group import ScheduleSlotGroup
from tools.checks.week_schedule import WeekSchedule


class WildEncounterWindowFixer():
   @classmethod
   def weekday_flags( cls, indexes: set[ int ] ) -> dict[ str, bool ]:
      return {
         day: index in indexes
         for index, day in enumerate( SCHEDULE_ROW_WEEKDAY_KEYS )
      }


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
      connection = RequestConnectionProvider.get()
      WildEncounterScheduleProvider.delete_schedules( connection, correction.name )

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
         schedule: WeekSchedule ) -> EncounterScheduleCorrection:
      return EncounterScheduleCorrection(
         name=name,
         start=schedule.start,
         end=schedule.end + timedelta( days=1 ),
         slots=set( schedule.slots ),
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
