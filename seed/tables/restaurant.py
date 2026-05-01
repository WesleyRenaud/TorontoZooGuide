def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Restaurant;' )
   cursor.execute( ''' CREATE TABLE Restaurant
                     (  NAME              VARCHAR(64) NOT NULL,
                        LOCATION          VARCHAR(64),
                        SUB_LOCATION      VARCHAR(64),
                        DESCRIPTION       TEXT        NOT NULL,
                        MENU_LINK         TEXT,
                        X_COORD           FLOAT       NOT NULL,
                        Y_COORD           FLOAT       NOT NULL,
                        FOREIGN KEY (LOCATION) REFERENCES Region(Name),
                        PRIMARY KEY (NAME) ); ''' )

restaurants = [
   (
      'Peacock Café',                                                                                    # Name
      'Front Courtyard',                                                                                 # Location
      None,                                                                                              # Sub-location
      '''Enjoy Tim Hortons fresh coffee, hot and cold beverages, breakfast sandwiches, pastries and more.''',
      '''https://www.torontozoo.com/!/pdfs/food/peacockcafemenu.pdf''',                                  # Menu link
      57.079,                                                                                            # X coordinate on map
      83.618                                                                                             # Y coordinate on map
   ),
   (
      'Africa Restaurant',                                                                               # Name
      'Africa',                                                                                          # Location
      None,                                                                                              # Sub-location
      '''Enjoy a variety of cuisine including Pizza Pizza, Smokes Poutinerie (seasonal), and our very own Zoo Grill. *Fully Licensed.
      '''.replace( '\n', ' ' ),
      '''https://www.torontozoo.com/!/pdfs/food/Africa%20Menu%202025.pdf?''',                            # Menu link
      53.383,                                                                                            # X coordinate on map
      57.213                                                                                             # Y coordinate on map
   ),
   (
      'BeaverTails Trailer',                                                                             # Name
      'Front Courtyard',                                                                                 # Location
      None,                                                                                              # Sub-location
      '''Iconic hand-stretched pastries, creating delicious memories since 1978.''',
      '''https://www.torontozoo.com/!/pdfs/food/BeavertailsMenu.pdf''',                                  # Menu link
      60.179,                                                                                            # X coordinate on map
      74.959                                                                                             # Y coordinate on map
   ),
   (
      'Americas Pretzel Bar',                                                                            # Name
      'Americas',                                                                                        # Location
      None,                                                                                              # Sub-location
      '''Serving warm Jumbo pretzels, assorted Craft beers, wine, seltzers, soft drinks, ice cream, and snacks''',
      None,                                                                                              # Menu link
      69.49,                                                                                             # X coordinate on map
      56.634                                                                                             # Y coordinate on map
   ),
   (
      'Caribou Café',                                                                                    # Name
      'Tundra Trek',                                                                                     # Location
      None,                                                                                              # Sub-location
      '''Located next to the arctic wolves, enjoy a variety of options including Zoo Grill, and Pizza Pizza! *Fully Licensed.''',
      '''https://www.torontozoo.com/!/pdfs/food/Caribou%20Cafe%20Menu%202025.pdf?''',                    # Menu link
      71.91,                                                                                             # X coordinate on map
      56.193                                                                                             # Y coordinate on map
   ),
   (
      'BeaverTails Lodge',                                                                               # Name
      'Tundra Trek',                                                                                     # Location
      None,                                                                                              # Sub-location
      '''Delicious whole-wheat deep fried pastry with a variety of toppings plus cold drinks.''',
      'https://www.torontozoo.com/!/pdfs/food/BeavertailsMenu.pdf',                                      # Menu link
      78.454,                                                                                            # X coordinate on map
      56.532                                                                                             # Y coordinate on map
   ),
   (
      'Thorntree Café',                                                                                  # Name
      'Africa',                                                                                          # Location
      None,                                                                                              # Sub-location
      '''Come hang out for bubble tea and smoothies at Palgong Tea near the Masai giraffes!''',
      '''https://www.torontozoo.com/!/pdfs/food/Palgong-Menu.pdf''',                                     # Menu link
      41.323,                                                                                            # X coordinate on map
      67.206                                                                                             # Y coordinate on map
   ),
   (
      'Eurasia Pizza Pizza',                                                                             # Name
      'Eurasia Wilds',                                                                                   # Location
      None,                                                                                              # Sub-location
      '''Enjoy a hot slice of Pizza Pizza or order a whole pizza for the whole family!''',
      'https://www.torontozoo.com/!/pdfs/food/Eurasia%20pizza%20pizza%20menu%202025.pdf',                # Menu link
      78.302,                                                                                            # X coordinate on map
      72.147                                                                                             # Y coordinate on map
   ),
   (
      'Souvlaki Bros',                                                                                   # Name
      'Africa',                                                                                          # Location
      'Africa Restaurant',                                                                               # Sub-location
      '''Enjoy Chicken Souvlaki, Falafel, Greek Salad, Wraps and Churros!''',
      'https://www.torontozoo.com/!/pdfs/food/Souvlaki%20Bros%20Menu.pdf',                               # Menu link
      53.202,                                                                                            # X coordinate on map
      58.399                                                                                             # Y coordinate on map
   ),
   (
      'Caribou Café Palgong',                                                                            # Name
      'Tundra Trek',                                                                                     # Location
      None,                                                                                              # Sub-location
      '''Located next to the arctic wolves, outside of Caribou Café!''',
      'https://www.torontozoo.com/!/pdfs/food/Palgong-Menu.pdf',                                         # Menu link
      71.344,                                                                                            # X coordinate on map
      56.601                                                                                             # Y coordinate on map
   ),
   (
      'Polar Patio',                                                                                     # Name
      'Tundra Trek',                                                                                     # Location
      None,                                                                                              # Sub-location
      '''Join us at our fully licensed Polar Patio next to the Arctic wolves, enjoy beer, wine, ciders & seltzers or try our wings,
         nachos, poutine and tenders!'''.replace( '\n', ' ' ),
      'https://www.torontozoo.com/!/pdfs/food/Polar%20Patio%20Menu%202024.pdf',                          # Menu link
      72.858,                                                                                            # X coordinate on map
      56.303                                                                                             # Y coordinate on map
   ),
   (
      'Savanna Snack Bar',                                                                               # Name
      'Africa Savanna',                                                                                  # Location
      None,                                                                                              # Sub-location
      '''Snacks, Beverages, Ice cream, Beer, Wine, and Pizza Pizza!''',
      'https://www.torontozoo.com/!/pdfs/food/Toronto%20Zoo%20Savana%20Hut%20Menu%20Spring%202025.pdf',  # Menu link
      56.812,                                                                                            # X coordinate on map
      38.413                                                                                             # Y coordinate on map
   ),
   (
      'Simba Safari Lodge',                                                                              # Name
      'Africa Savanna',                                                                                  # Location
      None,                                                                                              # Sub-location
      '''Located overlooking the white rhinos, enjoy a variety of drinks, snacks, burgers, hot dogs, salads, poutine and chicken.
         *Fully Licensed.'''.replace( '\n', ' ' ),
      'https://www.torontozoo.com/!/pdfs/food/Simba%20Menu%202025.pdf?',                                 # Menu link
      37.786,                                                                                            # X coordinate on map
      50.566                                                                                             # Y coordinate on map
   ),
   (
      'Smokes Poutinerie Trailer',                                                                       # Name
      'Front Courtyard',                                                                                 # Location
      None,                                                                                              # Sub-location
      '''Enjoy a variety of poutine creations.''',
      'https://www.torontozoo.com/!/pdfs/food/Smokes-Front-Courtyard-Menu.pdf',                          # Menu link
      60.694,                                                                                            # X coordinate on map
      74.56                                                                                              # Y coordinate on map
   ),
   (
      'Tim Hortons Express',                                                                             # Name
      'Tundra Trek',                                                                                     # Location
      None,                                                                                              # Sub-location
      '''Grab a quick beverage or snack including coffee, tea, iced caps, timbits, and frozen lemonade.''',
      'https://www.torontozoo.com/!/pdfs/food/Express%20Menu%202025.pdf',                                # Menu link
      79.073,                                                                                            # X coordinate on map
      56.207                                                                                             # Y coordinate on map
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Restaurant (
                              NAME,
                              LOCATION,
                              SUB_LOCATION,
                              DESCRIPTION,
                              MENU_LINK,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?, ?, ?) ''', restaurants )
