def restaurant_schedule_overlaps_existing_schedule( conn, schedule ):
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT 1
               FROM RestaurantOpeningSchedule
               WHERE RESTAURANT = ?
                  AND SCHEDULE_START_DATE != ?
                  AND SCHEDULE_START_DATE <= COALESCE( ?, '9999-12-31' )
                  AND COALESCE( SCHEDULE_END_DATE, '9999-12-31' ) >= ?
               LIMIT 1;
         """,
         (
            schedule.restaurant,
            schedule.start_date,
            schedule.end_date,
            schedule.start_date,
         ) ).fetchone()

      return row != None

   finally:
      cur.close()


def save_restaurant_opening_schedule( conn, schedule ):
   if restaurant_schedule_overlaps_existing_schedule( conn, schedule ):
      return False

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

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def save_restaurant_schedule_override( conn, override ):
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
