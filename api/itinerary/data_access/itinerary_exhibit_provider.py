from __future__ import annotations

from ...types import Connection, Cursor


class ItineraryExhibitProvider():
   @classmethod
   def fetch_itinerary_exhibits( cls, conn: Connection ) -> list[ str ]:
      cur = conn.cursor()

      rows = cur.execute(
         """   SELECT EXHIBIT
               FROM ItineraryExhibit;
         """ ).fetchall()

      cur.close()

      return [ row[ 'EXHIBIT' ] for row in rows ]


   @classmethod
   def save_itinerary_exhibits(
         cls,
         cur: Cursor,
         exhibits: list[ str ] ) -> None:
      for exhibit in exhibits:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryExhibit ( EXHIBIT )
                  VALUES ( ? );
            """,
            ( exhibit, ) )
