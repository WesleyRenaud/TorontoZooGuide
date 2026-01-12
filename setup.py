import sqlite3

conn = sqlite3.connect( 'animals.db' )

cursor = conn.cursor()

cursor.execute( 'DROP TABLE IF EXISTS Animal;' )
cursor.execute( ''' CREATE TABLE Animal
                  (  SPECIES                    VARCHAR(64) NOT NULL,
                     LOCATION                   VARCHAR(64) NOT NULL,
                     HAS_OUTDOOR_VIEWING        BOOL        NOT NULL,
                     HAS_INDOOR_VIEWING         BOOL        NOT NULL,
                     ALWAYS_VIEWABLE            BOOL        NOT NULL,
                     ALWAYS_VIEWABLE_OUTDOORS   BOOL,
                     MIN_TEMPERATURE            INTEGER,
                     SNOW_RESISTANCE            INTEGER     CHECK (SNOW_RESISTANCE BETWEEN 0 AND 5),
                     JAN_VIEWABILITY            INTEGER     CHECK (JAN_VIEWABILITY BETWEEN 0 AND 5),
                     FEB_VIEWABILITY            INTEGER     CHECK (FEB_VIEWABILITY BETWEEN 0 AND 5),
                     MAR_VIEWABILITY            INTEGER     CHECK (MAR_VIEWABILITY BETWEEN 0 AND 5),
                     APR_VIEWABILITY            INTEGER     CHECK (APR_VIEWABILITY BETWEEN 0 AND 5),
                     MAY_VIEWABILITY            INTEGER     CHECK (MAY_VIEWABILITY BETWEEN 0 AND 5),
                     JUN_VIEWABILITY            INTEGER     CHECK (JUN_VIEWABILITY BETWEEN 0 AND 5),
                     JUL_VIEWABILITY            INTEGER     CHECK (JUL_VIEWABILITY BETWEEN 0 AND 5),
                     AUG_VIEWABILITY            INTEGER     CHECK (AUG_VIEWABILITY BETWEEN 0 AND 5),
                     SEP_VIEWABILITY            INTEGER     CHECK (SEP_VIEWABILITY BETWEEN 0 AND 5),
                     OCT_VIEWABILITY            INTEGER     CHECK (OCT_VIEWABILITY BETWEEN 0 AND 5),
                     NOV_VIEWABILITY            INTEGER     CHECK (NOV_VIEWABILITY BETWEEN 0 AND 5),
                     DEC_VIEWABILITY            INTEGER     CHECK (DEC_VIEWABILITY BETWEEN 0 AND 5),
                     WINTER_VIEWABILITY         INTEGER     CHECK (WINTER_VIEWABILITY BETWEEN 0 AND 5),
                     PRIMARY KEY (SPECIES, LOCATION) ); ''' )

