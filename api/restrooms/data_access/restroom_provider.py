from __future__ import annotations

from .restroom_mapper import RestroomMapper
from .restroom_record import RestroomRecord
from ...types import Connection


class RestroomProvider():
   @classmethod
   def fetch_restroom_names( cls, conn: Connection ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     r.TITLE
                  FROM Restroom r;
            """ )

         return [ row[ 0 ] for row in data.fetchall() ]

      finally:
         cur.close()


   @classmethod
   def fetch_restroom_records( cls, conn: Connection ) -> list[ RestroomRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     r.TITLE,
                     r.X_COORD,
                     r.Y_COORD,
                     s.IS_CLOSED,
                     s.CLOSED_MESSAGE,
                     s.CLOSED_START,
                     s.CLOSED_END,
                     a.ALERT_MESSAGE,
                     a.ALERT_START_DATE,
                     a.ALERT_END_DATE
                  FROM Restroom r
                  LEFT JOIN RestroomStatus s
                     ON s.RESTROOM = r.TITLE
                  LEFT JOIN RestroomAlert a
                     ON a.RESTROOM = r.TITLE;
            """ )

         return RestroomMapper.map_records( data.fetchall() )

      finally:
         cur.close()
