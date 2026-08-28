from __future__ import annotations

from .guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from .guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from .guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ..scheduling.guardians_talk_weekday_time_resolver import GuardiansTalkWeekdayTimeResolver
from ...shared.calendar_dates import DateValues
from ...shared.scheduled_occurrence_sorter import ScheduledOccurrenceSorter
from ...types import Types


class GuardiansTalkDayScheduleProvider():
   @classmethod
   def fetch_day_schedule_records(
         cls,
         conn: Types.Connection,
         target_date: Types.DateKey ) -> list[ GuardiansTalkDayScheduleRecord ]:
      parsed_date = DateValues.parse_date_value( target_date )

      if parsed_date is None:
         return []

      weekday = parsed_date.weekday()
      day_records = [
         cls._day_schedule_record_from_schedule( schedule_record )
         for schedule_record in GuardiansTalkScheduleProvider.fetch_day_schedule_records_from_schedule(
            conn,
            target_date )
         if GuardiansTalkWeekdayTimeResolver.includes_weekday( schedule_record, weekday )
      ]
      day_records.extend(
         GuardiansTalkOccurrenceProvider.fetch_day_schedule_records_from_occurrences(
            conn,
            target_date ) )

      return ScheduledOccurrenceSorter.unique_sorted_by_key(
         day_records,
         key=lambda day_record: (
            day_record.name,
            day_record.location,
            day_record.talk_time,
         ),
         sort_key=lambda day_record: (
            day_record.talk_time or '',
            day_record.name,
            day_record.location,
         ) )


   @classmethod
   def _day_schedule_record_from_schedule(
         cls,
         schedule_record: GuardiansTalkScheduleRecord ) -> GuardiansTalkDayScheduleRecord:
      return GuardiansTalkDayScheduleRecord(
         name=schedule_record.name,
         location=schedule_record.location,
         x_coord=schedule_record.x_coord,
         y_coord=schedule_record.y_coord,
         maximum_duration=schedule_record.maximum_duration,
         talk_time=schedule_record.talk_time )
