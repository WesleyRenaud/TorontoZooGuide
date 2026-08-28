from __future__ import annotations

import sqlite3

from ..itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from ..types import Cursor


class UserItineraryConfigCleaner():
   @classmethod
   def clear( cls, cursor: Cursor ) -> None:
      ItineraryStatusProvider.clear_itinerary_status_suppressions( cursor )


   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         cls.clear( cursor )
         conn.commit()
      finally:
         cursor.close()
         conn.close()

      print( 'User itinerary config cleared successfully.' )


if __name__ == '__main__':
   UserItineraryConfigCleaner.main()
