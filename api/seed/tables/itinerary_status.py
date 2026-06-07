from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS ItineraryStatus;' )
   cursor.execute( ''' CREATE TABLE ItineraryStatus
                     (  STATUS             TEXT NOT NULL PRIMARY KEY,
                        IS_SUPPRESSABLE    BOOL NOT NULL ); ''' )

itinerary_statuses = [
   (
      'itineraryDateNotSet',                          # Status
      0,                                              # Is suppressable
   ),
   (
      'timeOutOfBounds',                              # Status
      0,                                              # Is suppressable
   ),
   (
      'timeOrderInvalid',                             # Status
      0,                                              # Is suppressable
   ),
   (
      'saveFailed',                                   # Status
      0,                                              # Is suppressable
   ),
   (
      'arrivalDepartureTooClose',                     # Status
      1,                                              # Is suppressable
   ),
   (
      'earlyAdmissionRequiresMembership',             # Status
      1,                                              # Is suppressable
   ),
   (
      'noAvailableSlot',                              # Status
      0,                                              # Is suppressable
   ),
   (
      'requestedTimeNotAvailable',                    # Status
      0,                                              # Is suppressable
   ),
   (
      'itemNotOnItinerary',                           # Status
      1,                                              # Is suppressable
   ),
   (
      'guardiansTalkWillUnscheduleItems',             # Status
      0,                                              # Is suppressable
   ),
   (
      'wildEncounterWillUnscheduleItems',             # Status
      0,                                              # Is suppressable
   ),
   (
      'guardiansTalkWildEncounterTimeConflict',       # Status
      0,                                              # Is suppressable
   ),
   (
      'wildEncounterTimeConflict',                    # Status
      0,                                              # Is suppressable
   ),
   (
      'bulkScheduleAnimalsNotEnoughTime',             # Status
      0,                                              # Is suppressable
   ),
   (
      'bulkScheduleAnimalsAlreadyScheduled',          # Status
      0,                                              # Is suppressable
   ),
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO ItineraryStatus (
                              STATUS,
                              IS_SUPPRESSABLE
                           )
                           VALUES (?, ?) ''', itinerary_statuses )
