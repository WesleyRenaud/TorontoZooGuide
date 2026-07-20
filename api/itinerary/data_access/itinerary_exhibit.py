from __future__ import annotations

from ...types import Connection, Cursor


def fetch_itinerary_exhibits( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT EXHIBIT
            FROM ItineraryExhibit;
      """ ).fetchall()

   cur.close()

   return [ row[ 'EXHIBIT' ] for row in rows ]


def save_itinerary_exhibits(
      cur: Cursor,
      exhibits: list[ str ] ) -> None:
   for exhibit in exhibits:
      cur.execute(
         """   INSERT OR IGNORE INTO ItineraryExhibit ( EXHIBIT )
               VALUES ( ? );
         """,
         ( exhibit, ) )
