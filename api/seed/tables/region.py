from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Region;' )
   cursor.execute( ''' CREATE TABLE Region
                     (  NAME  VARCHAR(64) NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

regions = [
   (
      'Australasia',
   ),
   (
      'Eurasia Wilds',
   ),
   (
      'Tundra Trek',
   ),
   (
      'Americas',
   ),
   (
      'Canadian Domain',
   ),
   (
      'Africa',
   ),
   (
      'Indo-Malaya',
   ),
   (
      'Discovery Zone',
   ),
   (
      'Front Courtyard',
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Region (
                              NAME
                           ) 
                           VALUES (?) ''', regions )
