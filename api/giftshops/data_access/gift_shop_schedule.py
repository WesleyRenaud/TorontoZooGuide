def gift_shop_schedule_overlaps_existing_schedule( conn, schedule ):
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM GiftShopOpeningSchedule
               WHERE GIFT_SHOP = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, '9999-12-31' )
                  AND COALESCE( SCHEDULE_END_DATE, '9999-12-31' ) >= ?
               LIMIT 1;
         """,
         (
            schedule.gift_shop,
            schedule.start_date,
            schedule.end_date,
            schedule.start_date,
         ) ).fetchone()

      return row != None

   finally:
      cur.close()


def save_gift_shop_opening_schedule( conn, schedule ):
   if gift_shop_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

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

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_gift_shop_schedule_override( conn, override ):
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
