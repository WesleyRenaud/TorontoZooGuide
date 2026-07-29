from __future__ import annotations

from .attraction_hours_schedule_record import AttractionHoursScheduleRecord
from ..scheduling.attraction_hours_schedule import AttractionHoursSchedule
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey


def attraction_hours_schedule_overlaps_existing_schedule(
      conn: Connection,
      schedule: AttractionHoursSchedule ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM AttractionHoursSchedule
               WHERE ATTRACTION = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
               LIMIT 1;
         """,
         (
            schedule.attraction,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) ).fetchone()

      return row != None

   finally:
      cur.close()


def save_attraction_hours_schedule(
      conn: Connection,
      schedule: AttractionHoursSchedule ) -> bool:
   if attraction_hours_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

   insert_or_update_attraction_hours_schedule( conn, schedule )
   conn.commit()
   return True


def fetch_attraction_hours_schedule_conflicts(
      conn: Connection,
      schedule: AttractionHoursSchedule ) -> list[ AttractionHoursScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  WEEKDAY_START_TIME,
                  WEEKDAY_END_TIME,
                  WEEKEND_HOLIDAY_START_TIME,
                  WEEKEND_HOLIDAY_END_TIME
               FROM AttractionHoursSchedule
               WHERE ATTRACTION = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
         """,
         (
            schedule.attraction,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) )

      return [
         AttractionHoursScheduleRecord(
            attraction=row[ 'ATTRACTION' ],
            schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
            schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
            weekday_start_time=row[ 'WEEKDAY_START_TIME' ],
            weekday_end_time=row[ 'WEEKDAY_END_TIME' ],
            weekend_holiday_start_time=row[ 'WEEKEND_HOLIDAY_START_TIME' ],
            weekend_holiday_end_time=row[ 'WEEKEND_HOLIDAY_END_TIME' ] )
         for row in data.fetchall()
      ]

   finally:
      cur.close()


def fetch_attraction_hours_schedule_records(
      conn: Connection ) -> list[ AttractionHoursScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  WEEKDAY_START_TIME,
                  WEEKDAY_END_TIME,
                  WEEKEND_HOLIDAY_START_TIME,
                  WEEKEND_HOLIDAY_END_TIME
               FROM AttractionHoursSchedule
               ORDER BY ATTRACTION, SCHEDULE_START_DATE;
         """ )

      return [
         AttractionHoursScheduleRecord(
            attraction=row[ 'ATTRACTION' ],
            schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
            schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
            weekday_start_time=row[ 'WEEKDAY_START_TIME' ],
            weekday_end_time=row[ 'WEEKDAY_END_TIME' ],
            weekend_holiday_start_time=row[ 'WEEKEND_HOLIDAY_START_TIME' ],
            weekend_holiday_end_time=row[ 'WEEKEND_HOLIDAY_END_TIME' ] )
         for row in data.fetchall()
      ]

   finally:
      cur.close()


def delete_attraction_hours_schedule(
      conn: Connection,
      schedule: AttractionHoursScheduleRecord ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM AttractionHoursSchedule
               WHERE ATTRACTION = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            schedule.attraction,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def update_attraction_hours_schedule_dates(
      conn: Connection,
      schedule: AttractionHoursScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE AttractionHoursSchedule
               SET
                  SCHEDULE_START_DATE = ?,
                  SCHEDULE_END_DATE = ?
               WHERE ATTRACTION = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            start_date,
            end_date,
            schedule.attraction,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def insert_copied_attraction_hours_schedule(
      conn: Connection,
      schedule: AttractionHoursScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AttractionHoursSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  WEEKDAY_START_TIME,
                  WEEKDAY_END_TIME,
                  WEEKEND_HOLIDAY_START_TIME,
                  WEEKEND_HOLIDAY_END_TIME
               )
               VALUES (?, ?, ?, ?, ?, ?, ?);
         """,
         (
            schedule.attraction,
            start_date,
            end_date,
            schedule.weekday_start_time,
            schedule.weekday_end_time,
            schedule.weekend_holiday_start_time,
            schedule.weekend_holiday_end_time,
         ) )

   finally:
      cur.close()


def insert_or_update_attraction_hours_schedule(
      conn: Connection,
      schedule: AttractionHoursSchedule ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AttractionHoursSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  WEEKDAY_START_TIME,
                  WEEKDAY_END_TIME,
                  WEEKEND_HOLIDAY_START_TIME,
                  WEEKEND_HOLIDAY_END_TIME
               )
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(ATTRACTION, SCHEDULE_START_DATE) DO UPDATE SET
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  WEEKDAY_START_TIME = excluded.WEEKDAY_START_TIME,
                  WEEKDAY_END_TIME = excluded.WEEKDAY_END_TIME,
                  WEEKEND_HOLIDAY_START_TIME = excluded.WEEKEND_HOLIDAY_START_TIME,
                  WEEKEND_HOLIDAY_END_TIME = excluded.WEEKEND_HOLIDAY_END_TIME;
         """,
         (
            schedule.attraction,
            schedule.start_date,
            schedule.end_date,
            schedule.weekday_start_time,
            schedule.weekday_end_time,
            schedule.weekend_holiday_start_time,
            schedule.weekend_holiday_end_time,
         ) )

   finally:
      cur.close()
