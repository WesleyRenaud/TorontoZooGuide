from __future__ import annotations

from ..data_access.guardians_talk_occurrence import guardians_talk_occurrence_record_exists
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records_covering_date
from .guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput
from ..scheduling.guardians_talk_weekday_time import guardians_talk_includes_weekday
from ...shared.calendar_dates import DateValues
from ...types import Connection, DateKey


def build_guardians_talk_occurrence(
      talk: str,
      location: str,
      date: DateKey,
      time: str ) -> GuardiansTalkOccurrenceInput:
   return GuardiansTalkOccurrenceInput(
      talk_name=talk,
      location=location,
      occurrence_date=date,
      talk_time=time )


def guardians_talk_occurrence_exists(
      conn: Connection,
      talk_name: str,
      location: str,
      occurrence_date: DateKey,
      talk_time: str ) -> bool:
   if guardians_talk_occurrence_record_exists(
         conn,
         talk_name,
         location,
         occurrence_date,
         talk_time ):
      return True

   parsed_date = DateValues.parse_date_value( occurrence_date )

   if parsed_date is None:
      return False

   for schedule_record in fetch_guardians_talk_schedule_records_covering_date(
         conn,
         talk_name=talk_name,
         location=location,
         talk_time=talk_time,
         occurrence_date=occurrence_date ):
      if guardians_talk_includes_weekday(
            schedule_record,
            parsed_date.weekday() ):
         return True

   return False