animals = [
   # Australasia Pavilion
   (
      'Brownbanded bamboo shark',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Central bearded dragon',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Clown triggerfish',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Crimson rosella',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Demoiselle crane',
      'Australasia Pavilion',
      1, # Has outdoor viewing
      0, # Has indoor viewing
      1, # Always viewable
      1, # Always viewable outdoors
      0,
      4,
      1,1,4,5,5,5,5,5,5,5,4,3,
      1
   ),
   (
      'Eastern rosella',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Emerald tree boa',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Fly River turtle',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Green tree python',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Galah',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Green-winged dove',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Komodo dragon',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      1, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      15,
      0,
      0,0,0,3,4,5,5,5,5,3,0,0,
      0
   ),
   (
      'Lau banded iguana',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Live coral reefs',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Longnose butterflyfish',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'MacLeay\'s spectres',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Moon jellyfish',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Nicobar pigeon',
      'Australasia Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Pennant coral fish',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Pot-bellied seahorse',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red claw yabby',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red-tailed black cockatoo',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Short-beaked echidna',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Solomon Island leaf frog',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Southern hairy-nosed wombat',
      'Australasia Pavilion',
      1, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      10,
      0,
      0,0,0,2,4,5,5,5,5,2,0,0,
      0
   ),
   (
      'Thorny devil stick insect',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Victoria crowned pigeon',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'White\'s tree frog',
      'Australasia Pavilion',
      0, # Has outdoor viewing
      1, # Has indoor viewing
      1, # Always viewable
      0, # Always viewable outdoors
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),

   # Australasia Outdoor
   (
      'Western grey kangaroo',
      'Australasia Outdoor',
      1, # Has outdoor viewing
      0, # Has indoor viewing
      1, # Always viewable
      1, # Always viewable outdoors
      0,
      2,
      1,1,3,4,5,5,5,5,5,5,4,2,
      1
   ),

   # Eurasia Wilds
   (
      'Amur tiger',
      'Eurasia Wilds',
      1, # Has outdoor viewing
      0, # Has indoor viewing
      1, # Always viewable
      1, # Always viewable outdoors
      -30,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Asian wild horse',
      'Eurasia Wilds',
      1, # Has outdoor viewing
      0, # Has indoor viewing
      1, # Always viewable
      1, # Always viewable outdoors
      -25,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Bactrian camel',
      'Eurasia Wilds',
      1, # Has outdoor viewing
      0, # Has indoor viewing
      1, # Always viewable
      1, # Always viewable outdoors
      -30,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Domestic yak',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Highland cattle',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -25,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -15,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Red panda',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -10,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Snow leopard',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -30,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Steller\'s sea eagle',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -20,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'West caucasian tur',
      'Eurasia Wilds',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -15,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),

   # Tundra Trek
   (
      'Arctic wolf',
      'Tundra Trek',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Caribou',
      'Tundra Trek',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Lesser snow goose',
      'Tundra Trek',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Northern bald eagle',
      'Tundra Trek',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -30,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Polar bear',
      'Tundra Trek',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      5,
      0,
      0,0,2,4,5,5,5,5,5,4,2,0,
      0
   ),
   (
      'Black-handed spider monkey',
      'Americas Outdoor Mayan Temple Ruins',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      15,
      0,
      0,0,1,3,5,5,5,5,5,3,1,0,
      0
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      5,
      0,
      0,0,3,4,5,5,5,5,5,4,2,0,
      0
   ),

   # Americas Pavilion
   (
      'American alligator',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'American eel',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'American lobster',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Black-footed ferret',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Black-widow spider',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Blanding\'s turtle',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Blue and yellow macaw',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Blue poison dart frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Boa constrictor',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Brazilian giant cockroach',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Brazilian salmon pink bird-eating tarantula',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Butterfly goodied',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Crested tinamou',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Cuvier\'s smooth fronted caiman',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Desert grassland whiptail',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Dyeing poison dart frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Eastern loggerhead shrike',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Eastern lubber grasshopper',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Eyelash viper',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Ferocious water bug',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Golden lion tamarin',
      'Americas Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      18,
      0,
      0,0,0,2,4,5,5,5,5,2,0,0,
      0
   ),
   (
      'Great-horned owl',
      'Americas Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -20,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Green and black poison dart frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Green surf anemone',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Green-winged macaw',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Guatamalan beaded lizard',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Jamaican boa',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Leather sea star',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Lemur leaf frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Longnose dace',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Massasauga rattlesnake',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Midland painted turtle',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'North American river otter',
      'Americas Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      5,
      5,5,5,5,5,5,5,5,5,5,5,5,
      5
   ),
   (
      'Opal-rumped tanagar',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Painted anemone',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Panamanian golden frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Plumose anemone',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Plush-crested jay',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Puerto Rican crested toad',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Pumpkinseed sunfish',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red Island bird-eating tarantula',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red-crested finch',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Reticulate gila monster',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Round goby',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Rufous-collared sparrow',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'San-Esteban Island chuckwalla',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Snapping turtle',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Spot prawn',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Spotted river stingray',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Spotted turtle',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Timber rattlesnake',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Turquoise tanager',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Two-toed sloth',
      'Americas Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,0,2,4,5,5,5,5,3,0,0,
      0
   ),
   (
      'Western blacknose dace',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'White-faced saki',
      'Americas Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      12,
      0,
      0,0,0,2,4,5,5,5,5,3,0,0,
      0
   ),
   (
      'Yellow-banded poison dart frog',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Zebra finch',
      'Americas Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),

   # Canadian Domain
   (
      'Cougar',
      'Canadian Domain',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      -20,
      4,
      0,0,5,5,5,5,5,5,5,5,5,5,
      0
   ),
   (
      'Grizzly bear',
      'Canadian Domain',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      -30,
      5,
      0,0,2,5,5,5,5,5,5,4,2,0,
      0
   ),
   (
      'Northern bald eagle',
      'Canadian Domain',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      -30,
      5,
      0,0,5,5,5,5,5,5,5,5,5,5,
      0
   ),
   (
      'Raccoon',
      'Canadian Domain',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      -35,
      5,
      0,0,5,5,5,5,5,5,5,5,5,5,
      0
   ),
   (
      'Wood bison',
      'Canadian Domain',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      -40,
      5,
      0,0,5,5,5,5,5,5,5,5,5,5,
      0
   ),

   # Africa Savanna
   (
      'African lion',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      3,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'African penguin',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      0,
      0,
      0,0,2,4,5,5,5,5,5,5,3,0,
      0
   ),
   (
      'Cheetah',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      3,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'Common eland',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      0,
      2,
      0,0,2,4,5,5,5,5,5,5,3,1,
      0
   ),
   (
      'Greater kudu',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,1,3,5,5,5,5,5,3,1,0,
      0
   ),
   (
      'Grevy\'s zebra',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      0,
      2,
      1,1,3,5,5,5,5,5,5,5,4,2,
      1
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      15,
      0,
      0,0,0,1,3,5,5,5,5,2,0,0,
      0
   ),
   (
      'Masai giraffe',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,1,3,5,5,5,5,5,4,1,0,
      0
   ),
   (
      'Olive baboon',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      4,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'Ostrich',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      0,
      1,
      0,0,3,5,5,5,5,5,5,5,3,1,
      0
   ),
   (
      'River hippopotamus',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,0,2,5,5,5,5,5,3,1,0,
      0
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      15,
      0,
      0,0,0,1,3,5,5,5,5,2,0,0,
      0
   ),
   (
      'Southern white rhinoceros',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,1,3,5,5,5,5,5,4,1,0,
      0
   ),
   (
      'Spotted hyena',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      3,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'Warthog',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,0,1,3,5,5,5,5,3,1,0,
      0
   ),
   (
      'Watusi cattle',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      2,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'White-breasted cormorant',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      0,
      0,
      0,0,2,4,5,5,5,5,5,5,3,0,
      0
   ),
   (
      'White-headed vulture',
      'Africa Savanna',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      0,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      15,
      0,
      0,0,0,1,3,5,5,5,5,2,0,0,
      0
   ),

   # African Rainforest Pavilion
   (
      'African clawed frog',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'African spoonbill',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Aldabra tortoise',
      'African Rainforest Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      20,
      0,
      0,0,0,0,1,3,4,4,3,1,0,0,
      0
   ),
   (
      'Black crake',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Blue-bellied roller',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Grey-necked crowned crane',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Lake Malawi cichlids',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Lau banded iguana',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Naked mole rat',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Nile soft-shelled turtle',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Pygmy hippopotamus',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red-footed tortoise',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red river hog',
      'African Rainforest Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      5,
      0,
      0,0,2,4,5,5,5,5,5,5,3,1,
      0
   ),
   (
      'Ring-tailed lemur',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Royal python',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Sacred ibis',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Slender-tailed meerkat',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'South African shelduck',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Speckled mousebird',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Straw coloured fruit bat',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Veiled chameleon',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'West African dwarf crocodile',
      'African Rainforest Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Western lowland gorilla',
      'African Rainforest Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,1,3,5,5,5,5,5,3,1,0,
      0
   ),

   # Indo-Malaya Pavilion
   (
      'Asian brown tortoise',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Bighead carp',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Black carp',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Black-breasted leaf turtle',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Black-throated laughing thrush',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Burmese star tortoise',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Concave casqued hornbill',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Crested wood partridge',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Crocodile lizard',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Crocodile newt',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Grass carp',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Green crested basilisk',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Luzon bleeding-heart dove',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Malayan bonytongue',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Malayan crested fireback pheasant',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Malaysian painted turtle',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Mekong barb',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Monocled cobra',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Nicobar pigeon',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Reticulated python',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Siamese catfish',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Spiny turtle',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Sumatran orangutan',
      'Indo-Malaya Pavilion',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,0,1,3,5,5,5,5,3,1,0,
      0
   ),
   (
      'Tentacled snake',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Tinfoil barb',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Tri-coloured shark',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'White-handed gibbon',
      'Indo-Malaya Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      1,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      10,
      0,
      0,0,1,3,5,5,5,5,5,4,1,0,
      0
   ),
   (
      'Greater one-horned rhinoceros',
      'Indo-Malaya Outdoor',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Indian peafowl',
      'Indo-Malaya Outdoor',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -15,
      4,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),
   (
      'Sumatran tiger',
      'Indo-Malaya Outdoor',
      1,  # HAS_OUTDOOR_VIEWING
      0,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      1,  # ALWAYS_VIEWABLE_OUTDOORS
      -5,
      3,
      4,4,5,5,5,5,5,5,5,5,5,4,
      4
   ),

   # Malayan Woods Pavilion
   (
      'Asian giant millipede',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Clouded leopard',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Giant gourami',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Gooty sapphire ornamental tarantula',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Malaysian stick insect jungle wood nymph',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Red-tailed green ratsnake',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   ),
   (
      'Wrinkled hornbill',
      'Malayan Woods Pavilion',
      0,  # HAS_OUTDOOR_VIEWING
      1,  # HAS_INDOOR_VIEWING
      1,  # ALWAYS_VIEWABLE
      0,  # ALWAYS_VIEWABLE_OUTDOORS
      None,
      None,
      None,None,None,None,None,None,None,None,None,None,None,None,
      None
   )
]

cursor.executemany( ''' INSERT INTO Animal (
                           SPECIES,
                           LOCATION,
                           HAS_OUTDOOR_VIEWING,
                           HAS_INDOOR_VIEWING,
                           ALWAYS_VIEWABLE,
                           ALWAYS_VIEWABLE_OUTDOORS,
                           MIN_TEMPERATURE,
                           SNOW_RESISTANCE,
                           JAN_VIEWABILITY,
                           FEB_VIEWABILITY,
                           MAR_VIEWABILITY,
                           APR_VIEWABILITY,
                           MAY_VIEWABILITY,
                           JUN_VIEWABILITY,
                           JUL_VIEWABILITY,
                           AUG_VIEWABILITY,
                           SEP_VIEWABILITY,
                           OCT_VIEWABILITY,
                           NOV_VIEWABILITY,
                           DEC_VIEWABILITY,
                           WINTER_VIEWABILITY
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', animals )

conn.commit()
conn.close()

print( 'Database and Animal table created successfully.' )