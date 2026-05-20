from .meet_the_guardians_talk_mapper import map_meet_the_guardians_talk_records


def fetch_guardians_talk_locations( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT DISTINCT
                  t.LOCATION
               FROM MeetTheGuardiansTalk t
               WHERE t.LOCATION IS NOT NULL
               ORDER BY t.LOCATION;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_guardians_talk_names( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME
               FROM MeetTheGuardiansTalk t;
         """ )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_guardians_talk_names_at_location( conn, location ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """  SELECT
                  t.NAME
              FROM MeetTheGuardiansTalk t
              WHERE t.LOCATION = ?;
         """,
         ( location, ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


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
