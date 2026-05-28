from __future__ import annotations

from ...types import Cursor

def create_table( cursor: Cursor ) -> None:
   cursor.execute( 'DROP TABLE IF EXISTS Enclosure;' )
   cursor.execute( ''' CREATE TABLE Enclosure
                     (  SPECIES                               VARCHAR(64) NOT NULL,
                        EXHIBIT                               VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_SUMMARY              VARCHAR(64) NOT NULL,
                        SEASONAL_VIEWING_INFORMATION          TEXT,
                        DEFAULT_ITINERARY_DURATION_SECONDS    INTEGER     NOT NULL,
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
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Blue-Girdled Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Brush-Tailed Bettong',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Clown Triggerfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Crested Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Crimson Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Demoiselle Crane',
      'Australasia Pavilion',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Eastern Rosella',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Emerald Tree Boa',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Flame Angelfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Fly River Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Galah',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Green Tree Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Green-Winged Dove',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Komodo Dragon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Oct-Apr',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Lau Banded Iguana',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Live Coral Reefs',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Longnose Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'MacLeay\'s Spectres',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Malagasy Rainbowfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Mimic Surgeonfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Moon Jellyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Nicobar Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Pennant Coral Fish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Pied Imperial Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Pot-Bellied Seahorse',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red Claw Yabby',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red-Bellied Short-Necked Turtle',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red-Tailed Black Cockatoo',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Short-Beaked Echidna',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Solomon Island Leaf Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Solomon Island Monkey-Tailed Skink',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Southern Hairy-Nosed Wombat',
      'Australasia Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Stimson\'s Python',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Tawny Frogmouth',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Thorny Devil Stick Insect',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Threadfin Butterflyfish',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Victoria Crowned Pigeon',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'White\'s Tree Frog',
      'Australasia Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),

   # Australasia Outdoor
   (
      'Western Grey Kangaroo',
      'Australasia Outdoor',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),

   # Eurasia Wilds
   (
      'Amur Tiger',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      480,                                         # Default itinerary duration (seconds)
   ),
   (
      'Asian Wild Horse',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Bactrian Camel',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Domestic Yak',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      # TO-DO: The yaks are only viewable from the zoomobile, so something must be done especially for adding them to the itinerary
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Highland Cattle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Red Panda',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      360,                                         # Default itinerary duration (seconds)
   ),
   (
      'Snow Leopard',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      480,                                         # Default itinerary duration (seconds)
   ),
   (
      'Steller\'s Sea Eagle',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'West Caucasian Tur',
      'Eurasia Wilds',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),

   # Tundra Trek
   (
      'Arctic Wolf',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Caribou',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Lesser Snow Goose',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Northern Bald Eagle',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Polar Bear',
      'Tundra Trek',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American Flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The American flamingos are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Black-Handed Spider Monkey',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Sep',                                   # Seasonal viewing summary
      '''The black-handed spider monkeys are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The capybara is part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit typically opens for
         the season sometime in late March or April, and closes sometime in November. For confirmation on whether the exhibit is open,
         consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Red-Legged Seriema',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The red-legged seriemas are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Turkey Vulture',
      'Americas Outdoor Mayan Temple Ruins',
      'May-Oct',                                   # Seasonal viewing summary
      '''The turkey vultures are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      60,                                          # Default itinerary duration (seconds)
   ),

   # Americas Pavilion
   (
      'American Alligator',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'American Eel',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'American Lobster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Bark Scorpion',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Black-Footed Ferret',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Black-Widow Spider',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Blanding\'s Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Blue And Yellow Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Boa Constrictor',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Blue Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Brazilian Giant Cockroach',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Brazilian Salmon Pink Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Butterfly Goodeid',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Crested Tinamou',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Cuvier\'s Smooth-Fronted Caiman',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Desert Grassland Whiptail',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Dyeing Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Eastern Loggerhead Shrike',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Eastern Lubber Grasshopper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Eyelash Viper',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Ferocious Water Bug',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Golden Lion Tamarin',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Great Horned Owl',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Green And Black Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Green Surf Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Green-Winged Macaw',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Guatemalan Beaded Lizard',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Jamaican Boa',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Leather Sea Star',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Lemur Leaf Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Longnose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Massasauga Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Mexican Blind Cavefish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Midland Painted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'North American River Otter',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      420,                                         # Default itinerary duration (seconds)
   ),
   (
      'Opal-Rumped Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Painted Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Panamanian Golden Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Plumose Anemone',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Plush-Crested Jay',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Puerto Rican Crested Toad',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Pumpkinseed Sunfish',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red Island Bird-Eating Tarantula',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red-Crested Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Reticulate Gila Monster',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Round Goby',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Rufous-Collared Sparrow',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'San-Esteban Island Chuckwalla',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Snapping Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Spot Prawn',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Spotted River Stingray',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Spotted Turtle',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Timber Rattlesnake',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Turquoise Tanager',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Two-Toed Sloth',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor:Year-round',       # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Western Blacknose Dace',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'White-Faced Saki',
      'Americas Pavilion',
      'Outdoor: May-Sep, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Yellow-Banded Poison Dart Frog',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Zebra Finch',
      'Americas Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
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
      360,                                         # Default itinerary duration (seconds)
   ),
   (
      'Grizzly Bear',
      'Canadian Domain',
      'Apr-Oct',                                   # Seasonal viewing summary
      '''The grizzly bear is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Keep in mind, that even if the domain
         is open, the grizzly bear may be off display due to hibernation.'''.replace( '\n', ' ' ),
      600,                                         # Default itinerary duration (seconds)
   ),
   (
      'Northern Bald Eagle',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The Northern bald eagle is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at
         the bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime
         in March. To check whether the domain is open, consult the Toronto Zoo's official website. Bald eagles thrive in all seasons,
         and if the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Raccoon',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The raccoons are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom
         of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March.
         To check whether the domain is open, consult the Toronto Zoo's official website. Raccoons thrive in all seasons, and if the
         domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Wood Bison',
      'Canadian Domain',
      'Mar-Dec',                                   # Seasonal viewing summary
      '''The wood bison are part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website. Cougars thrive in all seasons, and if 
         the domain is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      300,                                         # Default itinerary duration (seconds)
   ),

   # Africa Savanna
   (
      'African Lion',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      480,                                         # Default itinerary duration (seconds)
   ),
   (
      'African Penguin',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      420,                                         # Default itinerary duration (seconds)
   ),
   (
      'Cheetah',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Common Eland',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Greater Kudu',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Grevy\'s Zebra',
      'Africa Savanna',
      'Mar-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Marabou Stork',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Masai Giraffe',
      'Africa Savanna',
      'Outdoor: May-Oct, Indoor: Nov-Apr',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),
   (
      'Olive Baboon',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Apr-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'River Hippopotamus',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),
   (
      'Southern Ground Hornbill',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Southern White Rhinoceros',
      'Africa Savanna',
      'May-Oct',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),
   (
      'Spotted Hyena',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Warthog',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Watusi Cattle',
      'Africa Savanna',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'White-Breasted Cormorant',
      'Africa Savanna',
      'Outdoor: Mar-Nov, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'White-Headed Vulture',
      'Africa Savanna',
      'Jun-Sep',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),

   # African Rainforest Pavilion
   (
      'African Clawed Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'African Spoonbill',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Aldabra Tortoise',
      'African Rainforest Pavilion',
      'Outdoor: Jun-Sep, Indoor: Oct-May',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Black Crake',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Blue-Bellied Roller',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Gaboon Viper',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Grey-Necked Crowned Crane',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Lake Malawi Cichlids',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Lau Banded Iguana',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Leopard Ctenopoma',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Mantella (Poison Frog)',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Naked Mole Rat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Nile Soft-Shelled Turtle',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Pygmy Hippopotamus',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Radiated Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red River Hog',
      'African Rainforest Pavilion',
      'Apr-Nov',                                   # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Ring-Tailed Lemur',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Royal Python',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Sacred Ibis',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Slender-Tailed Meerkat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'South African Crested Porcupine',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'South African Shelduck',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Speckled Mousebird',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Spider Tortoise',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Straw Coloured Fruit Bat',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Tomato Frog',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Veiled Chameleon',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Violaceous Plantain Eater',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'West African Dwarf Crocodile',
      'African Rainforest Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Western Lowland Gorilla',
      'African Rainforest Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),

   # Indo-Malaya Pavilion
   (
      'Asian Brown Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Bighead Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Black Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Black-Breasted Leaf Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Black-Throated Laughing Thrush',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Burmese Star Tortoise',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Cattle Egret',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Concave Casqued Hornbill',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Crested Wood Partridge',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Crocodile Lizard',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Crocodile Newt',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Edward\'s Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Giant Gourami',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Grass Carp',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Green Crested Basilisk',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Hamilton\'s Pond Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Iridescent Shark Catfish',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Luzon Bleeding-Heart Dove',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Malayan Bonytongue',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Malaysian Painted Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Mekong Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Monocled Cobra',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Nicobar Pigeon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Palawan Peacock-Pheasant',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red-Lined Torpedo Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Reticulated Python',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Spiny Turtle',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),

   (
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      'Outdoor: Apr-Oct, Indoor: Year-round',      # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      600,                                         # Default itinerary duration (seconds)
   ),
   (
      'Tentacled Snake',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Tinfoil Barb',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Tri-Coloured Shark',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'White-Handed Gibbon',
      'Indo-Malaya Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Outdoor: Apr-Nov, Indoor: Nov-Mar',         # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Greater One-Horned Rhinoceros',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      420,                                         # Default itinerary duration (seconds)
   ),
   (
      'Indian Peafowl',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),
   (
      'Cheetah',
      'Indo-Malaya Outdoor',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   # Malayan Woods Pavilion
   (
      'Asian Giant Millipede',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Clouded Leopard',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      300,                                         # Default itinerary duration (seconds)
   ),
   (
      'Giant Gourami',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Gooty Sapphire Ornamental Tarantula',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Malayan Walking Stick',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Malaysian Stick Insect Jungle Wood Nymph',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      30,                                          # Default itinerary duration (seconds)
   ),
   (
      'Red-Tailed Green Ratsnake',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Wrinkled Hornbill',
      'Malayan Woods Pavilion',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      120,                                         # Default itinerary duration (seconds)
   ),

   # Goat World
   (
      'Domestic Goat',
      'Goat World',
      'Year-round',                                # Seasonal viewing summary
      None,                                        # Seasonal viewing information (for seasonal exhibits)
      180,                                         # Default itinerary duration (seconds)
   ),

   # Kids Zoo
   (
      'African Spurred Tortoise',
      'Kids Zoo',
      'Outdoor: May-Oct',                          # Seasonal viewing summary
      '''The African spurred tortoise is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through
         October. To check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Common Raven',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The common raven is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The raven is a very hardy species, and should
         be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Eurasian Eagle Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The Eurasian eagle owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Eurasian eagle owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Great Horned Owl',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The great horned owl is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October.
         To check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The great horned owl is a very hardy
         species, and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Guinea Pig',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The guinea pig is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Harris\'s Hawk',
      'Kids Zoo',
      'Apr-Nov',                                   # Seasonal viewing summary
      '''The Harris\'s hawk is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website. The Harris's hawk is a somewhat hardy species,
         and should be viewable if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      60,                                          # Default itinerary duration (seconds)
   ),
   (
      'Marabou Stork',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The marabou stork is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To
         check whether the Kids Zoo is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   ),
   (
      'Rabbit',
      'Kids Zoo',
      'Year-round',                                # Seasonal viewing summary
      '''The rabbit is part of the Kids Zoo exhibit at the zoo, which is open seasonally, roughly from May through October. To check
         whether the Kids Zoo is open, consult the Toronto Zoo's official website. The rabbit is a hardy species, and should be viewable
         if the Kids Zoo is open.'''.replace( '\n', ' ' ),
      120,                                         # Default itinerary duration (seconds)
   )
]

def insert_rows( cursor: Cursor ) -> None:
   cursor.executemany( ''' INSERT INTO Enclosure (
                              SPECIES,
                              EXHIBIT,
                              SEASONAL_VIEWING_SUMMARY,
                              SEASONAL_VIEWING_INFORMATION,
                              DEFAULT_ITINERARY_DURATION_SECONDS
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', enclosures )
