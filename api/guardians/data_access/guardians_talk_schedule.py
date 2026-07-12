from __future__ import annotations

from typing import TYPE_CHECKING

from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey

if TYPE_CHECKING:
   from ..scheduling.guardians_talk_schedule_end_input import GuardiansTalkScheduleEndInput
   from ..scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput

from .guardians_talk_cancellation_mapper import map_guardians_talk_cancellation_records
from .guardians_talk_schedule_mapper import map_guardians_talk_schedule_records
from .guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord


def fetch_guardians_talk_schedule_records( conn: Connection ) -> list[ GuardiansTalkScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  t.MAXIMUM_DURATION,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.TALK_TIME
               FROM MeetTheGuardiansTalk t
               JOIN GuardiansTalkSchedule s
                  ON t.NAME = s.TALK_NAME
                  AND t.LOCATION = s.LOCATION;
         """ )

      return map_guardians_talk_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_guardians_talk_schedule_records_for_talk(
      conn: Connection,
      talk_name: str,
      location: str ) -> list[ GuardiansTalkScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  t.MAXIMUM_DURATION,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.TALK_TIME
               FROM MeetTheGuardiansTalk t
               JOIN GuardiansTalkSchedule s
                  ON t.NAME = s.TALK_NAME
                  AND t.LOCATION = s.LOCATION
               WHERE s.TALK_NAME = ?
               AND s.LOCATION = ?
               ORDER BY s.TALK_TIME, s.SCHEDULE_START_DATE;
         """,
         (
            talk_name,
            location,
         ) )

      return map_guardians_talk_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_guardians_talk_schedule_records_for_occurrences(
      conn: Connection,
      talk_name: str,
      location: str ) -> list[ GuardiansTalkScheduleRecord ]:
   return fetch_guardians_talk_schedule_records_for_talk(
      conn,
      talk_name=talk_name,
      location=location )


def fetch_guardians_talk_cancellation_records(
      conn: Connection,
      talk_name: str,
      location: str ) -> list[ GuardiansTalkCancellationRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  CANCELLATION_DATE,
                  TALK_TIME
               FROM GuardiansTalkCancellation
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            talk_name,
            location,
         ) )

      return map_guardians_talk_cancellation_records( data.fetchall() )

   finally:
      cur.close()



def fetch_guardians_talk_occurrence_is_cancelled(
      conn: Connection,
      talk_name: str,
      location: str,
      cancellation_date: DateKey,
      talk_time: str ) -> bool:

   cur = conn.cursor()

   try:
      cancellation_data = cur.execute(
         """   SELECT 1
                  FROM GuardiansTalkCancellation
                  WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND CANCELLATION_DATE = ?
                  AND TALK_TIME = ?;
            """,
         (
            talk_name,
            location,
            cancellation_date,
            talk_time,
         ) )

      return cancellation_data.fetchone() != None

   finally:
      cur.close()



def fetch_guardians_talk_schedule_times(
      conn: Connection,
      talk_name: str,
      location: str,
      target_date: DateKey ) -> list[ str ]:
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT DISTINCT TALK_TIME
               FROM GuardiansTalkSchedule
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND SCHEDULE_START_DATE <= ?
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
               ORDER BY TALK_TIME;""",
         (
            talk_name,
            location,
            target_date,
            OPEN_ENDED_SQL_DATE,
            target_date,
         ) ).fetchall()

      return [ row[ 0 ] for row in rows ]

   finally:
      cur.close()



def guardians_talk_schedule_overlaps_existing_schedule(
      conn: Connection,
      schedule: GuardiansTalkScheduleInput ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM GuardiansTalkSchedule
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND TALK_TIME = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
               LIMIT 1;
         """,
         (
            schedule.talk_name,
            schedule.location,
            schedule.talk_time,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) ).fetchone()

      return row != None

   finally:
      cur.close()


def fetch_guardians_talk_schedule_conflicts(
      conn: Connection,
      schedule: GuardiansTalkScheduleInput ) -> list[ GuardiansTalkScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  t.MAXIMUM_DURATION,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.TALK_TIME
               FROM MeetTheGuardiansTalk t
               JOIN GuardiansTalkSchedule s
                  ON t.NAME = s.TALK_NAME
                  AND t.LOCATION = s.LOCATION
               WHERE s.TALK_NAME = ?
                  AND s.LOCATION = ?
                  AND s.TALK_TIME = ?
                  AND s.SCHEDULE_START_DATE != ?
                  AND s.SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( s.SCHEDULE_END_DATE, ? ) >= ?;
         """,
         (
            schedule.talk_name,
            schedule.location,
            schedule.talk_time,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) )

      return map_guardians_talk_schedule_records( data.fetchall() )

   finally:
      cur.close()


def delete_guardians_talk_schedule(
      conn: Connection,
      schedule: GuardiansTalkScheduleRecord ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM GuardiansTalkSchedule
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND TALK_TIME = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            schedule.name,
            schedule.location,
            schedule.talk_time,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def update_guardians_talk_schedule_dates(
      conn: Connection,
      schedule: GuardiansTalkScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE GuardiansTalkSchedule
               SET
                  SCHEDULE_START_DATE = ?,
                  SCHEDULE_END_DATE = ?
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND TALK_TIME = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            start_date,
            end_date,
            schedule.name,
            schedule.location,
            schedule.talk_time,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def insert_copied_guardians_talk_schedule(
      conn: Connection,
      schedule: GuardiansTalkScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO GuardiansTalkSchedule (
                  TALK_NAME,
                  LOCATION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  TALK_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               SELECT
                  TALK_NAME,
                  LOCATION,
                  ?,
                  ?,
                  TALK_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               FROM GuardiansTalkSchedule
               WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND TALK_TIME = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            start_date,
            end_date,
            schedule.name,
            schedule.location,
            schedule.talk_time,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def insert_or_update_guardians_talk_schedule(
      conn: Connection,
      schedule: GuardiansTalkScheduleInput ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO GuardiansTalkSchedule (
                  TALK_NAME,
                  LOCATION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  TALK_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION, TALK_TIME, SCHEDULE_START_DATE) DO UPDATE SET
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            schedule.talk_name,
            schedule.location,
            schedule.start_date,
            schedule.end_date,
            schedule.talk_time,
            schedule.monday,
            schedule.tuesday,
            schedule.wednesday,
            schedule.thursday,
            schedule.friday,
            schedule.saturday,
            schedule.sunday,
            schedule.message,
         ) )

   finally:
      cur.close()


def save_guardians_talk_schedule(
      conn: Connection,
      schedule: GuardiansTalkScheduleInput ) -> bool:
   if guardians_talk_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

   insert_or_update_guardians_talk_schedule( conn, schedule )
   conn.commit()
   return True



def save_guardians_talk_schedule_end(
      conn: Connection,
      schedule_end: GuardiansTalkScheduleEndInput ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE GuardiansTalkSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE TALK_NAME = ?
               AND LOCATION = ?
               AND TALK_TIME = ?
               AND SCHEDULE_START_DATE <= ?
               AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
         """,
         (
            schedule_end.schedule_end_date,
            schedule_end.talk_name,
            schedule_end.location,
            schedule_end.talk_time,
            schedule_end.schedule_end_date,
            OPEN_ENDED_SQL_DATE,
            schedule_end.schedule_end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
