from __future__ import annotations

from .guardians_talk_day_schedule_mapper import GuardiansTalkDayScheduleMapper
from .guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from .guardians_talk_occurrence_mapper import GuardiansTalkOccurrenceMapper
from .guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from .guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from ..occurrences.guardians_talk_occurrence_input import GuardiansTalkOccurrenceInput
from ..scheduling.guardians_talk_weekday_time_resolver import GuardiansTalkWeekdayTimeResolver
from ...shared.calendar_dates import DateValues
from ...types import Connection, DateKey


class GuardiansTalkOccurrenceProvider():
   @classmethod
   def occurrence_record_exists(
         cls,
         conn: Connection,
         talk_name: str,
         location: str,
         occurrence_date: DateKey,
         talk_time: str ) -> bool:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT 1
                  FROM GuardiansTalkOccurrence
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND OCCURRENCE_DATE = ?
                     AND TALK_TIME = ?
                  LIMIT 1;
            """,
            (
               talk_name,
               location,
               occurrence_date,
               talk_time,
            ) ).fetchone()

         return row is not None

      finally:
         cur.close()


   @classmethod
   def occurrence_exists(
         cls,
         conn: Connection,
         talk_name: str,
         location: str,
         occurrence_date: DateKey,
         talk_time: str ) -> bool:
      if cls.occurrence_record_exists(
            conn,
            talk_name,
            location,
            occurrence_date,
            talk_time ):
         return True

      parsed_date = DateValues.parse_date_value( occurrence_date )

      if parsed_date is None:
         return False

      for schedule_record in GuardiansTalkScheduleProvider.fetch_schedule_records_covering_date(
            conn,
            talk_name=talk_name,
            location=location,
            talk_time=talk_time,
            occurrence_date=occurrence_date ):
         if GuardiansTalkWeekdayTimeResolver.includes_weekday(
               schedule_record,
               parsed_date.weekday() ):
            return True

      return False


   @classmethod
   def save_occurrence(
         cls,
         conn: Connection,
         occurrence: GuardiansTalkOccurrenceInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GuardiansTalkOccurrence (
                     TALK_NAME,
                     LOCATION,
                     OCCURRENCE_DATE,
                     TALK_TIME
                  )
                  VALUES (?, ?, ?, ?)
                  ON CONFLICT(TALK_NAME, LOCATION, OCCURRENCE_DATE, TALK_TIME)
                  DO NOTHING;
            """,
            (
               occurrence.talk_name,
               occurrence.location,
               occurrence.occurrence_date,
               occurrence.talk_time,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def fetch_occurrence_records(
         cls,
         conn: Connection,
         talk_name: str,
         location: str,
         *,
         start_date: DateKey,
         end_date: DateKey ) -> list[ GuardiansTalkOccurrenceRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     OCCURRENCE_DATE,
                     TALK_TIME
                  FROM GuardiansTalkOccurrence
                  WHERE TALK_NAME = ?
                     AND LOCATION = ?
                     AND OCCURRENCE_DATE >= ?
                     AND OCCURRENCE_DATE <= ?
                  ORDER BY OCCURRENCE_DATE, TALK_TIME;
            """,
            (
               talk_name,
               location,
               start_date,
               end_date,
            ) )

         return GuardiansTalkOccurrenceMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_day_schedule_records_from_occurrences(
         cls,
         conn: Connection,
         target_date: DateKey ) -> list[ GuardiansTalkDayScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     t.NAME,
                     t.LOCATION,
                     t.X_COORD,
                     t.Y_COORD,
                     t.MAXIMUM_DURATION,
                     o.TALK_TIME
                  FROM MeetTheGuardiansTalk t
                  JOIN GuardiansTalkOccurrence o
                     ON t.NAME = o.TALK_NAME
                     AND t.LOCATION = o.LOCATION
                  WHERE o.OCCURRENCE_DATE = ?
                     AND NOT EXISTS (
                        SELECT 1
                        FROM GuardiansTalkCancellation c
                        WHERE c.TALK_NAME = o.TALK_NAME
                           AND c.LOCATION = o.LOCATION
                           AND c.CANCELLATION_DATE = o.OCCURRENCE_DATE
                           AND c.TALK_TIME = o.TALK_TIME
                     )
                  ORDER BY o.TALK_TIME, t.NAME, t.LOCATION;
            """,
            ( target_date, ) )

         return GuardiansTalkDayScheduleMapper.map_records( data.fetchall() )

      finally:
         cur.close()
