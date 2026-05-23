from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS GuestService;' )
   cursor.execute( ''' CREATE TABLE GuestService
                     (  SERVICE_TYPE  TEXT  NOT NULL,
                        X_COORD       FLOAT NOT NULL,
                        Y_COORD       FLOAT NOT NULL,
                        PRIMARY KEY (SERVICE_TYPE, X_COORD, Y_COORD) ); ''' )


guest_services = [
   (
      '''First Aid & Family Center''',    # Service type
      50.783,                             # X coordinate on map
      55.561                              # Y coordinate on map
   ),
   (
      '''Information''',                  # Service type
      72.294,                             # X coordinate on map
      57.641                              # Y coordinate on map
   ),
   (
      '''Information''',                  # Service type
      50.235,                             # X coordinate on map
      61.710                              # Y coordinate on map
   ),
   (
      '''Information''',                  # Service type
      58.730,                             # X coordinate on map
      78.782                              # Y coordinate on map
   ),
   (
      '''Rentals & Accessibility''',      # Service type
      56.587,                             # X coordinate on map
      79.762                              # Y coordinate on map
   ),
   (
      '''Wheelchairs''',                  # Service type
      57.193,                             # X coordinate on map
      79.673                              # Y coordinate on map
   ),
]


def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO GuestService (
                              SERVICE_TYPE,
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?, ?) ''', guest_services )
