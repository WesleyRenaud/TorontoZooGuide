from __future__ import annotations

from .exhibit_closure_mapper import ExhibitClosureMapper
from .exhibit_closure_record import ExhibitClosureRecord
from ...types import Types


class ExhibitStatusProvider():
   @classmethod
   def save_closed_status(
         cls,
         conn: Types.Connection,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO ExhibitStatus (
                     EXHIBIT,
                     IS_CLOSED,
                     CLOSED_MESSAGE,
                     CLOSED_START,
                     CLOSED_END
                  )
                  VALUES (?, 1, ?, ?, ?)
                  ON CONFLICT(EXHIBIT) DO UPDATE SET
                     IS_CLOSED = 1,
                     CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                     CLOSED_START = excluded.CLOSED_START,
                     CLOSED_END = excluded.CLOSED_END;
            """,
            (
               exhibit,
               message,
               start_date,
               end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def save_open_status(
         cls,
         conn: Types.Connection,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO ExhibitStatus (
                     EXHIBIT,
                     IS_CLOSED,
                     CLOSED_MESSAGE,
                     CLOSED_START,
                     CLOSED_END
                  )
                  VALUES (?, 0, NULL, ?, ?)
                  ON CONFLICT(EXHIBIT) DO UPDATE SET
                     IS_CLOSED = 0,
                     CLOSED_MESSAGE = NULL,
                     CLOSED_START = excluded.CLOSED_START,
                     CLOSED_END = excluded.CLOSED_END;
            """,
            (
               exhibit,
               start_date,
               end_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def fetch_closure_records( cls, conn: Types.Connection ) -> list[ ExhibitClosureRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     EXHIBIT,
                     CLOSED_START,
                     CLOSED_END
                  FROM ExhibitStatus
                  WHERE IS_CLOSED = 1;
            """ )

         return ExhibitClosureMapper.map_records( data.fetchall() )

      finally:
         cur.close()
