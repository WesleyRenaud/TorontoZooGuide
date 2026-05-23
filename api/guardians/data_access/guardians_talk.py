from __future__ import annotations

from .meet_the_guardians_talk_mapper import map_meet_the_guardians_talk_records
from .meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from ...types import Connection


def fetch_guardians_talk_locations( conn: Connection ) -> list[ str ]:
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


def fetch_guardians_talk_names( conn: Connection ) -> list[ str ]:
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


def fetch_guardians_talk_names_at_location( conn: Connection, location: str ) -> list[ str ]:
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


def fetch_meet_the_guardians_talk_records( conn: Connection ) -> list[ MeetTheGuardiansTalkRecord ]:
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
