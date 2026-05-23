from __future__ import annotations

from ..logic.restaurant_opening_schedule import RestaurantOpeningSchedule
from ..logic.restaurant_schedule_override import RestaurantScheduleOverride
from .restaurant_schedule_record import RestaurantScheduleRecord
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey


def restaurant_schedule_overlaps_existing_schedule(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM RestaurantOpeningSchedule
               WHERE RESTAURANT = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
               LIMIT 1;
         """,
         (
            schedule.restaurant,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) ).fetchone()

      return row != None

   finally:
      cur.close()


def save_restaurant_opening_schedule(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> bool:
   if restaurant_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

   insert_or_update_restaurant_opening_schedule( conn, schedule )
   conn.commit()
   return True


def fetch_restaurant_opening_schedule_conflicts(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> list[ RestaurantScheduleRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  RESTAURANT,
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
               FROM RestaurantOpeningSchedule
               WHERE RESTAURANT = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                  AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
         """,
         (
            schedule.restaurant,
            schedule.start_date,
            schedule.end_date,
            OPEN_ENDED_SQL_DATE,
            OPEN_ENDED_SQL_DATE,
            schedule.start_date,
         ) )

      return [
         RestaurantScheduleRecord(
            restaurant=row[ 'RESTAURANT' ],
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


def delete_restaurant_opening_schedule(
      conn: Connection,
      schedule: RestaurantScheduleRecord ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   DELETE FROM RestaurantOpeningSchedule
               WHERE RESTAURANT = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            schedule.restaurant,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def update_restaurant_opening_schedule_dates(
      conn: Connection,
      schedule: RestaurantScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE RestaurantOpeningSchedule
               SET
                  SCHEDULE_START_DATE = ?,
                  SCHEDULE_END_DATE = ?
               WHERE RESTAURANT = ?
                  AND SCHEDULE_START_DATE = ?;
         """,
         (
            start_date,
            end_date,
            schedule.restaurant,
            schedule.schedule_start_date,
         ) )

   finally:
      cur.close()


def insert_copied_restaurant_opening_schedule(
      conn: Connection,
      schedule: RestaurantScheduleRecord,
      start_date: DateKey,
      end_date: DateKey | None ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO RestaurantOpeningSchedule (
                  RESTAURANT,
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
            schedule.restaurant,
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


def insert_or_update_restaurant_opening_schedule(
      conn: Connection,
      schedule: RestaurantOpeningSchedule ) -> None:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO RestaurantOpeningSchedule (
                  RESTAURANT,
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
               ON CONFLICT(RESTAURANT, SCHEDULE_START_DATE) DO UPDATE SET
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
            schedule.restaurant,
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


def save_restaurant_schedule_override(
      conn: Connection,
      override: RestaurantScheduleOverride ) -> bool:
   cur = conn.cursor()

   try:
      cur.execute(
         """   INSERT INTO RestaurantScheduleOverride (
                  RESTAURANT,
                  OVERRIDE_START_DATE,
                  OVERRIDE_END_DATE,
                  IS_CLOSED,
                  OVERRIDE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(RESTAURANT, OVERRIDE_START_DATE) DO UPDATE SET
                  OVERRIDE_END_DATE = excluded.OVERRIDE_END_DATE,
                  IS_CLOSED = excluded.IS_CLOSED,
                  OVERRIDE_MESSAGE = excluded.OVERRIDE_MESSAGE;
         """,
         (
            override.restaurant,
            override.start_date,
            override.end_date,
            override.is_closed,
            override.message,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
