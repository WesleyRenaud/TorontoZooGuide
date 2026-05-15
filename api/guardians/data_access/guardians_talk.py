from .meet_the_guardians_talk_mapper import map_meet_the_guardians_talk_records


def fetch_meet_the_guardians_talk_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  NAME,
                  LOCATION,
                  X_COORD,
                  Y_COORD,
                  MAXIMUM_DURATION
               FROM MeetTheGuardiansTalk;
         """ )

      return map_meet_the_guardians_talk_records( data.fetchall() )

   finally:
      cur.close()
