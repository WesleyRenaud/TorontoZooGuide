from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS ZoomobileStation;' )
   cursor.execute( ''' CREATE TABLE ZoomobileStation
                     (  NAME              VARCHAR(64) NOT NULL,
                        ON_WINTER_ROUTE   BOOL        NOT NULL,
                        DESCRIPTION       TEXT        NOT NULL,
                        X_COORD           FLOAT       NOT NULL,
                        Y_COORD           FLOAT       NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

zoomobile_stations = [
   (
      'Main Zoomobile Station',
      1,       # On winter route
      '''This stop is right beside the entrance and exit to the zoo. Located next door is the Peacock Café. This is also the closest
         stop to Indo-Malaya where you can see Sumatran orangutans, white-handed gibbons, greater one-horned rhinos, clouded
         leopards, and so much more.'''.replace( '\n', ' ' ),
      56.992,  # X coordinate on map
      80.918   # Y coordinate on map
   ),
   (
      'Canadian Domain Zoomobile Station',
      0,       # On winter route
      '''This stop gives you direct access to the Canadian Domain, home to raccoons, bald eagles, wood bison, cougars, and grizzly
         bears. Please note that this station is located at the top of the domain hill, and if you wish to venture down to see the
         Canadian animals you will have to come back up the hill on foot.'''.replace( '\n', ' ' ),
      35.293,  # X coordinate on map
      26.083   # Y coordinate on map
   ),
   (
      'Africa Zoomobile Station',
      0,       # On winter route
      '''This stop drops you off at the back of the Africa Savanna section of the zoo home to hyenas, African penguins, lions,
         cheetahs, zebras, rhinos, hippos, giraffes, and more! If you move through the savanna you will reach the African Rainforest
         Pavilion which is home to Western lowland gorillas, pygmy hippos, ring-tailed lemurs, to name a few.'''.replace( '\n', ' ' ),
      56.186,  # X coordinate on map
      35.325   # Y coordinate on map
   ),
   (
      'Tundra Zoomobile Station',
      1,       # On winter route
      '''This stop drops you off just behind the Tundra Trek exhibit. The Tundra Trek is home to polar bears, arctic wolves, and
         caribou. During the warmer months, via the tundra trek you can also access the Mayan Temple Ruins, which is home to
         capybaras, flamingoes, and spider monkeys. Across from Tundra zoomobile station are the greenhouse and wildlife health
         center, which are available for guests to walk through, free with admission, year-round. This stop is also the closest
         access point to the Americas and Australasia pavilions.'''.replace( '\n', ' ' ),
      80.191,  # X coordinate on map
      56.422   # Y coordinate on map
   ),
   (
      'Eurasia Zoomobile Station',
      1,       # On winter route
      '''This station is located right in the middle of the Eurasia Wilds loop. In Eurasia you can find Amur tigers, snow leopards,
         red pandas, camels, highland cows, and more. Between this station and the tundra station you will also pass through the
         Eurasia Wilds drive-thru where you can get face-to-face with Asian wild horses, West Caucasian turs, and yaks.'''
         .replace( '\n', ' ' ),
      75.145,  # X coordinate on map
      88.373   # Y coordinate on map
   ),
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO ZoomobileStation (
                              NAME,
                              ON_WINTER_ROUTE,
                              DESCRIPTION,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', zoomobile_stations )
