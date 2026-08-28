from __future__ import annotations

from ..inputs.update_create_input import UpdateCreateInput
from ..inputs.update_edit_input import UpdateEditInput
from ..inputs.update_end_input import UpdateEndInput
from ...models import Update
from ...types import Types
from .update_mapper import UpdateMapper


class UpdateProvider():
   @classmethod
   def insert_update( cls, conn: Types.Connection, update: UpdateCreateInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   INSERT INTO ZooUpdate (
                     TITLE,
                     DESCRIPTION,
                     UPDATE_TYPE,
                     START_DATE,
                     END_DATE
                  )
                  VALUES (?, ?, ?, ?, ?)
                  ON CONFLICT(TITLE, START_DATE) DO NOTHING;
            """,
            (
               update.title,
               update.description,
               update.update_type,
               update.start_date,
               update.end_date or None,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def update_end_date( cls, conn: Types.Connection, update: UpdateEndInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE ZooUpdate
                  SET END_DATE = ?
                  WHERE TITLE = ?
                     AND START_DATE = ?;
            """,
            (
               update.end_date,
               update.title,
               update.start_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def edit_update_record( cls, conn: Types.Connection, update: UpdateEditInput ) -> bool:
      cur = conn.cursor()

      try:
         cur.execute(
            """  UPDATE ZooUpdate
                  SET DESCRIPTION = ?,
                      UPDATE_TYPE = ?,
                      END_DATE = ?
                  WHERE TITLE = ?
                     AND START_DATE = ?;
            """,
            (
               update.description,
               update.update_type,
               update.end_date,
               update.title,
               update.start_date,
            ) )

         conn.commit()
         return cur.rowcount > 0

      finally:
         cur.close()


   @classmethod
   def fetch_updates(
         cls,
         conn: Types.Connection,
         as_of_date: Types.DateKey ) -> list[ Update ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     TITLE,
                     DESCRIPTION,
                     UPDATE_TYPE,
                     START_DATE,
                     END_DATE
                  FROM ZooUpdate
                  WHERE END_DATE IS NULL
                     OR END_DATE >= ?
                  ORDER BY START_DATE DESC, TITLE ASC;
            """,
            ( as_of_date, ) )

         return UpdateMapper.map_records( data.fetchall() )

      finally:
         cur.close()
