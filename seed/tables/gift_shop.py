def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS GiftShop;' )
   cursor.execute( ''' CREATE TABLE GiftShop
                     (  NAME              VARCHAR(64) NOT NULL,
                        LOCATION          VARCHAR(64) NOT NULL,
                        DESCRIPTION       TEXT        NOT NULL,
                        X_COORD           FLOAT       NOT NULL,
                        Y_COORD           FLOAT       NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

gift_shops = [
   (
      'Zootique',
      'Learning & Engagement Centre',
      '''Our largest main boutique with the widest variety of souvenirs, toys, plush, apparel, books, jewelry, and more! Something
         for everyone, from every region of the Zoo.'''.replace( '\n', ' ' ),
      62.365,  # X coordinate on map
      73.1     # Y coordinate on map
   ),
   (
      'Courtyard Kiosk',
      'Front Courtyard',
      '''This green pod is a quick stop shop in the main front courtyard for all your Zoo necessities! *
         Located beside our Conservation Carousel.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      57.492,  # X coordinate on map
      78.41    # Y coordinate on map
   ),
   (
      'Eurasia Wilds Outpost',
      'Eurasia Wilds',
      '''Located by our endangered Amur Tiger exhibit, this indoor shop offers a variety of tiger themed souvenirs and gifts, as
         well as your other favourite Eurasian species!'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      78.41,   # X coordinate on map
      71.053   # Y coordinate on map
   ),
   (
      'Savanna Shop',
      'Africa Savanna',
      '''An indoor gift shop located by the Africa Zoomobile station. Souvenirs, toys, plush, apparel, and exclusive African gifts
         to remember some of your favourite species found in the African Savanna.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      56.47,   # X coordinate on map
      37.199   # Y coordinate on map
   ),
   (
      'Twiga Market',
      'Africa Savanna',
      '''A breezy outdoor market located directly in front of our Giraffe exhibit. Specializing in Giraffe, Hippo, and Gorilla
         themed souvenirs and gifts.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      41.501,  # X coordinate on map
      69.603   # Y coordinate on map
   ),
   (
      'Discovery Zone',
      'Next to Splash Island',
      '''An aquatic-themed outdoor kiosk that has you covered for summer. Towels, apparel, sunscreen, toys, and more! Located by the
         entrance of Splash Island.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      67.176,  # X coordinate on map
      77.413   # Y coordinate on map
   ),
   (
      'Tundra Trading Post',
      'Tundra Trek',
      '''This arctic-themed outdoor kiosk has you covered for summer adventures! Find apparel, sunscreen, toys, and other essentials
         perfect for your day at the Zoo. Conveniently located beside BeaverTails and the polar bear habitat near the Tundra Trek
         Loop.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      74.05,   # X coordinate on map
      56.912   # Y coordinate on map
   ),
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO GiftShop (
                              NAME,
                              LOCATION,
                              DESCRIPTION,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', gift_shops )
