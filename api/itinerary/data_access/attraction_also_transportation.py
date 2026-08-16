from __future__ import annotations

from ...types import Connection


def attraction_is_also_transportation(
      conn: Connection,
      attraction_name: str ) -> bool:
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT IS_ALSO_TRANSPORTATION
               FROM Attraction
               WHERE NAME = ?;
         """,
         ( attraction_name, ),
      ).fetchone()

      if row is None:
         return False

      return bool( row[ 'IS_ALSO_TRANSPORTATION' ] )

   finally:
      cur.close()


def fetch_also_transportation_attraction_names(
      conn: Connection ) -> set[ str ]:
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT NAME
               FROM Attraction
               WHERE IS_ALSO_TRANSPORTATION = 1;
         """
      ).fetchall()

      return { row[ 'NAME' ] for row in rows }

   finally:
      cur.close()
