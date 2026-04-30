def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS WildEncounter;' )
   cursor.execute( ''' CREATE TABLE WildEncounter
                     (  NAME           TEXT  NOT NULL,
                        MEETING_SPOT   TEXT  NOT NULL,
                        LINK           TEXT  NOT NULL,           
                        FOREIGN KEY (MEETING_SPOT) REFERENCES WildEncounterMeetingSpot(NAME),
                        PRIMARY KEY (NAME) ); ''' )

wild_encounters = [
   (
      '''African Rainforest''',                                      # Name
      '''Wild Encounter - Africa Meeting Spot''',                    # Meeting spot
      '''https://www.torontozoo.com/tickets/weafricarainforest'''
   ),
   (
      '''Ballin' with the Armadillos''',                             # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',            # Meeting spot
      '''https://www.torontozoo.com/tickets/wearmadillo'''
   ),
   (
      '''Burrows & Caves''',                                         # Name
      '''Wild Encounter - Africa Meeting Spot''',                    # Meeting spot
      '''https://www.torontozoo.com/tickets/weburrows'''
   ),
   (
      '''Highland Cattle''',                                         # Name
      '''Wild Encounter - Eurasia Zoomobile Station Meeting Spot''', # Meeting spot
      '''https://www.torontozoo.com/tickets/wecows'''
   ),
   (
      '''From Howls to Honks''',                                     # Name
      '''Wild Encounter - Mayan Temple Meeting Spot''',              # Meeting spot
      '''https://www.torontozoo.com/tickets/wearctic'''
   ),
   (
      '''Kangaroo''',                                                # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wekangaroo'''
   ),
   (
      '''Scales & Tales of Americas''',                              # Name
      '''Wild Encounter - First Nations Art Garden Meeting Spot''',  # Meeting spot
      '''https://www.torontozoo.com/tickets/weamerica'''
   ),
   (
      '''Sunrise in Sumatra''',                                      # Name
      '''Wild Encounter - Zoo Front Entrance Gates Meeting Spot''',  # Meeting spot
      '''https://www.torontozoo.com/tickets/wesumatra'''
   ),
   (
      '''Animal Ambassadors: Keeper's Choice''',                     # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',            # Meeting spot
      '''https://www.torontozoo.com/tickets/weoutreach'''
   ),
   (
      '''Guardians of Snow Leopards''',                              # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wesnowleopard'''
   ),
   (
      '''Guardians of White Rhinos''',                               # Name
      '''Wild Encounter - Penguin Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wewhiterhino'''
   ),
   (
      '''The Tiny Tour''',                                           # Name
      '''Wild Encounter - Discovery Zone Meeting Spot''',            # Meeting spot
      '''https://www.torontozoo.com/tickets/wetiny'''
   ),
   (
      '''Capybara''',                                                # Name
      '''Wild Encounter - Mayan Temple Meeting Spot''',              # Meeting spot
      '''https://www.torontozoo.com/tickets/wecapybara'''
   ),
   (
      '''Guardians of Gorillas''',                                   # Name
      '''Wild Encounter - Penguin Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wegorilla'''
   ),
   (
      '''Great Barrier Reef''',                                      # Name
      '''Wild Encounter - Eurasia Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wegbr'''
   ),
   (
      '''Mischevious Meerkats''',                                    # Name
      '''Wild Encounter - Africa Meeting Spot''',                    # Meeting spot
      '''https://www.torontozoo.com/tickets/wemeerkats'''
   ),
   (
      '''Savanna Safari''',                                          # Name
      '''Wild Encounter - Penguin Meeting Spot''',                   # Meeting spot
      '''https://www.torontozoo.com/tickets/wesavannasafarI'''
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO WildEncounter (
                              NAME,
                              MEETING_SPOT,
                              LINK
                           ) 
                           VALUES (?, ?, ?) ''', wild_encounters )
