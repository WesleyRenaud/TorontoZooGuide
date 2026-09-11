from __future__ import annotations

import sqlite3

from ..itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from ..types import Types


class UserItineraryConfigCleaner():
   @classmethod
   def clear( cls, cursor: Types.Cursor ) -> None:
      ItineraryStatusProvider.clear_itinerary_status_suppressions( cursor )


   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         suppressed_before = ItineraryStatusProvider.fetch_suppressed_status_values( conn )
         cls.clear( cursor )
         conn.commit()
      finally:
         cursor.close()
         conn.close()

      if suppressed_before:
         print(
            "Cleared Don't show this again for: "
            + ', '.join( suppressed_before )
            + '.' )
      else:
         print( "No Don't show this again suppressions were enabled." )

      print( 'User itinerary config cleared successfully.' )


if __name__ == '__main__':
   UserItineraryConfigCleaner.main()
