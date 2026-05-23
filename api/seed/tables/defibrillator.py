from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Defibrillator;' )
   cursor.execute( ''' CREATE TABLE Defibrillator
                     (  X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL,
                        PRIMARY KEY (X_COORD, Y_COORD) ); ''' )


defibrillators = [
   (
      57.018,  # X coordinate on map
      37.556   # Y coordinate on map
   ),
   (
      50.476,  # X coordinate on map
      56.564   # Y coordinate on map
   ),
   (
      53.700,  # X coordinate on map
      59.124   # Y coordinate on map
   ),
   (
      37.674,  # X coordinate on map
      52.049   # Y coordinate on map
   ),
   (
      43.241,  # X coordinate on map
      64.403   # Y coordinate on map
   ),
   (
      47.751,  # X coordinate on map
      73.976   # Y coordinate on map
   ),
   (
      57.270,  # X coordinate on map
      87.345   # Y coordinate on map
   ),
   (
      62.760,  # X coordinate on map
      71.970   # Y coordinate on map
   ),
   (
      69.496,  # X coordinate on map
      49.609   # Y coordinate on map
   ),
   (
      71.613,  # X coordinate on map
      57.478   # Y coordinate on map
   ),
   (
      72.803,  # X coordinate on map
      69.290   # Y coordinate on map
   ),
   (
      85.803,  # X coordinate on map
      78.971   # Y coordinate on map
   ),
]


def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Defibrillator (
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?) ''', defibrillators )
