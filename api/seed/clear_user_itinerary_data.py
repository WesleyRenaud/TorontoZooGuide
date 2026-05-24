from __future__ import annotations

import sqlite3

from .user_itinerary_data import clear_user_itinerary_data


def main( db_path: str = 'animals.db' ) -> None:
   conn = sqlite3.connect( db_path )
   cursor = conn.cursor()

   try:
      clear_user_itinerary_data( cursor )
      conn.commit()
   finally:
      cursor.close()
      conn.close()

   print( 'User itinerary data cleared successfully.' )


if __name__ == '__main__':
   main()
