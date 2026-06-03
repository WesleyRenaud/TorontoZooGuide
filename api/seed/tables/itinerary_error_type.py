from __future__ import annotations

from ...types import Cursor


def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS ItineraryErrorType;' )
   cursor.execute( ''' CREATE TABLE ItineraryErrorType
                     (  ERROR_TYPE         TEXT NOT NULL PRIMARY KEY,
                        IS_SUPPRESSABLE    BOOL NOT NULL ); ''' )


itinerary_error_types = [
   (
      'arrivalDepartureTooClose',                 # Error type
      1,                                          # Is suppressable
   ),
   (
      'itemNotOnItinerary',                       # Error type
      1,                                          # Is suppressable
   ),
   (
      'guardiansTalkWillUnscheduleItems',         # Error type
      0,                                          # Is suppressable
   ),
   (
      'wildEncounterWillUnscheduleItems',         # Error type
      0,                                          # Is suppressable
   ),
]


def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO ItineraryErrorType (
                              ERROR_TYPE,
                              IS_SUPPRESSABLE
                           )
                           VALUES (?, ?) ''', itinerary_error_types )
