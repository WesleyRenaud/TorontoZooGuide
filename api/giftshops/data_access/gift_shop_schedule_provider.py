from __future__ import annotations

from .gift_shop_schedule_record import GiftShopScheduleRecord
from ..scheduling.gift_shop_opening_schedule import GiftShopOpeningSchedule
from ..scheduling.gift_shop_schedule_override import GiftShopScheduleOverride
from ...shared.constants import OPEN_ENDED_SQL_DATE
from ...types import Connection, DateKey


class GiftShopScheduleProvider():
   @classmethod
   def overlaps_existing_schedule(
         cls,
         conn: Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      cur = conn.cursor()

      try:
         row = cur.execute(
            """   SELECT 1
                  FROM GiftShopOpeningSchedule
                  WHERE GIFT_SHOP = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?
                  LIMIT 1;
            """,
            (
               schedule.gift_shop,
               schedule.start_date,
               schedule.end_date,
               OPEN_ENDED_SQL_DATE,
               OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) ).fetchone()

         return row != None

      finally:
         cur.close()


   @classmethod
   def save_opening_schedule(
         cls,
         conn: Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      if cls.overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_opening_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def fetch_opening_schedule_conflicts(
         cls,
         conn: Connection,
         schedule: GiftShopOpeningSchedule ) -> list[ GiftShopScheduleRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     GIFT_SHOP,
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
                  FROM GiftShopOpeningSchedule
                  WHERE GIFT_SHOP = ?
                     AND SCHEDULE_START_DATE != ?
                     AND SCHEDULE_START_DATE <= COALESCE( ?, ? )
                     AND COALESCE( SCHEDULE_END_DATE, ? ) >= ?;
            """,
            (
               schedule.gift_shop,
               schedule.start_date,
               schedule.end_date,
               OPEN_ENDED_SQL_DATE,
               OPEN_ENDED_SQL_DATE,
               schedule.start_date,
            ) )

         return [
            GiftShopScheduleRecord(
               gift_shop=row[ 'GIFT_SHOP' ],
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


   @classmethod
   def delete_opening_schedule(
         cls,
         conn: Connection,
         schedule: GiftShopScheduleRecord ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   DELETE FROM GiftShopOpeningSchedule
                  WHERE GIFT_SHOP = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               schedule.gift_shop,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def update_opening_schedule_dates(
         cls,
         conn: Connection,
         schedule: GiftShopScheduleRecord,
         start_date: DateKey,
         end_date: DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE GiftShopOpeningSchedule
                  SET
                     SCHEDULE_START_DATE = ?,
                     SCHEDULE_END_DATE = ?
                  WHERE GIFT_SHOP = ?
                     AND SCHEDULE_START_DATE = ?;
            """,
            (
               start_date,
               end_date,
               schedule.gift_shop,
               schedule.schedule_start_date,
            ) )

      finally:
         cur.close()


   @classmethod
   def insert_copied_opening_schedule(
         cls,
         conn: Connection,
         schedule: GiftShopScheduleRecord,
         start_date: DateKey,
         end_date: DateKey | None ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GiftShopOpeningSchedule (
                     GIFT_SHOP,
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
               schedule.gift_shop,
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


   @classmethod
   def insert_or_update_opening_schedule(
         cls,
         conn: Connection,
         schedule: GiftShopOpeningSchedule ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GiftShopOpeningSchedule (
                     GIFT_SHOP,
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
                  ON CONFLICT(GIFT_SHOP, SCHEDULE_START_DATE) DO UPDATE SET
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
               schedule.gift_shop,
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


   @classmethod
   def save_schedule_override(
         cls,
         conn: Connection,
         override: GiftShopScheduleOverride ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO GiftShopScheduleOverride (
                     GIFT_SHOP,
                     OVERRIDE_START_DATE,
                     OVERRIDE_END_DATE,
                     IS_CLOSED,
                     OVERRIDE_MESSAGE
                  )
                  VALUES (?, ?, ?, ?, ?)
                  ON CONFLICT(GIFT_SHOP, OVERRIDE_START_DATE) DO UPDATE SET
                     OVERRIDE_END_DATE = excluded.OVERRIDE_END_DATE,
                     IS_CLOSED = excluded.IS_CLOSED,
                     OVERRIDE_MESSAGE = excluded.OVERRIDE_MESSAGE;
            """,
            (
               override.gift_shop,
               override.start_date,
               override.end_date,
               override.is_closed,
               override.message,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()
