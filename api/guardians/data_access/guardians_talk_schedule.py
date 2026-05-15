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
