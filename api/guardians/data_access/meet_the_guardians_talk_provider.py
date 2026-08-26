from __future__ import annotations

from .meet_the_guardians_talk_mapper import MeetTheGuardiansTalkMapper
from .meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from ...types import Connection


class MeetTheGuardiansTalkProvider():
   @classmethod
   def fetch_guardians_talk_locations( cls, conn: Connection ) -> list[ str ]:
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


   @classmethod
   def fetch_guardians_talk_names( cls, conn: Connection ) -> list[ str ]:
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


   @classmethod
   def fetch_guardians_talk_names_at_location(
         cls,
         conn: Connection,
         location: str ) -> list[ str ]:
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


   @classmethod
   def fetch_meet_the_guardians_talk_records(
         cls,
         conn: Connection ) -> list[ MeetTheGuardiansTalkRecord ]:
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

         return MeetTheGuardiansTalkMapper.map_records( data.fetchall() )

      finally:
         cur.close()
