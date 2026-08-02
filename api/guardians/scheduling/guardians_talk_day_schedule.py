from __future__ import annotations

from ..data_access.guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from ..data_access.guardians_talk_occurrence import fetch_guardians_talk_day_schedule_records_from_occurrences
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_day_schedule_records_from_schedule
from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from .guardians_talk_weekday_time import guardians_talk_includes_weekday
from ...models import GuardiansTalk
from ...shared.calendar_dates import DateValues
from ...shared.scheduled_occurrences import unique_sorted_by_key
from ...types import Connection, DateKey


def fetch_guardians_talk_day_schedule_records(
      conn: Connection,
      target_date: DateKey ) -> list[ GuardiansTalkDayScheduleRecord ]:
   parsed_date = DateValues.parse_date_value( target_date )

   if parsed_date is None:
      return []

   weekday = parsed_date.weekday()
   day_records = [
      _day_schedule_record_from_schedule( schedule_record )
      for schedule_record in fetch_guardians_talk_day_schedule_records_from_schedule(
         conn,
         target_date )
      if guardians_talk_includes_weekday( schedule_record, weekday )
   ]
   day_records.extend(
      fetch_guardians_talk_day_schedule_records_from_occurrences(
         conn,
         target_date ) )

   return unique_sorted_by_key(
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


def build_guardians_talks_from_day_schedule_records(
      records: list[ GuardiansTalkDayScheduleRecord ] ) -> list[ GuardiansTalk ]:
   return [
      GuardiansTalk(
         name=record.name,
         location=record.location,
         x_coord=record.x_coord,
         y_coord=record.y_coord,
         start_time=record.talk_time,
         maximum_duration=record.maximum_duration,
         end_time=DateValues.add_minutes_to_time(
            record.talk_time,
            record.maximum_duration ),
         is_available=True,
         unavailable_message=None )
      for record in records
   ]


def _day_schedule_record_from_schedule(
      schedule_record: GuardiansTalkScheduleRecord ) -> GuardiansTalkDayScheduleRecord:
   return GuardiansTalkDayScheduleRecord(
      name=schedule_record.name,
      location=schedule_record.location,
      x_coord=schedule_record.x_coord,
      y_coord=schedule_record.y_coord,
      maximum_duration=schedule_record.maximum_duration,
      talk_time=schedule_record.talk_time )
