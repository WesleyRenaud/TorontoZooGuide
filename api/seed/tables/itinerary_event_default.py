from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS ItineraryEventDefault;' )
   cursor.execute( ''' CREATE TABLE ItineraryEventDefault
                     (  EVENT_TYPE                            TEXT        NOT NULL PRIMARY KEY,
                        DEFAULT_ITINERARY_DURATION_MINUTES    INTEGER     NOT NULL ); ''' )

itinerary_event_defaults = [
   (
      'breakfast',                                # Event type
      20,                                         # Default itinerary duration (minutes)
   ),
   (
      'lunch',                                    # Event type
      40,                                         # Default itinerary duration (minutes)
   ),
   (
      'dinner',                                   # Event type
      40,                                         # Default itinerary duration (minutes)
   ),
   (
      'snack',                                    # Event type
      15,                                         # Default itinerary duration (minutes)
   ),
   (
      'break',                                    # Event type
      15,                                         # Default itinerary duration (minutes)
   ),
   (
      'shopping',                                 # Event type
      30,                                         # Default itinerary duration (minutes)
   ),
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO ItineraryEventDefault (
                              EVENT_TYPE,
                              DEFAULT_ITINERARY_DURATION_MINUTES
                           )
                           VALUES (?, ?) ''', itinerary_event_defaults )
