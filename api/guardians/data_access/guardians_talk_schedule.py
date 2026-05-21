from .guardians_talk_cancellation_mapper import map_guardians_talk_cancellation_records
from .guardians_talk_schedule_mapper import map_guardians_talk_schedule_record
from .guardians_talk_schedule_mapper import map_guardians_talk_schedule_records


def fetch_guardians_talk_schedule_records( conn ):
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


def fetch_guardians_talk_schedule_record_for_occurrences( conn, talk_name, location ):
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
               AND s.LOCATION = ?;
         """,
         (
            talk_name,
            location,
         ) )

      row = data.fetchone()

      if row == None:
         return None

      return map_guardians_talk_schedule_record( row )

   finally:
      cur.close()


def fetch_guardians_talk_cancellation_records( conn, talk_name, location ):
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
      conn,
      talk_name,
      location,
      cancellation_date,
      talk_time ):

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



def save_guardians_talk_schedule( conn, schedule ):
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
               ON CONFLICT(TALK_NAME, LOCATION) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  TALK_TIME = excluded.TALK_TIME,
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

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()



def save_guardians_talk_schedule_end( conn, schedule_end ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE GuardiansTalkSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            schedule_end.schedule_end_date,
            schedule_end.talk_name,
            schedule_end.location,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
