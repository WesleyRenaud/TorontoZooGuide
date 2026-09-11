from __future__ import annotations

import sqlite3
from datetime import date
from datetime import timedelta

from ..types import Types


class UserItineraryDateBackdater():
   @classmethod
   def backdate_to_yesterday( cls, cursor: Types.Cursor ) -> str | None:
      yesterday = ( date.today() - timedelta( days=1 ) ).isoformat()
      cursor.execute(
         """   UPDATE ItineraryDate
                  SET ITINERARY_DATE = ?
         """,
         ( yesterday, ) )

      if cursor.rowcount < 1:
         return None

      return yesterday


   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         backdated_to = cls.backdate_to_yesterday( cursor )
         conn.commit()
      finally:
         cursor.close()
         conn.close()

      if backdated_to is None:
         print( 'No itinerary date row to backdate. Save an itinerary first.' )
         return

      print( f'Itinerary date backdated to { backdated_to }.' )


if __name__ == '__main__':
   UserItineraryDateBackdater.main()
