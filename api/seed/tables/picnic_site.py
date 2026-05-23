from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS PicnicSite;' )
   cursor.execute( ''' CREATE TABLE PicnicSite
                     (  X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL,
                        PRIMARY KEY (X_COORD, Y_COORD) ); ''' )


picnic_sites = [
   (
      36.200,  # X coordinate on map
      45.821   # Y coordinate on map
   ),
   (
      36.089,  # X coordinate on map
      23.430   # Y coordinate on map
   ),
   (
      35.597,  # X coordinate on map
      47.978   # Y coordinate on map
   ),
   (
      51.320,  # X coordinate on map
      61.897   # Y coordinate on map
   ),
]


def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO PicnicSite (
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?) ''', picnic_sites )
