def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Attraction;' )
   cursor.execute( ''' CREATE TABLE Attraction
                     (  NAME                 VARCHAR(64) NOT NULL,
                        FREE_WITH_ADMISSION  BOOL        NOT NULL,
                        DESCRIPTION          TEXT        NOT NULL,
                        INFO_LINK            TEXT        NOT NULL,
                        HYPERLINK_TEXT       TEXT        NOT NULL,
                        X_COORD              FLOAT       NOT NULL,
                        Y_COORD              FLOAT       NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

attractions = [
   (
      'Zoomobile',
      0,                                                                      # Free with admission
      '''All Aboard for a Wild Ride! Climb aboard the Zoomobile for a fun ride through your Toronto Zoo!''',
      '''https://www.torontozoo.com/tickets/zoomobile''',                     # Info link
      '''PRICING & DETAILS''',                                                # Hyperlink text
      56.246,                                                                 # X coordinate on map
      81.096                                                                  # Y coordinate on map
   ),
   (
      'Conservation Carousel',
      0,                                                                      # Free with admission
      '''Carousels are timeless and fun for all ages! Hop on and choose a unique animal seat.''',
      '''https://www.torontozoo.com/tickets/carousel''',                      # Info link
      '''TICKETS & DETAILS''',                                                # Hyperlink text
      58.475,                                                                 # X coordinate on map
      75.904                                                                  # Y coordinate on map
   ),
   (
      'Greenhouse',
      1,                                                                      # Free with admission
      '''Take a self-guided tour of our Greenhouse, full of plants from around the world.''',
      '''https://www.torontozoo.com/tz/greenhouse''',                         # Info link
      '''LEARN MORE''',                                                       # Hyperlink text
      82.835,                                                                 # X coordinate on map
      54.277                                                                  # Y coordinate on map
   ),
   (
      'Wildlife Health & Science Centre',
      1,                                                                      # Free with admission
      '''Step inside one of the most advanced wildlife health and science facilities in Canada.''',
      '''https://www.torontozoo.com/whsc''',                                  # Info link
      '''LEARN MORE''',                                                       # Hyperlink text
      84.459,                                                                 # X coordinate on map
      50.743                                                                  # Y coordinate on map
   ),
   (
      'Kangaroo Walk-Thru',
      1,                                                                      # Free with admission
      '''Walk among the kangaroos!''',                                        
      '''https://www.torontozoo.com/tz/kangaroo''',                           # Info link
      '''LEARN MORE''',                                                       # Hyperlink text
      74.985,                                                                 # X coordinate on map
      70.331                                                                  # Y coordinate on map
   ),
   (
      'Virtual Reality (VR) Theatre!',
      0,                                                                      # Free with admission
      '''An interactive adventure! This fully immersive technology will transport you from Scarborough to various locations around
         the world. Three Shows to Choose From!'''.replace( '\n', ' ' ),
      '''https://www.torontozoo.com/tickets/wildexplorer''',                  # Info link
      '''PRICING & DETAILS''',                                                # Hyperlink text
      71.786,                                                                 # X coordinate on map
      59.947                                                                  # Y coordinate on map
   ),
   (
      'TundraAir Ride',
      0,                                                                      # Free with admission
      '''Soar through the air at speeds of 48km/hr over the Tundra Trek on the TundraAir Ride.''',
      '''https://www.torontozoo.com/tz/tundraair''',                          # Info link
      '''PRICING & DETAILS''',                                                # Hyperlink text
      75.152,                                                                 # X coordinate on map
      60.212                                                                  # Y coordinate on map
   ),
   (
      'Gorilla Climb Ropes Course',
      0,                                                                      # Free with admission
      '''Hang out like the gorilla troop do! Swing, crawl and balance on 26 elements almost 33 feet high!''',
      '''https://www.torontozoo.com/tz/gorillaclimb''',                       # Info link
      '''PRICING & DETAILS''',                                                # Hyperlink text
      50.023,                                                                 # X coordinate on map
      58.884                                                                  # Y coordinate on map
   ),
   (
      'Splash Island',
      1,                                                                      # Free with admission
      '''Cool off at our 2-acre splash pad, filled with water-spouting animals.''',
      '''https://www.torontozoo.com/tz/splash''',                             # Info link
      '''LEARN MORE''',                                                       # Hyperlink text
      67.797,                                                                 # X coordinate on map
      72.648                                                                  # Y coordinate on map
   ),
   (
      'Face Painting, Caricatures and Henna!',
      0,                                                                      # Free with admission
      '''Transform into your favorite animal with our talented face painters and caricature artists!''',
      '''https://www.torontozoo.com/tz/facepainting''',                       # Info link
      '''LEARN MORE''',                                                       # Hyperlink text
      73.669,                                                                 # X coordinate on map
      59.054                                                                  # Y coordinate on map
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Attraction (
                              NAME,
                              FREE_WITH_ADMISSION,
                              DESCRIPTION,
                              INFO_LINK,
                              HYPERLINK_TEXT,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?, ?, ?) ''', attractions )
