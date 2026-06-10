from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Enclosure;' )
   cursor.execute( ''' CREATE TABLE Enclosure
                     (  SPECIES                               VARCHAR(64) NOT NULL,
                        EXHIBIT                               VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_SUMMARY              VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_INFORMATION          TEXT,
                        DEFAULT_ITINERARY_DURATION_MINUTES    REAL        NOT NULL,
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
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Blue-Girdled Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Brush-Tailed Bettong',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Clown Triggerfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Crested Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Crimson Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Demoiselle Crane',
      'Australasia Pavilion',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Eastern Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Emerald Tree Boa',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Flame Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Fly River Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Galah',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Green Tree Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Green-Winged Dove',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Komodo Dragon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Oct-Apr',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Lau Banded Iguana',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Live Coral Reefs',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Longnose Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'MacLeay\'s Spectres',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Malagasy Rainbowfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Mimic Surgeonfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Moon Jellyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Nicobar Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Pennant Coral Fish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Pied Imperial Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Pot-Bellied Seahorse',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red Claw Yabby',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Red-Bellied Short-Necked Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red-Tailed Black Cockatoo',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Short-Beaked Echidna',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Solomon Island Leaf Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Solomon Island Monkey-Tailed Skink',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Stimson\'s Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Tawny Frogmouth',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Thorny Devil Stick Insect',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Threadfin Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Victoria Crowned Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'White\'s Tree Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),

   # Australasia Outdoor
   (
      'Western Grey Kangaroo',
      'Australasia Outdoor',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),

   # Eurasia Wilds
   (
      'Amur Tiger',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      8,                                           # Default itinerary duration (minutes)
   ),
   (
      'Asian Wild Horse',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Bactrian Camel',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Domestic Yak',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      # TO-DO: The yaks are only viewable from the zoomobile, so something must be done especially for adding them to the itinerary
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Highland Cattle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red Panda',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      6,                                           # Default itinerary duration (minutes)
   ),
   (
      'Snow Leopard',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      8,                                           # Default itinerary duration (minutes)
   ),
   (
      'Steller\'s Sea Eagle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'West Caucasian Tur',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),

   # Tundra Trek
   (
      'Arctic Wolf',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Caribou',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Lesser Snow Goose',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Northern Bald Eagle',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Polar Bear',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American Flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The American flamingos are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Black-Handed Spider Monkey',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Sep',                                   # Seasonal viewing summary
      '''The black-handed spider monkeys are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The capybara is part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit typically opens for
         the season sometime in late March or April, and closes sometime in November. For confirmation on whether the exhibit is open,
         consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red-Legged Seriema',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The red-legged seriemas are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Turkey Vulture',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The turkey vultures are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      1,                                           # Default itinerary duration (minutes)
   ),

   # Americas Pavilion
   (
      'American Alligator',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'American Eel',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'American Lobster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Bark Scorpion',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Black-Footed Ferret',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Black-Widow Spider',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Blanding\'s Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Blue And Yellow Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Boa Constrictor',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Blue Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Brazilian Giant Cockroach',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Brazilian Salmon Pink Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Butterfly Goodeid',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Crested Tinamou',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Cuvier\'s Smooth-Fronted Caiman',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Desert Grassland Whiptail',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Dyeing Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Eastern Loggerhead Shrike',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Eastern Lubber Grasshopper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Eyelash Viper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Ferocious Water Bug',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Golden Lion Tamarin',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Great Horned Owl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Green And Black Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Green Surf Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Green-Winged Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Guatemalan Beaded Lizard',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Jamaican Boa',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Leather Sea Star',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Lemur Leaf Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Longnose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Massasauga Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Mexican Blind Cavefish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Midland Painted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'North American River Otter',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      7,                                           # Default itinerary duration (minutes)
   ),
   (
      'Opal-Rumped Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Painted Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Panamanian Golden Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Plumose Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Plush-Crested Jay',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Puerto Rican Crested Toad',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Pumpkinseed Sunfish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Red Island Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Red-Crested Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Reticulate Gila Monster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Round Goby',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Rufous-Collared Sparrow',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'San-Esteban Island Chuckwalla',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Snapping Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Spot Prawn',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Spotted River Stingray',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Spotted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Timber Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Turquoise Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Two-Toed Sloth',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor:Year-round',       # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Western Blacknose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'White-Faced Saki',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Yellow-Banded Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Zebra Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
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
      6,                                           # Default itinerary duration (minutes)
   ),
   (
      'Grizzly Bear',
      'Canadian Domain',
      'Apr-Oct',                                   # Seasonal viewing summary
      '''The grizzly bear is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Keep in mind, that even if the domain
         is open, the grizzly bear may be off display due to hibernation.'''.replace( '\n', ' ' ),
      10,                                          # Default itinerary duration (minutes)
   ),
   (
      'Northern Bald Eagle',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The Northern bald eagle is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at
         the bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime
         in March. To check whether the domain is open, consult the Toronto Zoo's official website. Bald eagles thrive in all seasons,
         and if the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Raccoon',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The raccoons are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom
         of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March.
         To check whether the domain is open, consult the Toronto Zoo's official website. Raccoons thrive in all seasons, and if the
         domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Wood Bison',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The wood bison are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Cougars thrive in all seasons, and if 
         the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      5,                                           # Default itinerary duration (minutes)
   ),

   # Africa Savanna
   (
      'African Lion',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      8,                                           # Default itinerary duration (minutes)
   ),
   (
      'African Penguin',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      7,                                           # Default itinerary duration (minutes)
   ),
   (
      'Cheetah',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Common Eland',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Grevy\'s Zebra',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Masai Giraffe',
      'Africa Savanna',
      'Outdoor: May-Oct, Indoor: Nov-Apr',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),
   (
      'Olive Baboon',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Apr-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'River Hippopotamus',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Southern White Rhinoceros',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),
   (
      'Spotted Hyena',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Warthog',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Watusi Cattle',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'White-Breasted Cormorant',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),

   # African Rainforest Pavilion
   (
      'African Clawed Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'African Spoonbill',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      'Outdoor: Jun-Sep, Indoor: Oct-May',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Black Crake',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Blue-Bellied Roller',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Gaboon Viper',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Grey-Necked Crowned Crane',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Lake Malawi Cichlids',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Lau Banded Iguana',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Leopard Ctenopoma',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Mantella (Poison Frog)',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Naked Mole Rat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Nile Soft-Shelled Turtle',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Pygmy Hippopotamus',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Radiated Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red River Hog',
      'African Rainforest Pavilion',
      'Apr-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Ring-Tailed Lemur',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Royal Python',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Sacred Ibis',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Slender-Tailed Meerkat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'South African Crested Porcupine',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'South African Shelduck',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Speckled Mousebird',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Spider Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Straw Coloured Fruit Bat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Tomato Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Veiled Chameleon',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Violaceous Plantain Eater',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'West African Dwarf Crocodile',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Western Lowland Gorilla',
      'African Rainforest Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),

   # Indo-Malaya Pavilion
   (
      'Asian Brown Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Bighead Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Black Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Black-Breasted Leaf Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Black-Throated Laughing Thrush',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Burmese Star Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Cattle Egret',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Concave Casqued Hornbill',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Crested Wood Partridge',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Crocodile Lizard',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Crocodile Newt',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Edward\'s Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Giant Gourami',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Grass Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Green Crested Basilisk',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Hamilton\'s Pond Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Iridescent Shark Catfish',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Luzon Bleeding-Heart Dove',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Malayan Bonytongue',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Malaysian Painted Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Mekong Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Monocled Cobra',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Nicobar Pigeon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Palawan Peacock-Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Red-Lined Torpedo Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Reticulated Python',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Spiny Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),

   (
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      10,                                          # Default itinerary duration (minutes)
   ),
   (
      'Tentacled Snake',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Tinfoil Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Tri-Coloured Shark',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'White-Handed Gibbon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Outdoor: Apr-Nov, Indoor: Nov-Mar',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Indo-Malaya Outdoor',
      'Outdoor: May-Oct, Indoor: Nov-Apr',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      7,                                           # Default itinerary duration (minutes)
   ),
   (
      'Indian Peafowl',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),
   (
      'Cheetah',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   # Malayan Woods Pavilion
   (
      'Asian Giant Millipede',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Clouded Leopard',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      5,                                           # Default itinerary duration (minutes)
   ),
   (
      'Giant Gourami',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Gooty Sapphire Ornamental Tarantula',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Malayan Walking Stick',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Malaysian Stick Insect Jungle Wood Nymph',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      0.5,                                         # Default itinerary duration (minutes)
   ),
   (
      'Red-Tailed Green Ratsnake',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Wrinkled Hornbill',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      2,                                           # Default itinerary duration (minutes)
   ),

   # Goat World
   (
      'Domestic Goat',
      'Goat World',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      3,                                           # Default itinerary duration (minutes)
   ),

   # Kids Zoo
   (
      'African Spurred Tortoise',
      'Kids Zoo',
      'Outdoor: May-Oct',                          # Seasonal viewing summary
      '''The African spurred tortoise is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through
         October. To check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Common Raven',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The common raven is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The raven is a very hardy species, and should
         be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Eurasian Eagle Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The Eurasian eagle owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Eurasian eagle owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Great Horned Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The great horned owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The great horned owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Guinea Pig',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The guinea pig is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Harris\'s Hawk',
      'Kids Zoo',
      'Apr-Nov',                                   # Seasonal viewing summary
      '''The Harris\'s hawk is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Harris's hawk is a somewhat hardy species,
         and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      1,                                           # Default itinerary duration (minutes)
   ),
   (
      'Marabou Stork',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The marabou stork is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   ),
   (
      'Rabbit',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The rabbit is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website. The rabbit is a hardy species, and should be viewable
         if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      2,                                           # Default itinerary duration (minutes)
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Enclosure (
                              SPECIES,
                              EXHIBIT,
                              SEASONAL_VIEWING_SUMMARY,
                              SEASONAL_VIEWING_INFORMATION,
                              DEFAULT_ITINERARY_DURATION_MINUTES
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', enclosures )
