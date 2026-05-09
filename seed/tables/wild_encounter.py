def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS WildEncounter;' )
   cursor.execute( ''' CREATE TABLE WildEncounter
                     (  NAME           TEXT  NOT NULL,
                        MEETING_SPOT   TEXT  NOT NULL,
                        LINK           TEXT  NOT NULL,
                        DURATION INTEGER NOT NULL,
                        FOREIGN KEY (MEETING_SPOT) REFERENCES WildEncounterMeetingSpot(NAME),
                        PRIMARY KEY (NAME) ); ''' )

wild_encounters = [
   (
      '''African Rainforest''',                                        # Name
      '''Wild Encounter - Africa Meeting Spot''',                      # Meeting spot
      '''https://www.torontozoo.com/tickets/weafricarainforest''',     # Link
      45                                                               # Duration in minutes
   ),
   (
      '''Ballin' with the Armadillos''',                               # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',              # Meeting spot
      '''https://www.torontozoo.com/tickets/wearmadillo''',            # Link
      30                                                               # Duration in minutes
   ),
   (
      '''Burrows & Caves''',                                           # Name
      '''Wild Encounter - Africa Meeting Spot''',                      # Meeting spot
      '''https://www.torontozoo.com/tickets/weburrows''',              # Link
      60                                                               # Duration in minutes
   ),
   (
      '''Highland Cattle''',                                           # Name
      '''Wild Encounter - Eurasia Zoomobile Station Meeting Spot''',   # Meeting spot
      '''https://www.torontozoo.com/tickets/wecows''',                 # Link
      30                                                               # Duration in minutes
   ),
   (
      '''From Howls to Honks''',                                       # Name
      '''Wild Encounter - Mayan Temple Meeting Spot''',                # Meeting spot
      '''https://www.torontozoo.com/tickets/wearctic''',               # Link
      30                                                               # Duration in minutes
   ),
   (
      '''Kangaroo''',                                                  # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wekangaroo''',             # Link
      45                                                               # Duration in minutes
   ),
   (
      '''Scales & Tales of Americas''',                                # Name
      '''Wild Encounter - First Nations Art Garden Meeting Spot''',    # Meeting spot
      '''https://www.torontozoo.com/tickets/weamerica''',              # Link
      45                                                               # Duration in minutes
   ),
   (
      '''Sunrise in Sumatra''',                                        # Name
      '''Wild Encounter - Zoo Front Entrance Gates Meeting Spot''',    # Meeting spot
      '''https://www.torontozoo.com/tickets/wesumatra''',              # Link
      60                                                               # Duration in minutes
   ),
   (
      '''Animal Ambassadors: Keeper's Choice''',                       # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',              # Meeting spot
      '''https://www.torontozoo.com/tickets/weoutreach''',             # Link
                                                                       # TO-DO: Update/verify duration when this encounter returns
      30                                                               # Duration in minutes
   ),
   (
      '''Guardians of Snow Leopards''',                                # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wesnowleopard''',          # Link
      40                                                               # Duration in minutes
   ),
   (
      '''Guardians of White Rhinos''',                                 # Name
      '''Wild Encounter - Penguin Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wewhiterhino''',           # Link
      45                                                               # Duration in minutes
   ),
   (
      '''The Tiny Tour''',                                             # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',              # Meeting spot
      '''https://www.torontozoo.com/tickets/wetiny''',                 # Link
      30                                                               # Duration in minutes
   ),
   (
      '''Capybara''',                                                  # Name
      '''Wild Encounter - Mayan Temple Meeting Spot''',                # Meeting spot
      '''https://www.torontozoo.com/tickets/wecapybara''',             # Link
      30                                                               # Duration in minutes
   ),
   (
      '''Guardians of Gorillas''',                                     # Name
      '''Wild Encounter - Penguin Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wegorilla''',              # Link
      45                                                               # Duration in minutes
   ),
   (
      '''Great Barrier Reef''',                                        # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wegbr''',                  # Link
      20                                                               # Duration in minutes
   ),
   (
      '''Mischevious Meerkats''',                                      # Name
      '''Wild Encounter - Africa Meeting Spot''',                      # Meeting spot
      '''https://www.torontozoo.com/tickets/wemeerkats''',             # Link
      20                                                               # Duration in minutes
   ),
   (
      '''Savanna Safari''',                                            # Name
      '''Wild Encounter - Penguin Meeting Spot''',                     # Meeting spot
      '''https://www.torontozoo.com/tickets/wesavannasafarI''',        # Link
      60                                                               # Duration in minutes
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO WildEncounter (
                              NAME,
                              MEETING_SPOT,
                              LINK,
                              DURATION
                           ) 
                           VALUES (?, ?, ?, ?) ''', wild_encounters )
