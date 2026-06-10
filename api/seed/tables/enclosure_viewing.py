from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS EnclosureViewing;' )
   cursor.execute( ''' CREATE TABLE EnclosureViewing
                     (  SPECIES                          VARCHAR(64) NOT NULL,
                        EXHIBIT                          VARCHAR(64) NOT NULL,
                        ENCLOSURE_TYPE                   VARCHAR(64) NOT NULL,
                        SEASONALLY_OFF_DISPLAY_MESSAGE   TEXT,     
                        X_COORD                          FLOAT       NOT NULL,
                        Y_COORD                          FLOAT       NOT NULL,
                        FOREIGN KEY (SPECIES) REFERENCES Animal,
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(Name),
                        PRIMARY KEY (SPECIES, EXHIBIT, X_COORD, Y_COORD) ); ''' )

enclosure_viewings =\
[
   # Australasia Pavilion
   (
      'Black Tree Monitor',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Blue-Girdled Angelfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Brush-Tailed Bettong',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Clown Triggerfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Crested Pigeon',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Crimson Rosella',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Eastern Rosella',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Emerald Tree Boa',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Flame Angelfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Fly River Turtle',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Galah',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Green Tree Python',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Green-Winged Dove',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Komodo Dragon',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Lau Banded Iguana',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Live Coral Reefs',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Longnose Butterflyfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'MacLeay\'s Spectres',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Malagasy Rainbowfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Mimic Surgeonfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Moon Jellyfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Nicobar Pigeon',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Pennant Coral Fish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Pied Imperial Pigeon',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Pot-Bellied Seahorse',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Red Claw Yabby',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Red-Bellied Short-Necked Turtle',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Red-Tailed Black Cockatoo',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Short-Beaked Echidna',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Solomon Island Leaf Frog',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Solomon Island Monkey-Tailed Skink',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Stimson\'s Python',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Tawny Frogmouth',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Thorny Devil Stick Insect',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Threadfin Butterflyfish',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Victoria Crowned Pigeon',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'White\'s Tree Frog',
      'Australasia Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      72.869,                 # X coordinate on map
      67.782,                 # Y coordinate on map
   ),
   (
      'Demoiselle Crane',
      'Australasia Pavilion',
      'Outdoor',
      '''The demoiselle cranes are likely to be inside and off display on this day due to cold weather.''',
      72.925,                 # X coordinate on map
      64.81,                  # Y coordinate on map
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Outdoor',
      '''The kookaburras can most likely be seen inside on this day due to cooler weather.''',
      72.925,                 # X coordinate on map
      64.81,                  # Y coordinate on map
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor',
      '''The wombats can most likely be seen inside on this day due to cooler weather.''',
      73.888,                 # X coordinate on map
      67.181,                 # Y coordinate on map
   ),

   # Australasia Outdoor
   (
      'Western Grey Kangaroo',
      'Australasia Outdoor',
      'Outdoor',
      '''The kangaroos are likely to be inside and off display on this day due to cold weather.''',
      75.357,                 # X coordinate on map
      72.167,                 # Y coordinate on map
   ),

   # Eurasia Wilds
   (
      'Amur Tiger',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      76.076,                 # X coordinate on map
      76.176,                 # Y coordinate on map
   ),
   (
      'Asian Wild Horse',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      83.172,                 # X coordinate on map
      65.82                   # Y coordinate on map
   ),
   (
      'Asian Wild Horse',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      91.461,                 # X coordinate on map
      85.732                  # Y coordinate on map
   ),
   (
      'Bactrian Camel',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      85.339,                 # X coordinate on map
      84.538                  # Y coordinate on map
   ),
   (
      'Bactrian Camel',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      81.436,                 # X coordinate on map
      83.418                  # Y coordinate on map
   ),
   (
      'Domestic Yak',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      90.495,                 # X coordinate on map
      90.868                  # Y coordinate on map
   ),
   (
      'Highland Cattle',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      82.525,                 # X coordinate on map
      95.269                  # Y coordinate on map
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      79.357,                 # X coordinate on map
      69.972                  # Y coordinate on map
   ),
   (
      'Red Panda',
      'Africa Savanna',
      'Outdoor',
      '''The red pandas are likely to be inside and off-display on this day due to particularly harsh conditions.''',
      # 76,
      # 35.25
      52.186,                 # X coordinate on map
      42.034                  # Y coordinate on map
   ),
   (
      'Snow Leopard',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      86.033,                 # X coordinate on map
      76.673                  # Y coordinate on map
   ),
   (
      'Steller\'s Sea Eagle',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      86.73,                  # X coordinate on map
      79.365                  # Y coordinate on map
   ),
   (
      'West Caucasian Tur',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      85.24,                  # X coordinate on map
      72.803                  # Y coordinate on map
   ),
   (
      'West Caucasian Tur',
      'Eurasia Wilds',
      'Outdoor',
      None,                   # Seasonally off-display message
      88.224,                 # X coordinate on map
      93.671                  # Y coordinate on map
   ),

   # Tundra Trek
   (
      'Arctic Wolf',
      'Tundra Trek',
      'Outdoor',
      None,                   # Seasonally off-display message
      75.673,                 # X coordinate on map
      53.208                  # Y coordinate on map
   ),
   (
      'Caribou',
      'Tundra Trek',
      'Outdoor',
      None,                   # Seasonally off-display message
      77.744,                 # X coordinate on map
      43.772                  # Y coordinate on map
   ),
   (
      'Lesser Snow Goose',
      'Tundra Trek',
      'Outdoor',
      None,                   # Seasonally off-display message
      72.064,                 # X coordinate on map
      51.575                  # Y coordinate on map
   ),
   (
      'Northern Bald Eagle',
      'Tundra Trek',
      'Outdoor',
      None,                   # Seasonally off-display message
      73.885,                 # X coordinate on map
      46.811                  # Y coordinate on map
   ),
   (
      'Polar Bear',
      'Tundra Trek',
      'Outdoor',
      None,                   # Seasonally off-display message
      78.289,                 # X coordinate on map
      51.1                    # Y coordinate on map
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American Flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      '''The American flamingos are likely to be inside and off display on this day due to cold weather.''',
      77.471,                 # X coordinate on map
      38.008                  # Y coordinate on map
   ),
   (
      'Black-Handed Spider Monkey',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      '''The black-handed spider monkeys are likely to be inside and off display on this day due to colder weather.''',
      77.016,                 # X coordinate on map
      35.154                  # Y coordinate on map
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      '''The capybaras are likely to be inside and off display on this day due to cold weather.''',
      76.108,                 # X coordinate on map
      37.753                  # Y coordinate on map
   ),
   (
      'Red-Legged Seriema',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      '''The red-legged seriemas are likely to be inside and off display on this day due to cold weather.''',
      78.017,                 # X coordinate on map
      36.228                  # Y coordinate on map
   ),
   (
      'Turkey Vulture',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      '''The turkey vultures are likely to be inside and off display on this day due to cold weather.''',
      78.017,                 # X coordinate on map
      36.228                  # Y coordinate on map
   ),

   # Americas Pavilion
   (
      'American Alligator',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'American Eel',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'American Lobster',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Bark Scorpion',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Black-Footed Ferret',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Black-Widow Spider',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Blanding\'s Turtle',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Blue And Yellow Macaw',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Boa Constrictor',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Blue Poison Dart Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Brazilian Giant Cockroach',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Brazilian Salmon Pink Bird-Eating Tarantula',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Butterfly Goodeid',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Crested Tinamou',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Cuvier\'s Smooth-Fronted Caiman',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Desert Grassland Whiptail',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Dyeing Poison Dart Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Eastern Loggerhead Shrike',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Eastern Lubber Grasshopper',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Eyelash Viper',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Ferocious Water Bug',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Golden Lion Tamarin',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Great Horned Owl',
      'Americas Pavilion',
      'Outdoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Green And Black Poison Dart Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Green Surf Anemone',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Green-Winged Macaw',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Guatemalan Beaded Lizard',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Jamaican Boa',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Leather Sea Star',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Lemur Leaf Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Longnose Dace',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Massasauga Rattlesnake',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Mexican Blind Cavefish',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Midland Painted Turtle',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'North American River Otter',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Opal-Rumped Tanager',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Painted Anemone',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Panamanian Golden Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Plumose Anemone',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Plush-Crested Jay',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Puerto Rican Crested Toad',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Pumpkinseed Sunfish',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Red Island Bird-Eating Tarantula',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Red-Crested Finch',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Reticulate Gila Monster',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Round Goby',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Rufous-Collared Sparrow',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'San-Esteban Island Chuckwalla',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Snapping Turtle',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Spot Prawn',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Spotted River Stingray',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Spotted Turtle',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Timber Rattlesnake',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Turquoise Tanager',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Two-Toed Sloth',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Western Blacknose Dace',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'White-Faced Saki',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Yellow-Banded Poison Dart Frog',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Zebra Finch',
      'Americas Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      68.663,                 # X coordinate on map
      49.679                  # Y coordinate on map
   ),
   (
      'Golden Lion Tamarin',
      'Americas Pavilion',
      'Outdoor',
      '''The golden lion tamarins can most likely be seen inside on this day due to cooler weather.''',
      69.119,                 # X coordinate on map
      51.599                  # Y coordinate on map
   ),
   (
      'Two-Toed Sloth',
      'Americas Pavilion',
      'Outdoor',
      '''The sloths can most likely be seen inside on this day due to cooler weather.''',
      69.119,                 # X coordinate on map
      51.599                  # Y coordinate on map
   ),
   (
      'White-Faced Saki',
      'Americas Pavilion',
      'Outdoor',
      '''The white-faced sakis can most likely be seen inside on this day due to cooler weather.''',
      69.119,                 # X coordinate on map
      51.599                  # Y coordinate on map
   ),
   (
      'North American River Otter',
      'Americas Pavilion',
      'Outdoor',
      None,                   # Seasonally off-display message
      68.706,                 # X coordinate on map
      47.561                  # Y coordinate on map
   ),

   # Canadian Domain
   (
      'Cougar',
      'Canadian Domain',
      'Outdoor',
      None,
      26.885,                 # X coordinate on map
      7.094                   # Y coordinate on map
   ),
   (
      'Grizzly Bear',
      'Canadian Domain',
      'Outdoor',
      '''The grizzly bears are likely to be off display on this day due to cooler weather and hibernation patterns.''',
      22.896,                 # X coordinate on map
      4.714                   # Y coordinate on map
   ),
   (
      'Northern Bald Eagle',
      'Canadian Domain',
      'Outdoor',
      None,
      22.226,                 # X coordinate on map
      14.269                  # Y coordinate on map
   ),
   (
      'Raccoon',
      'Canadian Domain',
      'Outdoor',
      None,
      30.393,                 # X coordinate on map
      17.759                  # Y coordinate on map
   ),
   (
      'Wood Bison',
      'Canadian Domain',
      'Outdoor',
      None,
      28.482,                 # X coordinate on map
      4.141                   # Y coordinate on map
   ),
   (
      'Wood Bison',
      'Canadian Domain',
      'Outdoor',
      None,
      20.453,                 # X coordinate on map
      21.249                  # Y coordinate on map
   ),

   # Africa Savanna
   (
      'African Lion',
      'Africa Savanna',
      'Outdoor',
      '''The African lions are most likely inside and off-display on this day due to particularly harsh conditions.''',
      51.162,                 # X coordinate on map
      39.787                  # Y coordinate on map
   ),
   (
      'African Penguin',
      'Africa Savanna',
      'Outdoor',
      '''The penguins can most likely be seen inside on this day due to cold weather.''',
      51.001,                 # X coordinate on map
      50.458                  # Y coordinate on map
   ),
   (
      'White-Breasted Cormorant',
      'Africa Savanna',
      'Outdoor',
      '''The cormorants can most likely be seen inside on this day due to cold weather.''',
      51.001,                 # X coordinate on map
      50.458                  # Y coordinate on map
   ),
   (
      'African Penguin',
      'Africa Savanna',
      'Indoor',
      None,                   # Seasonally off-display message
      51.954,                 # X coordinate on map
      49.237                  # Y coordinate on map
   ),
   (
      'White-Breasted Cormorant',
      'Africa Savanna',
      'Indoor',
      None,                   # Seasonally off-display message
      51.954,                 # X coordinate on map
      49.237                  # Y coordinate on map
   ),
   (
      'Cheetah',
      'Africa Savanna',
      'Outdoor',
      '''The cheetahs are most likely inside and off-display on this day due to particularly harsh conditions.''',
      42.194,                 # X coordinate on map
      40.492                  # Y coordinate on map
   ),
   (
      'Common Eland',
      'Africa Savanna',
      'Outdoor',
      '''The elands are most likely inside and off-display on this day due to cold weather.''',
      50.618,                 # X coordinate on map
      44.872                  # Y coordinate on map
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'Outdoor',
      '''The greater kudus are most likely inside and off-display on this day due to cold weather.''',
      43.612,                 # X coordinate on map
      62.754                  # Y coordinate on map
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Outdoor',
      '''The marabou storks are most likely inside and off-display on this day due to cooler weather.''',
      43.612,                 # X coordinate on map
      62.754                  # Y coordinate on map
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Outdoor',
      '''The southern ground hornbills are most likely inside and off-display on this day due to cooler weather.''',
      43.612,                 # X coordinate on map
      62.754                  # Y coordinate on map
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Outdoor',
      '''The white-headed vultures are most likely inside and off-display on this day due to cooler weather.''',
      43.612,                 # X coordinate on map
      62.754                  # Y coordinate on map
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'Outdoor',
      '''The greater kudus are most likely inside and off-display on this day due to cold weather.''',
      40.544,                 # X coordinate on map
      58.662                  # Y coordinate on map
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Outdoor',
      '''The marabou storks are most likely inside and off-display on this day due to cooler weather.''',
      40.544,                 # X coordinate on map
      58.662                  # Y coordinate on map
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Outdoor',
      '''The southern ground hornbills are off-display for the season. They can be seen outside again in the summer.''',
      40.544,                 # X coordinate on map
      58.662                  # Y coordinate on map
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Outdoor',
      '''The southern ground hornbills are most likely inside and off-display on this day due to cooler weather.''',
      40.544,                 # X coordinate on map
      58.662                  # Y coordinate on map
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'Outdoor',
      '''The greater kudus are most likely inside and off-display on this day due to cold weather.''',
      41.389,                 # X coordinate on map
      55.434                  # Y coordinate on map
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Outdoor',
      '''The marabou storks are most likely inside and off-display on this day due to cooler weather.''',
      41.389,                 # X coordinate on map
      55.434                  # Y coordinate on map
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Outdoor',
      '''The southern ground hornbills are most likely inside and off-display on this day due to cooler weather.''',
      41.389,                 # X coordinate on map
      55.434                  # Y coordinate on map
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Outdoor',
      '''The white-headed vultures are most likely inside and off-display on this day due to cooler weather.''',
      41.389,                 # X coordinate on map
      55.434                  # Y coordinate on map
   ),
   (
      'Grevy\'s Zebra',
      'Africa Savanna',
      'Outdoor',
      '''The zebras are most likely inside and off-display on this day due to cold weather.''',
      46.194,                 # X coordinate on map
      41.967                  # Y coordinate on map
   ),
   (
      'Grevy\'s Zebra',
      'Africa Savanna',
      'Outdoor',
      None,                   # Seasonally off-display message
      51.664,                  # X coordinate on map (Savanna Barn)
      29.598                   # Y coordinate on map
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Outdoor',
      '''The marabou storks are most likely inside and off-display on this day due to cooler weather.''',
      43.38,                  # X coordinate on map
      43.353                  # Y coordinate on map
   ),
   (
      'Masai Giraffe',
      'Africa Savanna',
      'Outdoor',
      '''The giraffes can most likely be seen inside on this day due to cold weather.''',
      39.885,                 # X coordinate on map
      70.927                  # Y coordinate on map
   ),
   (
      'Masai Giraffe',
      'Africa Savanna',
      'Indoor',
      None,                   # Seasonally off-display message
      42.35,                  # X coordinate on map
      71.366                  # Y coordinate on map
   ),
   (
      'Olive Baboon',
      'Africa Savanna',
      'Outdoor',
      '''The baboons are most likely inside and off-display on this day due to particularly harsh conditions.''',
      46.381,                 # X coordinate on map
      37.671                  # Y coordinate on map
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Outdoor',
      '''The ostriches are most likely inside and off-display on this day due to cold weather.''',
      49.056,                 # X coordinate on map
      36.903                  # Y coordinate on map
   ),
   (
      'River Hippopotamus',
      'Africa Savanna',
      'Outdoor',
      '''The hippopotamuses are most likely inside and off-display on this day due to cooler weather.''',
      37.731,                 # X coordinate on map
      68.101                  # Y coordinate on map
   ),
   # (
   #    'Southern Ground Hornbill',
   #    'Africa Savanna',
   #    'Outdoor',
   #    '''The southern ground hornbills are most likely inside and off-display on this day due to cooler weather.''',
   #    41,                     # X coordinate on map
   #    65                      # Y coordinate on map
   # ),
   (
      'Southern White Rhinoceros',
      'Africa Savanna',
      'Outdoor',
      '''The white rhinos are most likely inside and off-display on this day due to cold weather.''',
      41.57,                  # X coordinate on map
      50.29                   # Y coordinate on map
   ),
   (
      'Spotted Hyena',
      'Africa Savanna',
      'Outdoor',
      '''The hyenas are most likely inside and off-display on this day due to particularly harsh conditions.''',
      53.96,                  # X coordinate on map
      42.207                  # Y coordinate on map
   ),
   (
      'Warthog',
      'Africa Savanna',
      'Outdoor',
      '''The warthogs are most likely inside and off-display on this day due to cooler weather.''',
      41.363,                 # X coordinate on map
      64.056                  # Y coordinate on map
   ),
   (
      'Watusi Cattle',
      'Africa Savanna',
      'Outdoor',
      '''The watusi cattle are most likely inside and off-display on this day due to particularly harsh conditions.''',
      55.34,                  # X coordinate on map
      45.331                  # Y coordinate on map
   ),

   # African Rainforest Pavilion
   (
      'African Clawed Frog',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Black Crake',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Blue-Bellied Roller',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Lake Malawi Cichlids',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Lau Banded Iguana',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Leopard Ctenopoma',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Mantella (Poison Frog)',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Naked Mole Rat',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Slender-Tailed Meerkat',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'South African Crested Porcupine',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Speckled Mousebird',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Spider Tortoise',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Tomato Frog',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Veiled Chameleon',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Violaceous Plantain Eater',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'West African Dwarf Crocodile',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      45.865,                 # X coordinate on map
      64.211                  # Y coordinate on map
   ),
   (
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      43.103,                 # X coordinate on map
      67.078                  # Y coordinate on map
   ),
   (
      'Gaboon Viper',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      43.103,                 # X coordinate on map
      67.078                  # Y coordinate on map
   ),
   (
      'Grey-Necked Crowned Crane',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      43.103,                 # X coordinate on map
      67.078                  # Y coordinate on map
   ),
   (
      'Ring-Tailed Lemur',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      43.103,                 # X coordinate on map
      67.078                  # Y coordinate on map
   ),
   (
      'Royal Python',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      43.103,                 # X coordinate on map
      67.078                  # Y coordinate on map
   ),
   (
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      'Outdoor',
      '''The Aldabra tortoises can most likely be seen inside on this day due to cooler weather.'''.replace( '\n', ' ' ),
      47.091,                 # X coordinate on map
      66.261                  # Y coordinate on map
   ),
   (
      'African Spoonbill',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Nile Soft-Shelled Turtle',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Pygmy Hippopotamus',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Radiated Tortoise',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Sacred Ibis',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'South African Shelduck',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Straw Coloured Fruit Bat',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      44.546,                 # X coordinate on map
      66.138                  # Y coordinate on map
   ),
   (
      'Red River Hog',
      'African Rainforest Pavilion',
      'Outdoor',
      '''The red river hogs are most likely inside and off-display on this day due to cold weather.''',
      44.591,                 # X coordinate on map
      68.531                  # Y coordinate on map
   ),
   (
      'Western Lowland Gorilla',
      'African Rainforest Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      47.487,                 # X coordinate on map
      62.703                  # Y coordinate on map
   ),
   (
      'Western Lowland Gorilla',
      'African Rainforest Pavilion',
      'Outdoor',
      '''The gorillas can most likely only be seen inside on this day due to cold weather.''',
      48.951,                 # X coordinate on map
      59.856                  # Y coordinate on map
   ),

   # Indo-Malaya Pavilion
   (
      'Asian Brown Tortoise',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Bighead Carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Black Carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Black-Breasted Leaf Turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Black-Throated Laughing Thrush',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Burmese Star Tortoise',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Cattle Egret',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Concave Casqued Hornbill',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Crested Wood Partridge',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Crocodile Lizard',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Crocodile Newt',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Edward\'s Pheasant',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Giant Gourami',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Grass Carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Green Crested Basilisk',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Hamilton\'s Pond Turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Iridescent Shark Catfish',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Luzon Bleeding-Heart Dove',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Malayan Bonytongue',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Malaysian Painted Turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Mekong Barb',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Monocled Cobra',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Nicobar Pigeon',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Palawan Peacock-Pheasant',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Red-Lined Torpedo Barb',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Reticulated Python',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Spiny Turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),

   (
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Tentacled Snake',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Tinfoil Barb',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Tri-Coloured Shark',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'White-Handed Gibbon',
      'Indo-Malaya Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      46.391,                 # X coordinate on map
      75.269                  # Y coordinate on map
   ),
   (
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      'Outdoor',
      '''The orangutans can most only likely be seen inside on this day due to cold weather.''',
      42.963,                 # X coordinate on map
      78.506                  # Y coordinate on map
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Outdoor',
      '''The babirusas can most likely be seen inside on this day due to cold weather.''',
      54.631,                 # X coordinate on map
      83.101                  # Y coordinate on map
   ),
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Indoor',
      None,                   # Seasonally off-display message
      53.679,                 # X coordinate on map
      84.485                  # Y coordinate on map
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Indo-Malaya Outdoor',
      'Outdoor',
      '''The greater one-horned rhinoceros is most likely inside and off-display on this day due to cold weather.''',
      52.485,                 # X coordinate on map
      85.012                  # Y coordinate on map
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Indo-Malaya Outdoor',
      'Indoor',
      None,                   # Seasonally off-display message
      53.679,                 # X coordinate on map
      84.485                  # Y coordinate on map
   ),
   (
      'Indian Peafowl',
      'Indo-Malaya Outdoor',
      'Outdoor',
      None,                   # Seasonally off-display message
      52.643,                 # X coordinate on map
      78.68                   # Y coordinate on map
   ),
   (
      'Cheetah',
      'Indo-Malaya Outdoor',
      'Outdoor',
      '''The cheetahs are most likely inside and off-display on this day due to particularly harsh conditions.''',
      49.295,                 # X coordinate on map
      71.958                  # Y coordinate on map
   ),
   # Malayan Woods Pavilion
   (
      'Asian Giant Millipede',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Clouded Leopard',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Giant Gourami',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Gooty Sapphire Ornamental Tarantula',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Malayan Walking Stick',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Malaysian Stick Insect Jungle Wood Nymph',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Red-Tailed Green Ratsnake',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),
   (
      'Wrinkled Hornbill',
      'Malayan Woods Pavilion',
      'Indoor',
      None,                   # Seasonally off-display message
      50.177,                 # X coordinate on map
      81.571                  # Y coordinate on map
   ),

   # Goat World
   (
      'Domestic Goat',
      'Goat World',
      'Outdoor',
      None,                   # Seasonally off-display message
      64.786,                 # X coordinate on map
      72.611                  # Y coordinate on map
   ),

   # TO-DO: Add individual coordinates for each Kid's Zoo animal
   # Kids Zoo
   (
      'African Spurred Tortoise',
      'Kids Zoo',
      'Outdoor',
      '''The African spurred tortoise is most likely inside and off-display on this day due to cooler weather.''',
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Common Raven',
      'Kids Zoo',
      'Outdoor',
      None,
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Eurasian Eagle Owl',
      'Kids Zoo',
      'Outdoor',
      None,
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Great Horned Owl',
      'Kids Zoo',
      'Outdoor',
      None,
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Guinea Pig',
      'Kids Zoo',
      'Indoor',
      None,
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Harris\'s Hawk',
      'Kids Zoo',
      'Outdoor',
      '''The Harris' hawks can most likely be seen inside on this day due to cold weather.''',
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Marabou Stork',
      'Kids Zoo',
      'Outdoor',
      '''The marabou storks are most likely inside and off-display on this day due to cooler weather.''',
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   ),
   (
      'Rabbit',
      'Kids Zoo',
      'Outdoor',
      '''The rabbits are most likely inside and off-display on this day due to particularly harsh conditions.''',
      66.827,                 # X coordinate on map
      80.627                  # Y coordinate on map
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO EnclosureViewing (
                              SPECIES,
                              EXHIBIT,
                              ENCLOSURE_TYPE,
                              SEASONALLY_OFF_DISPLAY_MESSAGE,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?, ?) ''', enclosure_viewings )
