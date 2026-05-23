from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Restroom;' )
   cursor.execute( ''' CREATE TABLE Restroom
                     (  TITLE    VARCHAR(64) NOT NULL,
                        X_COORD  FLOAT       NOT NULL,
                        Y_COORD  FLOAT       NOT NULL,
                        PRIMARY KEY (TITLE) ); ''' )

restrooms = [
   (
      'Entrance Restroom',
      57.418,  # X coordinate on map
      84.787   # Y coordinate on map
   ),
   (
      'Africa Restaurant Restroom',
      52.751,  # X coordinate on map
      59.47    # Y coordinate on map
   ),
   (
      'Simba Safari Lodge Restroom',
      38.27,   # X coordinate on map
      51.794   # Y coordinate on map
   ),
   (
      'Canadian Domain Zoomobile Stop Restroom',
      36.066,  # X coordinate on map
      25.484   # Y coordinate on map
   ),
   (
      'Canadian Domain Restroom',
      17.865,  # X coordinate on map
      13.699   # Y coordinate on map
   ),
   (
      'Caribou Café Restroom',
      72.594,  # X coordinate on map
      54.25    # Y coordinate on map
   ),
   (
      'Eurasia Restroom',
      77.472,  # X coordinate on map
      69.345   # Y coordinate on map
   ),
   (
      'Splash Island Restroom',
      67.201,  # X coordinate on map
      75.854   # Y coordinate on map
   ),
   (
      'Zootique Restroom',
      62.467,  # X coordinate on map
      72.934   # Y coordinate on map
   ),
   (
      'African Rainforest Restroom',
      46.313,  # X coordinate on map
      68.117   # Y coordinate on map
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Restroom (
                              TITLE,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?) ''', restrooms )
