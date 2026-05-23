from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Enclosure;' )
   cursor.execute( ''' CREATE TABLE Enclosure
                     (  SPECIES                          VARCHAR(64) NOT NULL,
                        EXHIBIT                          VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_SUMMARY         VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_INFORMATION     TEXT,
                        FOREIGN KEY (SPECIES) REFERENCES Animal,
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(Name),
                        PRIMARY KEY (SPECIES, EXHIBIT) ); ''' )

enclosures =\
[
   # Australasia Pavilion indoor enclosures
   (
      'Black Tree Monitor',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Blue-Girdled Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Brush-Tailed Bettong',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Clown Triggerfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crested Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crimson Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Demoiselle Crane',
      'Australasia Pavilion',
      'Mar-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Eastern Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Emerald Tree Boa',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Flame Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Fly River Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Galah',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green Tree Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green-Winged Dove',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Komodo Dragon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Oct-Apr',         # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lau Banded Iguana',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Live Coral Reefs',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Longnose Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'MacLeay\'s Spectres',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Malagasy Rainbowfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Mimic Surgeonfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Moon Jellyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Nicobar Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Pennant Coral Fish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Pied Imperial Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Pot-Bellied Seahorse',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red Claw Yabby',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red-Bellied Short-Necked Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red-Tailed Black Cockatoo',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Short-Beaked Echidna',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Solomon Island Leaf Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Solomon Island Monkey-Tailed Skink',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Stimson\'s Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tawny Frogmouth',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Thorny Devil Stick Insect',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Threadfin Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Victoria Crowned Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'White\'s Tree Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Australasia Outdoor
   (
      'Western Grey Kangaroo',
      'Australasia Outdoor',
      'Mar-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Eurasia Wilds
   (
      'Amur Tiger',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Asian Wild Horse',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Bactrian Camel',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Domestic Yak',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Highland Cattle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red Panda',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Snow Leopard',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Steller\'s Sea Eagle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'West Caucasian Tur',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Tundra Trek
   (
      'Arctic Wolf',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Caribou',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lesser Snow Goose',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Northern Bald Eagle',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Polar Bear',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American Flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The American flamingos are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),
   (
      'Black-Handed Spider Monkey',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Sep',                                   # Seasonal viewing summary
      '''The black-handed spider monkeys are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The capybara is part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit typically opens for
         the season sometime in late March or April, and closes sometime in November. For confirmation on whether the exhibit is open,
         consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),
   (
      'Red-Legged Seriema',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The red-legged seriemas are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),
   (
      'Turkey Vulture',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The turkey vultures are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),

   # Americas Pavilion
   (
      'American Alligator',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'American Eel',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'American Lobster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Bark Scorpion',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black-Footed Ferret',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black-Widow Spider',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Blanding\'s Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Blue And Yellow Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Boa Constrictor',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Blue Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Brazilian Giant Cockroach',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Brazilian Salmon Pink Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Butterfly Goodeid',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crested Tinamou',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Cuvier\'s Smooth-Fronted Caiman',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Desert Grassland Whiptail',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Dyeing Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Eastern Loggerhead Shrike',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Eastern Lubber Grasshopper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Eyelash Viper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Ferocious Water Bug',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Golden Lion Tamarin',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Great Horned Owl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green And Black Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green Surf Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green-Winged Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Guatemalan Beaded Lizard',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Jamaican Boa',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Leather Sea Star',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lemur Leaf Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Longnose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Massasauga Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Mexican Blind Cavefish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Midland Painted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'North American River Otter',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Opal-Rumped Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Painted Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Panamanian Golden Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Plumose Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Plush-Crested Jay',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Puerto Rican Crested Toad',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Pumpkinseed Sunfish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red Island Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red-Crested Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Reticulate Gila Monster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Round Goby',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Rufous-Collared Sparrow',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'San-Esteban Island Chuckwalla',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Snapping Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spot Prawn',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spotted River Stingray',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spotted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Timber Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Turquoise Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Two-Toed Sloth',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor:Year-round',       # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Western Blacknose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'White-Faced Saki',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Yellow-Banded Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Zebra Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Canadian Domain
   (
      'Cougar',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The cougars are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom
         of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March.
         To check whether the domain is open, consult the Toronto Zoo's official website. Cougars thrive in all seasons, and if the
         domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
   ),
   (
      'Grizzly Bear',
      'Canadian Domain',
      'Apr-Oct',                                   # Seasonal viewing summary
      '''The grizzly bear is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Keep in mind, that even if the domain
         is open, the grizzly bear may be off display due to hibernation.'''.replace( '\n', ' ' ),
   ),
   (
      'Northern Bald Eagle',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The Northern bald eagle is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at
         the bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime
         in March. To check whether the domain is open, consult the Toronto Zoo's official website. Bald eagles thrive in all seasons,
         and if the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
   ),
   (
      'Raccoon',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The raccoons are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom
         of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March.
         To check whether the domain is open, consult the Toronto Zoo's official website. Raccoons thrive in all seasons, and if the
         domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
   ),
   (
      'Wood Bison',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The wood bison are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Cougars thrive in all seasons, and if 
         the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
   ),

   # Africa Savanna
   (
      'African Lion',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'African Penguin',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Cheetah',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Common Eland',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Grevy\'s Zebra',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Masai Giraffe',
      'Africa Savanna',
      'Outdoor: May-Oct, Indoor: Nov-Apr',         # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Olive Baboon',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Apr-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'River Hippopotamus',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Southern White Rhinoceros',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spotted Hyena',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Warthog',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Watusi Cattle',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'White-Breasted Cormorant',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # African Rainforest Pavilion
   (
      'African Clawed Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'African Spoonbill',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      'Outdoor: Jun-Sep, Indoor: Oct-May',         # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black Crake',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Blue-Bellied Roller',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Gaboon Viper',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Grey-Necked Crowned Crane',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lake Malawi Cichlids',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Lau Banded Iguana',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Leopard Ctenopoma',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Mantella (Poison Frog)',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Naked Mole Rat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Nile Soft-Shelled Turtle',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Pygmy Hippopotamus',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Radiated Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red River Hog',
      'African Rainforest Pavilion',
      'Apr-Nov',                                   # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Ring-Tailed Lemur',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Royal Python',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Sacred Ibis',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Slender-Tailed Meerkat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'South African Crested Porcupine',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'South African Shelduck',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Speckled Mousebird',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spider Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Straw Coloured Fruit Bat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tomato Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Veiled Chameleon',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Violaceous Plantain Eater',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'West African Dwarf Crocodile',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'African Spurred Tortoise',
      'African Rainforest Pavilion',
      'Outdoor: Apr-May, Oct',                     # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Western Lowland Gorilla',
      'African Rainforest Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Indo-Malaya Pavilion
   (
      'Asian Brown Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Bighead Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black-Breasted Leaf Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Black-Throated Laughing Thrush',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Burmese Star Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Cattle Egret',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Concave Casqued Hornbill',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crested Wood Partridge',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crocodile Lizard',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Crocodile Newt',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Edward\'s Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Giant Gourami',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Grass Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Green Crested Basilisk',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Hamilton\'s Pond Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Iridescent Shark Catfish',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Luzon Bleeding-Heart Dove',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Malayan Bonytongue',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Malaysian Painted Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Mekong Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Monocled Cobra',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Nicobar Pigeon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Palawan Peacock-Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red-Lined Torpedo Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Reticulated Python',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Spiny Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   (
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tentacled Snake',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tinfoil Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Tri-Coloured Shark',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'White-Handed Gibbon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Outdoor: Apr-Nov, Indoor: Nov-Mar',         # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Indian Peafowl',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Cheetah',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   # Malayan Woods Pavilion
   (
      'Asian Giant Millipede',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Clouded Leopard',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Giant Gourami',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Gooty Sapphire Ornamental Tarantula',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Malayan Walking Stick',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Malaysian Stick Insect Jungle Wood Nymph',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Red-Tailed Green Ratsnake',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),
   (
      'Wrinkled Hornbill',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Goat World
   (
      'Domestic Goat',
      'Goat World',
      'Year-round',                                # Seasonal viewing summary
      None                                         # Seasonal viewing information (for seasonal exhibits)
   ),

   # Kids Zoo
   (
      'Abyssinian Ground Hornbill',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The Abyssinian ground hornbill is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through
         October. To check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
   ),
   (
      'Common Raven',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The common raven is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The raven is a very hardy species, and should
         be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ).replace( '*', '\n' )
   ),
   (
      'Eurasian Eagle Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The Eurasian eagle owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Eurasian eagle owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' )
   ),
   (
      'Great Horned Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The great horned owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The great horned owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
   ),
   (
      'Guinea Pig',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The guinea pig is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
   ),
   (
      'Harris\'s Hawk',
      'Kids Zoo',
      'Apr-Nov',                                   # Seasonal viewing summary
      '''The Harris\'s hawk is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Harris's hawk is a somewhat hardy species,
         and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
   ),
   (
      'Marabou Stork',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The marabou stork is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
   ),
   (
      'Rabbit',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The rabbit is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website. The rabbit is a hardy species, and should be viewable
         if the Kids Zoo is open.'''.replace( '\n', ' ' ),
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Enclosure (
                              SPECIES,
                              EXHIBIT,
                              SEASONAL_VIEWING_SUMMARY,
                              SEASONAL_VIEWING_INFORMATION
                           ) 
                           VALUES (?, ?, ?, ?) ''', enclosures )
