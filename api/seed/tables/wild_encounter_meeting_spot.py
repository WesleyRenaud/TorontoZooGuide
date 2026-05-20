def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS WildEncounterMeetingSpot;' )
   cursor.execute( ''' CREATE TABLE WildEncounterMeetingSpot
                     (  NAME     TEXT  NOT NULL,
                        X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

wild_encounter_meeting_spots = [
   (
      '''Wild Encounter - Penguin Meeting Spot''',
      53.338,  # X coordinate on map
      47.237   # Y coordinate on map
   ),
   (
      '''Wild Encounter - Africa Meeting Spot''',
      40.044,  # X coordinate on map
      69       # Y coordinate on map
   ),
   (
      '''Wild Encounter - Discovery Zone Meeting Spot''',
      65.885,  # X coordinate on map
      77.803   # Y coordinate on map
   ),
   (
      '''Wild Encounter - Eurasia Meeting Spot''',
      77.23,   # X coordinate on map
      63.73    # Y coordinate on map
   ),
   (
      '''Wild Encounter - Mayan Temple Meeting Spot''',
      75.819,  # X coordinate on map
      42.75    # Y coordinate on map
   ),
   (
      '''Wild Encounter - Eurasia Zoomobile Station Meeting Spot''',
      75.943,  # X coordinate on map
      90.577   # Y coordinate on map
   ),
   (
      '''Wild Encounter - Zoo Front Entrance Gates Meeting Spot''',
      59.812,  # X coordinate on map
      85.689   # Y coordinate on map
   ),
   (
      '''Wild Encounter - First Nations Art Garden Meeting Spot''',
      70.329,  # X coordinate on map
      53.162   # Y coordinate on map
   ),
   (
      '''Wild Encounter - Canadian Domain Meeting Spot''',
      35.584,  # X coordinate on map
      20.070   # Y coordinate on map
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO WildEncounterMeetingSpot (
                              NAME,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?) ''', wild_encounter_meeting_spots )
