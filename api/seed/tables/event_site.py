from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS EventSite;' )
   cursor.execute( ''' CREATE TABLE EventSite
                     (  NAME     TEXT  NOT NULL PRIMARY KEY,
                        X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL ); ''' )


event_sites = [
   (
      '''Special Events Center''',              # Event site name
      71.908,                                   # X coordinate on map
      79.867                                    # Y coordinate on map
   ),
   (
      '''Wildlife Marquee''',                   # Event site name
      71.024,                                   # X coordinate on map
      75.519                                    # Y coordinate on map
   ),
   (
      '''Conservation Clubhouse''',             # Event site name
      70.698,                                   # X coordinate on map
      81.363                                    # Y coordinate on map
   ),
   (
      '''Learning & Engagement Auditorium''',   # Event site name
      61.957,                                   # X coordinate on map
      71.829                                    # Y coordinate on map
   ),
   (
      '''Canopy Classroom''',                   # Event site name
      48.227,                                   # X coordinate on map
      76.278                                    # Y coordinate on map
   ),
   (
      '''Serengeti Bush Camp''',                # Event site name
      36.801,                                   # X coordinate on map
      53.564                                    # Y coordinate on map
   ),
]


def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO EventSite (
                              NAME,
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?, ?) ''', event_sites )
