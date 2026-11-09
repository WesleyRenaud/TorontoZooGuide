from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.scheduling.guardians_talk_schedule_conflict_resolver import GuardiansTalkScheduleConflictResolver
from api.guardians.scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.shared.schedule_row_input import SCHEDULE_ROW_WEEKDAY_KEYS
from .guardians_talk_window_correction import GuardiansTalkWindowCorrection
from tools.checks.check_report import CheckReport
from tools.checks.schedule_slot_group import ScheduleSlotGroup
from tools.checks.week_schedule import WeekSchedule


class GuardiansTalkWindowFixer():
   @classmethod
   def weekday_flags( cls, indexes: set[ int ] ) -> dict[ str, bool ]:
      return {
         day: index in indexes
         for index, day in enumerate( SCHEDULE_ROW_WEEKDAY_KEYS )
      }


   @classmethod
   def detail( cls, correction: GuardiansTalkWindowCorrection ) -> str:
      lines = [
         CheckReport.detail_item(
            CheckReport.text( 'checks.setScheduleFrom' )
            + DateValues.format_display_date_value( correction.start )
            + CheckReport.text( 'checks.dateThrough' )
            + DateValues.format_display_date_value( correction.end )
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
   def rows_for(
         cls,
         correction: GuardiansTalkWindowCorrection ) -> list[ GuardiansTalkScheduleRecord ]:
      return [
         schedule
         for schedule in GuardiansTalkScheduleProvider.fetch_schedule_records(
            RequestConnectionProvider.get(),
         )
         if schedule.name == correction.name and schedule.location == correction.location
      ]


   @classmethod
   def enclosures(
         cls,
         correction: GuardiansTalkWindowCorrection,
         rows: list[ GuardiansTalkScheduleRecord ] ) -> set[ str | None ]:
      if rows != []:
         return { schedule.enclosure_name for schedule in rows }

      return {
         talk.enclosure_name
         for talk in GuardiansCoordinator.get_guardians_talk_details()
         if talk.name == correction.name and talk.location == correction.location
      }


   @classmethod
   def write( cls, correction: GuardiansTalkWindowCorrection ) -> None:
      rows = cls.rows_for( correction )
      enclosures = cls.enclosures( correction, rows )
      connection = RequestConnectionProvider.get()

      for schedule in rows:
         GuardiansTalkScheduleProvider.delete_schedule( connection, schedule )

      for group in ScheduleSlotGroup.from_slots( correction.slots ):
         talk_time = DateValues.format_display_time_value( group.time )

         if talk_time == None:
            continue

         for enclosure in enclosures:
            GuardiansTalkScheduleConflictResolver.save_replacing_overlaps(
               RequestConnectionProvider.get(),
               GuardiansTalkScheduleInput(
                  talk_name=correction.name,
                  location=correction.location,
                  start_date=correction.start.isoformat(),
                  end_date=correction.end.isoformat(),
                  talk_time=talk_time,
                  message='',
                  enclosure_name=enclosure,
                  **cls.weekday_flags( group.weekdays() ),
               ),
            )


   @classmethod
   def correction(
         cls,
         name: str,
         location: str,
         schedule: WeekSchedule ) -> GuardiansTalkWindowCorrection:
      return GuardiansTalkWindowCorrection(
         name=name,
         location=location,
         start=schedule.start,
         end=schedule.end,
         slots=set( schedule.slots ),
      )


   @classmethod
   def apply(
         cls,
         database: Path,
         correction: GuardiansTalkWindowCorrection ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.write( correction )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return cls.detail( correction )
