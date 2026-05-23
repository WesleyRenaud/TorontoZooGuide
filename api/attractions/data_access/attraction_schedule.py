from __future__ import annotations

from .attraction_schedule_record import AttractionScheduleRecord
from ..logic.attraction_opening_schedule import AttractionOpeningSchedule
from ..logic.attraction_schedule_override import AttractionScheduleOverride
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey


def attraction_schedule_overlaps_existing_schedule(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM AttractionOpeningSchedule
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


def save_attraction_opening_schedule(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> bool:
   if attraction_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

   insert_or_update_attraction_opening_schedule( conn, schedule )
   conn.commit()
   return True


def fetch_attraction_opening_schedule_conflicts(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> list[ AttractionScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               FROM AttractionOpeningSchedule
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
         AttractionScheduleRecord(
            attraction=row[ 'ATTRACTION' ],
            schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
            schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
            monday=row[ 'MONDAY' ],
            tuesday=row[ 'TUESDAY' ],
            wednesday=row[ 'WEDNESDAY' ],
            thursday=row[ 'THURSDAY' ],
            friday=row[ 'FRIDAY' ],
            saturday=row[ 'SATURDAY' ],
            sunday=row[ 'SUNDAY' ],
            holidays_only=row[ 'HOLIDAYS_ONLY' ],
            schedule_message=row[ 'SCHEDULE_MESSAGE' ] )
         for row in data.fetchall()
      ]

   finally:
      cur.close()


def delete_attraction_opening_schedule(
      conn: Connection,
      schedule: AttractionScheduleRecord ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM AttractionOpeningSchedule
               WHERE ATTRACTION = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            schedule.attraction,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def update_attraction_opening_schedule_dates(
      conn: Connection,
      schedule: AttractionScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE AttractionOpeningSchedule
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


def insert_copied_attraction_opening_schedule(
      conn: Connection,
      schedule: AttractionScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AttractionOpeningSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
         """,
         (
            schedule.attraction,
            start_date,
            end_date,
            schedule.monday,
            schedule.tuesday,
            schedule.wednesday,
            schedule.thursday,
            schedule.friday,
            schedule.saturday,
            schedule.sunday,
            schedule.holidays_only,
            schedule.schedule_message,
         ) )

   finally:
      cur.close()


def insert_or_update_attraction_opening_schedule(
      conn: Connection,
      schedule: AttractionOpeningSchedule ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AttractionOpeningSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(ATTRACTION, SCHEDULE_START_DATE) DO UPDATE SET
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            schedule.attraction,
            schedule.start_date,
            schedule.end_date,
            schedule.monday,
            schedule.tuesday,
            schedule.wednesday,
            schedule.thursday,
            schedule.friday,
            schedule.saturday,
            schedule.sunday,
            schedule.holidays_only,
            schedule.message,
         ) )

   finally:
      cur.close()


def save_attraction_schedule_override(
      conn: Connection,
      override: AttractionScheduleOverride ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO AttractionScheduleOverride (
                  ATTRACTION,
                  OVERRIDE_START_DATE,
                  OVERRIDE_END_DATE,
                  IS_CLOSED,
                  OVERRIDE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(ATTRACTION, OVERRIDE_START_DATE) DO UPDATE SET
                  OVERRIDE_END_DATE = excluded.OVERRIDE_END_DATE,
                  IS_CLOSED = excluded.IS_CLOSED,
                  OVERRIDE_MESSAGE = excluded.OVERRIDE_MESSAGE;
         """,
         (
            override.attraction,
            override.start_date,
            override.end_date,
            override.is_closed,
            override.message,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
