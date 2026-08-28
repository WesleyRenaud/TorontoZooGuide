from __future__ import annotations

from ...types import Types


class ItineraryExhibitProvider():
   @classmethod
   def fetch_itinerary_exhibits( cls, conn: Types.Connection ) -> list[ str ]:
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
         cur: Types.Cursor,
         exhibits: list[ str ] ) -> None:
      for exhibit in exhibits:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryExhibit ( EXHIBIT )
                  VALUES ( ? );
            """,
            ( exhibit, ) )
