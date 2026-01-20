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
                     JAN_VISIBILITY             INTEGER     CHECK (JAN_VISIBILITY BETWEEN 0 AND 5),
                     FEB_VISIBILITY             INTEGER     CHECK (FEB_VISIBILITY BETWEEN 0 AND 5),
                     MAR_VISIBILITY             INTEGER     CHECK (MAR_VISIBILITY BETWEEN 0 AND 5),
                     APR_VISIBILITY             INTEGER     CHECK (APR_VISIBILITY BETWEEN 0 AND 5),
                     MAY_VISIBILITY             INTEGER     CHECK (MAY_VISIBILITY BETWEEN 0 AND 5),
                     JUN_VISIBILITY             INTEGER     CHECK (JUN_VISIBILITY BETWEEN 0 AND 5),
                     JUL_VISIBILITY             INTEGER     CHECK (JUL_VISIBILITY BETWEEN 0 AND 5),
                     AUG_VISIBILITY             INTEGER     CHECK (AUG_VISIBILITY BETWEEN 0 AND 5),
                     SEP_VISIBILITY             INTEGER     CHECK (SEP_VISIBILITY BETWEEN 0 AND 5),
                     OCT_VISIBILITY             INTEGER     CHECK (OCT_VISIBILITY BETWEEN 0 AND 5),
                     NOV_VISIBILITY             INTEGER     CHECK (NOV_VISIBILITY BETWEEN 0 AND 5),
                     DEC_VISIBILITY             INTEGER     CHECK (DEC_VISIBILITY BETWEEN 0 AND 5),
                     WINTER_VISIBILITY          INTEGER     CHECK (WINTER_VISIBILITY BETWEEN 0 AND 5),
                     SEASONAL_VIEWING_SUMMARY   VARCHAR(64),
                     SEASONAL_VIEWING_TIPS      TEXT,
                     GENERAL_VIEWING_TIPS       TEXT,
                     ANIMAL_INFO                TEXT,
                     SPECIFIC_ANIMAL_INFO       TEXT,
                     PRIMARY KEY (SPECIES, LOCATION) ); ''' )

cursor.execute( 'DROP TABLE IF EXISTS Enclosure;' )
cursor.execute( ''' CREATE TABLE Enclosure
                  (  SPECIES        VARCHAR(64) NOT NULL,
                     LOCATION       VARCHAR(64) NOT NULL,
                     EXHIBIT_TYPE   VARCHAR(64) NOT NULL,
                     X_COORD        INTEGER     NOT NULL,
                     Y_COORD        INTEGER     NOT NULL,
                     FOREIGN KEY (SPECIES, LOCATION) REFERENCES Animal,
                     PRIMARY KEY (SPECIES, X_COORD, Y_COORD) ); ''' )

animals = [
   # Australasia Pavilion
   (
      'Brownbanded bamboo shark',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Central bearded dragon',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Clown triggerfish',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Crimson rosella',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Demoiselle crane',
      'Australasia Pavilion',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      4,                                                             # Snow resistance (only for animals with outdoor viewing)
      1,1,4,5,5,5,5,5,5,5,4,3,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      1,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Nov',
      '''Demoiselle cranes are most reliably seen from the spring through the fall. They are fairly hardy birds, but will generally
         retreat to shelter in the coldest months.'''.replace( '\n', ' ' ),
      '''The demoiselle cranes are generally more active earlier in the day, when they can often be seen wandering around their habitat,
         foraging for food.'''.replace( '\n', ' ' ),
      '''Demoiselle cranes are native to Central Asia, Eastern Europe, and North Africa. They are famous for their long migrations, where
         they may travel thousands of kilometers between their breeding and winter grounds. They also perform elaborate courtship dances
         to impress potential mates, involving bowing, jumping, and wing-flapping.'''.replace( '\n', ' ' ),                                                          
      '''The Toronto Zoo is home to one male and one female demoiselle crane.'''.replace( '\n', ' ' )
   ),
   (
      'Eastern rosella',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Emerald tree boa',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Fly River turtle',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Green tree python',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Galah',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Green-winged dove',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Komodo dragon',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The Komodo dragons at the zoo are young, and still getting used to their habitat. Most of the time you can find them high in the
         tree in the center of the enclosure. Look closely for a claw, or a dangling tail.'''.replace( '\n', ' ' ),
      '''Komodo dragons are the world's largest lizard. They are also one of only a few venomous lizards. Komodo dragons are found only
         on a few islands in Indonesia, where they hunt large prey items including deer and boar. Komodos can grow to over 100 kg in
         weight.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has two ~4-year-old Komodo dragons which were acquired in November of 2025. They were named by the community--
         the female being named Raya, and the male, Komo. They are still getting used to their new space and thus may be difficult to
         spot. They are also only a fraction of their full-grown size.'''.replace( '\n', ' ' )
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,3,4,5,5,5,5,3,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep (Outdoor), Oct-May (Indoor)',                         # Seasonal VISIBILITY summary
      '''Kookaburras are warm weather birds, and thus are only comfortable outside during the warmer months of the year. In these warmer
         months they can be seen outside in the Australasia outdoor aviary, alongside the demoiselle cranes. In the cooler months they
         can be spotted in their indoor habitat just past the red-tailed black cockatoos.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Kookaburras are a species of kingfisher, and are actually carnivorous, feeding on insects, small mammals, and reptiles. They are
         also known for their distinct laugh-like call, which is used for territorial purposes and communication.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Lau banded iguana',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Live coral reefs',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Longnose butterflyfish',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'MacLeay\'s spectres',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Moon jellyfish',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Nicobar pigeon',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Pennant coral fish',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Pot-bellied seahorse',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red claw yabby',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red-tailed black cockatoo',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Short-beaked echidna',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The short-beaked echidna is perhaps the most difficult animal to spot at the zoo. This is because the species is nocturnal,
         and rarely exits its burrow during the day. Your best chance of spotting the echidna is to visit the Australasia pavilion
         right at the end of the day, and looking around the bottom of the cockatoo enclosure.'''.replace( '\n', ' ' ),
      '''The short-beaked echidna is one of five living species of monotreme, which is a mammal that lays eggs. Although they may
         resemble hedgehogs or porcupines, echidnas are most closely related to the platypus (the only other monotreme). The monotreme
         family has no close relatives, and is believed to have diverged from the marsupial family approximately 200 million years ago.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo has one short-beaked echidna, a female named Annie, who is about 45 years old!'''.replace( '\n', ' ' )
   ),
   (
      'Solomon Island leaf frog',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Southern hairy-nosed wombat',
      'Australasia Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,2,4,5,5,5,5,2,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Sep (Outdoor + Indoor), Oct-Apr (Indoor Only)',           # Seasonal VISIBILITY summary
      '''Wombats are warm weather animals, and tend to only venture outside in the warmer months of the year. They are also generally
         less active in the winter, spending more time sleeping in their burrows. Even in the warmer months, the wombats are often found
         in their indoor habitat in the Australasia Pavilion.'''.replace( '\n', ' ' ),
      '''The wombats are most active closer to dusk or dawn. They spend much of the daytime sleeping, but during these lazy hours they
         are likely to be viewable in their indoor habitat.'''.replace( '\n', ' ' ),
      '''The Southern hairy-nosed wombat is a marsupial, meaning they carry their young in their pouches. A newborn wombat is
         remarkably small, weighing about a gram, and being 2-3 cm in length. The baby develops in the pouch for 6-7 months, as it seeks
         protection from the mother. Wombats also have a backwards-facing pouch to prevent dirt from entering the pouch while digging.
         Wombats can run surprisingly fast at 35-40 km/h, and have reinforced cartilage and bone in their backends protecting them from
         predators.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has a breeding pair of wombats, male Arthur, and female Matilba.'''.replace( '\n', ' ' )
   ),
   (
      'Thorny devil stick insect',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Victoria crowned pigeon',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'White\'s tree frog',
      'Australasia Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),

   # Australasia Outdoor
   (
      'Western grey kangaroo',
      'Australasia Outdoor',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      2,                                                             # Snow resistance (only for animals with outdoor viewing)
      1,1,3,4,5,5,5,5,5,5,4,2,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      1,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Nov',                                                     # Seasonal VISIBILITY summary
      '''The Western grey kangaroo is a fairly hardy species. As long as the temperature is above 0°C and there isn't much snow on the
         ground, they should be viewable outside.'''.replace( '\n', ' ' ),
      '''The kangaroos at the Toronto Zoo have a rather large habitat, meaning that sometimes the animals will be fairly far from the
         guest viewing. The kangaroos are the most active, and the most likely to be closer to the guest viewing early in the morning.
         In the warmer months (approximately Jun-Oct) any guest of the zoo may enter the kangaroo habitat via the kangaroo walkthrough
         from 11:00 am to 3:00 pm, to get an up-close view of these remarkable creatures.'''.replace( '\n', ' ' ),
      '''Kangaroos are the world's largest marsupial. They are native to South and West Australia, where they are rather plentiful.
         Kangaroos are herbivorous, and despite what some people think, they are very docile creatures, and will only attack you if they
         are provoked. Kangaroos have an incredible jump, in which they can cover up to 9 m in one jump.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a group of Western grey kangaroos, called a mob, with several active breeding members.'''
         .replace( '\n', ' ' )
   ),

   # Eurasia Wilds
   (
      'Amur tiger',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary'
      '''While the Amur tigers at the zoo can be viewed year-round, these cats are actually most comfortable when it is cooler, so your
         best chance of seeing them active is in the winter.'''.replace( '\n', ' ' ),
      '''For a year-round, comfortable experience, the tigers at the zoo always have access to indoor and outdoor spaces. Specifically
         when it is warmer, the tiger may be in one of her indoor habitats, past the main habitat and on the left. Amur tigers are most
         active early and late in the day.'''.replace( '\n', ' ' ),
      '''The Amur tiger is the world's largest cat. They are native to North-Eastern Asia, where they are critically endangered. The
         females can get up to 370 lb, while males are much larger, and can reach weights of up to 675 lb. Tigers are solitary, and thus,
         unless they are breeding, or it is a mother and her cubs, you will only ever see one in a habitat at the zoo.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female Amur tiger, Mazy. Mazy is in her golden years, and will spend much of her time resting,
         but you can still see her being active, specifically in the cooler months and earlier in the day, or whenever she is being given
         enrichment. Mazy is past her breeding days, and will remain alone, as she likes it, for the rest of her days at the zoo.'''
         .replace( '\n', ' ' )
   ),
   (
      'Asian wild horse',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -25,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The Asian wild horse (previously known as the Przewalski horse) is the last true surviving species of wild horse. They
         nearly went extinct, but efforts from zoos like Toronto have given the species new hope with several thousand individuals
         being released since their near-extinction. These horses are native to central Asia, and are amazingly well adapted to the
         colder weather. If you see the horses at the zoo in the summer, and then again in the winter, you will notice the dense coats
         they grow for the colder seasons.'''.replace( '\n', ' ' ),
      '''Most of the zoo's horses live in a herd which you can see up close in the Zoomobile Eurasia Wilds, barrier-free drive-thru.
         Several of the zoo's older and 'retired' horses can be viewed in a habitat across from the West Caucasian turs.'''
         .replace( '\n', ' ' )
   ),
   (
      'Bactrian camel',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Bactrian camels are native to Central Asia, where they live in some of the harshest habitats in the world, with temperatures
         ranging from -30°C winters to 40°C summers. These camels have two humps, which store fat and not water, a common misconception.
         Their eyelashes and closable nostrils protect them from sand, dust and snow.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Domestic yak',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Yaks are incredibly well adapted for the cold. Additionally, their large lungs and hearts allow them to thrive in the thin air,
         high up in the mountains. They generally have calm demeanors, and historically have been used to help humans transport goods
         across terrain / in mountainous regions.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Highland cattle',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -25,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Highland cattle are recognized for their thick fur, and droopy hair that covers their eyes. Their fur protects them from bugs
         and the elements. Their long, curved horns are used for defence and social dominance. These cows originate from the Scottish
         highlands, and they have evolved to bear harsh winters, and to survive on rough vegetation diets, composed of grasses and
         shrubs.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two young highland cattle, Blue and Jay, who are named after the Toronto Blue Jays baseball team.
         They are still growing, and love interacting with guests during wild encounters.'''.replace( '\n', ' ' )
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -15,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Mouflon are one of the oldest species of wild sheep in the world. They are believed to be an ancestor of many modern
         species/breeds of sheep. They live in high altitudes in Western Asia and Europe, where they feed on sparse vegetation. They
         are recognized for their colourful grey, brown, and white coats, and their curved horns, grown only by the males.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Red panda',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -10,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''Red pandas are most comfortable in the cooler weather, so visiting them from the fall through the spring will give you the
         best chance to see them active. During the summer months they spend much of their time sleeping high up in the trees. On the
         warmest summer days they may opt to spend their time inside, away from guests.'''.replace( '\n', ' ' ),
      '''Red pandas are most active early and late in the day, so your best chance of seeing them active is to visit their enclosure
         first thing in the morning. Through much of the day they spend their time sleeping way up in the trees. To spot them in their
         exhibit, crank your necks all the way up to the top branches of the tallest trees in their habitat, and look for a couple of
         red-black furry balls.'''.replace( '\n', ' ' ),
      '''Despite their name and appearance, red pandas are not related to pandas nor raccoons. They are the only member of their family.
         Red pandas live in high altitudes in central Asia, primarily China and Nepal. Like their giant counterparts, they feed on
         bamboo, but also berries, fruit, eggs, and insects.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two red pandas, a young female, Poppy, born in 2024, and an older male, Kalden, who came from the
         Edmonton Zoo. Poppy is young and energetic, and can often be spotted zooming around her habitat in the cool mornings. Kalden
         moves at a slower pace, and spends most of his time high up in the trees.'''.replace( '\n', ' ' )
   ),
   (
      'Snow leopard',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''Snow leopards are built for the extreme cold of the Himalayas, and thus are the most active in the winter. During the warmer
         months, they may be active earlier in the day, but they will spend a lot of the day sleeping in the shade, and perhaps away
         from the view of zoo visitors.'''.replace( '\n', ' ' ),
      '''The snow leopards are most active early in the day, especially during the summer months, so your best chance of seeing them
         active is to head to their exhibit first thing in your visit. The snow leopard habitat is designed to mimic the mountainous
         habitats they originate from. They can often be spotted towards the back of the exhibit on top of their rock wall. During the
         warm months of the year, you may walk up the mountain to get a good vantage point of the habitat. They may also lie down in
         front of the glass viewing inside the cave. A couple of other good spots to check are the set of trees across from the West
         Caucasian tur habitat, and in the dip beside the rocks by the viewing nearest to the Steller's sea eagle. Look closely and you
         should be able to spot them.'''.replace( '\n', ' ' ),
      '''Snow leopards are the most elusive species of cat in the world. They are endemic to the Himalayan mountains where they are very
         rarely seen by people. They avoid people when possible. They hunt sheep and goats in these mountains, using ambush techniques,
         made possible by their remarkable stealth. They have very long tails which help them jump incredible distances, up to 9 m.'''
         .replace( '\n', ' ' ),
      '''The zoo is home to four snow leopards: an adult male, Pemba who goes in exhibit by himself on Mondays, Wednesdays, and Fridays,
         and a mother, Jita, and her two female cubs, Minu and Zoya, who are all on exhibit together on Tuesdays, Thursdays, Saturdays,
         and Sundays. The mother and cubs are nearing the end of their time together on exhibit. Once the cubs become too old for their
         mother, they will be moved to other zoos. Snow leopards are solitary animals, except for during breeding season, and a mother
         and her cubs, hence why Pemba goes on exhibit by himself. The snow leopard cubs are quite active, and can often be seen chasing
         each other, or their mother, around the habitat.'''.replace( '\n', ' ' )
   ),
   (
      'Steller\'s sea eagle',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Steller's sea eagles are one of the largest and heaviest species of eagle in the world. They are native to Northeastern coastal
         Asia, where they feed primarily on fish. They also feed on whale carcasses that end up on shore. They have bright yellow beaks,
         and brown and white plumage. Their wingspan can reach up to 8 ft, and they build nests up to 2 m wide.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo has a young breeding pair of Steller's Sea Eagles.'''.replace( '\n', ' ' )
   ),
   (
      'West Caucasian tur',
      'Eurasia Wilds',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -15,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''West Caucasian turs get their name from where they come from--the West Caucasus mountains. They live in altitudes of up to
         3000 m, and are very well adapted to moving through the mountains. They are seasonal feeders, grazing on grasses, during the
         summer, and seeking woody plants and exposed vegetation when the snow covers the grass. The males have noteworthy horns, which
         are curved backwards, and used in clashing rituals.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),

   # Tundra Trek
   (
      'Arctic wolf',
      'Tundra Trek',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The arctic wolf enclosure at the Toronto Zoo is very large, and has many viewing points. To get the best view of the wolves,
         you can move 360° around the habitat which will also take you all the way around the Tundra Trek exhibit, and you should get a
         semi-close view.'''.replace( '\n', ' ' ),
      '''Arctic wolves are a subspecies of the grey wolf that have pure white coats, and are only found around the Arctic Circle. Like
         most canines, arctic wolves are pack animals, and can travel long distances to hunt down their prey.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has a pack of seven arctic wolves. Typically speaking, they move through their exhibit together.'''
         .replace( '\n', ' ' )
   ),
   (
      'Caribou',
      'Tundra Trek',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The caribou exhibit at the zoo is very large, and expands quite far back to the left from the main viewing area. Most of the
         time the caribou can be seen towards the back, right section of the habitat in and around their shelter. Sometimes they may be
         in a part of their habitat across from the flamingo enclosure, so be sure to walk that way and check all along the fence if
         you can't spot them from the Tundra Trek viewing.'''.replace( '\n', ' ' ),
      '''Caribou, which are the same species as the reindeer, are native to arctic and subarctic regions. Caribou have large, splayed
         hooves which allow them to travel across the snow without sinking. In the winter, they dig through the snow, to find lichen,
         also known as 'reindeer moss'.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Lesser snow goose',
      'Tundra Trek',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Lesser snow geese breed in the arctic tundra, but migrate in the winter to the Southern U.S., and Mexico. They have one of the
         longest migration patterns of any bird, usually landing somewhere in the range of 2000-3000 km. Adult geese have purely white
         plumage, while juveniles are grey.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Northern bald eagle',
      'Tundra Trek',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The recovery of bald eagles in North America is one of the greatest conservation stories of our time. In 1964 there were
         approximately 400 breeding pairs, and now there are ~71,000. Banning DDT, and habitat protection initiatives allowed their
         population to grow exponentially. Bald eagles feed on fish and mammals, and are often year-round residents at their nests
         as long as the water bodies they get their food from do not freeze over.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Polar bear',
      'Tundra Trek',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''While visible all year-round, the polar bears at the zoo are far more active during the cooler months. During the summer, they
         are quite lethargic, and spend much of their time resting in the shade. If you want to see the polar bears in their glory
         playing with one another, consider visiting in the winter.'''.replace( '\n', ' ' ),
      '''The polar bears at the zoo have a few different habitats: the maternity yard, the main pool habitat, and the main grass
         habitat. In the warmer months the bears will likely avoid the grass habitat and either spend their time in the pool or in the
         pool habitat and/or the maternity yard in the shade. In the cooler months you are more likely to see bears being active in the
         grass habitat.'''.replace( '\n', ' ' ),
      '''Polar bears are the largest bear species and are also purely carnivorous in the wild. Seals are their most common prey. They
         are also the largest land carnivore. At the zoo, the bears are fed a diet which includes fruit and vegetables. The reasons
         that these bears do not eat any vegetation in the wild is because their arctic habitat does not suit a diet of it, unlike that
         of other bear species. Polar bears' skin is actually black, which helps them absorb heat.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to four polar bears, male Hudson, and females Juno, Aurora, and Nikita. The bears go on display in
         pairs of two.'''.replace( '\n', ' ' )
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,4,5,5,5,5,5,4,2,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct',                                                     # Seasonal VISIBILITY summary
      '''American flamingos are a relatively hardy bird, tolerating temperatures as low as 5°C. They can be seen reliably from May
         through to October, but they can also often be seen on warmer days in March, April, and November.
         *The American flamingos are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.*'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      None,                                                          # General viewing tips
      '''American flamingos are the largest species of flamingo. They get their pink colouration from the carotenoid in their diets.
         Young flamingos have a light grey colouration. In the wild, flamingos live in very large colonies. A group of flamingos is
         called a flamboyance. Flamingos can often be seen standing on one leg. They do this to save energy and prevent muscle fatigue.
         '''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to many American flamingos, including several that are around 50 years old!'''.replace( '\n', ' ' )
   ),
   (
      'Black-handed spider monkey',
      'Americas Outdoor Mayan Temple Ruins',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,2,4,5,5,5,5,3,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Sep',                                                     # Seasonal VISIBILITY summary
      '''Spider monkeys are warm-weather primates, and struggle to be outside in any temperature below 15°C. They can be reliably seen
         from May through September, but even then, on colder days they opt to spend their time inside.
         *The black-handed spider monkeys are part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit
         typically opens for the season sometime in late March or April, and closes sometime in November. For confirmation on whether
         the exhibit is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      '''The spider monkeys often move through the indoor and outdoor habitats in a given day. Check all of their platforms, along the
         back of the exhibit, and above the glass viewing across from the flamingos. If you don't spot them, then they are likely inside
         for the moment. If you are patient, you may see them venture outside.'''.replace( '\n', ' ' ),
      '''Spider monkeys get their name from their long limbs, and their hook-like hands. Spider monkeys are highly arboreal, spending
         the vast majority of their time in the tree canopy. At the zoo, you will likely see them swinging across their exhibit, and
         rarely walking on the ground. The spider monkey's tail acts like a fifth appendage. They can latch their tails onto a branch
         and hang from it that way.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of female black-handed spider monkeys.'''
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,3,4,5,5,5,5,5,4,2,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      '''May-Oct''',
      '''The capybara is a warm-weather animal, and is most reliably seen from May until April. The capybara has a viewing pattern
         similar to the flamingos, and may also be viewable outside on warmer March, April, and November days. On days that aren't too
         warm, the capybara may move between her indoor and outdoor habitats.
         *The capybara is part of the Mayan Temple Ruins exhibit at the zoo, which is a seasonal exhibit. The exhibit typically opens for
         the season sometime in late March or April, and closes sometime in November. For confirmation on whether the exhibit is open,
         consult the Toronto Zoo's official website.'''.replace( '\n', ' ' ).replace( '*', '\n' ),
      None,                                                          # General viewing tips
      '''The capybara is the world's largest rodent. They are endemic to South America. They often live in large social groups, but can
         also live independently. They are also excellent swimmers, and their eyes, ears and nostrils are placed high on their bodies to
         allow them to remain mostly submerged when in the water.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a female capybara, Tootsie, who came from the San Diego Zoo.'''.replace( '\n', ' ' )
   ),

   # Americas Pavilion
   (
      'American alligator',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''American alligators are one of the largest reptiles in North America. Their range consists of the Southeastern part of the U.S.,
         extending as far West as Texas, and as far North as North Carolina. They can be told apart from their crocodile counterparts
         by the shape of their snout. Alligators have a more U-shaped snout, while crocodiles have a more V-shaped snout. Crocodiles are
         also significantly more aggressive than alligators. Alligators, unlike crocodiles, have barely evolved, and have been around
         for hundreds of millions of years, because their 'ambush' strategy for hunting is so effective.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'American eel',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'American lobster',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The axolotl is one of the rarest species in the world, found only in the lakes and canals around Mexico City. Axolotls are a
         species of amphibian, and unlike most amphibians, axolotls keep their external gills throughout their entire lives.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Black-footed ferret',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Black-footed ferrets were believed to be extinct in the wild, until they were rediscovered in Wyoming in 1981. At one point
         there were only a few dozen individuals in the world, but conservation efforts have helped their numbers rebound in the
         hundreds. The diet of the black-footed ferret comprises almost entirely of prairie dogs, accounting for over 90%.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Black-widow spider',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Blanding\'s turtle',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The story of the blanding's turtle is one of the great conservation stories of the Toronto Zoo. Since being declared
         functionally extinct in the Rouge valley, the zoo has bred and released many hundreds of individuals.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Blue and yellow macaw',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The blue and gold macaw is one of the most recognizable species of parrot in the world. They are native to South America where
         they inhabit rainforests, river edges, and open woodlands. They are incredibly intelligent birds, and have been recorded using
         tools to solve problems. They also form lifelong pair bonds in the wild.'''.replace( '\n', ' ' ),
      '''The macaws at the zoo are rescues, and were previously kept as pets, and thus their wings are clipped and they cannot fly.'''
         .replace( '\n', ' ' )
   ),
   (
      'Blue poison dart frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Boa constrictor',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Brazilian giant cockroach',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Brazilian salmon pink bird-eating tarantula',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Butterfly goodied',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Crested tinamou',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Cuvier\'s smooth-fronted caiman',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Cuvier's smooth-fronted caiman is the smallest species of caiman, and one of the smallest species of crocodilian in the world.
         This species is more terrestrial than other species. These caimans are primarily nocturnal, becoming active at night to hunt.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Desert grassland whiptail',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''This species is parthenogenetic, which means they can reproduce without males. The females lay eggs, which develop into
         genetically-identical offspring.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Dyeing poison dart frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Eastern loggerhead shrike',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Eastern lubber grasshopper',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Eyelash viper',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Ferocious water bug',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Golden lion tamarin',
      'Americas Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      18,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,3,5,5,5,5,3,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep (Outdoor + Indoor), Oct-May (Indoor Only)',           # Seasonal VISIBILITY summary
      '''Golden lion tamarins are a species native to the tropical rainforests of South America, and can only be outside during the
         warmest months of the year. Even on these days, these little monkeys may opt to spend their time in their indoor habitat.'''
         .replace( '\n', ' ' ),
      '''The golden lion tamarin outdoor viewing is located right near the boardwalk that connects the Americas to Africa. If you don't
         see the monkeys in any of these enclosures, head inside the Americas Pavilion and you can spot them inside in the primate wing,
         just past the macaws.'''.replace( '\n', ' ' ),
      '''Golden lion tamarins get their name from their bright gold fur, and their lion-like manes. These tamarins are highly social,
         living in groups of 2-8 individuals, cooperating to care for young, and forage for food. Golden lion tamarins are highly
         arboreal, and will rarely go to the rainforest floor in the wild.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Great-horned owl',
      'Americas Pavilion',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The great-horned owl is one of the largest species of owl in North America. They are easily recognized by the tufts on top of
         their heads, and their bright yellow eyes. They hunt at night, and their prey includes rabbits, squirrels, skunks, birds, and
         reptiles.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Green and black poison dart frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Green surf anemone',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Green-winged macaw',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Green-winged macaws are an iconic species of parrot, identified through their red, green, and blue plumage, and the white
         colouring on their faces. They are social and live in pairs or small groups. In zoos, they have been known to interact with
         their caretakers and form bonds. Their beaks allow them to crack open nuts and fruits which many other birds cannot.'''
         .replace( '\n', ' ' ),
      '''The macaws at the zoo are rescues, and were previously kept as pets, and thus their wings are clipped and they cannot fly.'''
         .replace( '\n', ' ' )
   ),
   (
      'Guatamalan beaded lizard',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Jamaican boa',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Leather sea star',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Lemur leaf frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Longnose dace',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Massasauga rattlesnake',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Midland painted turtle',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'North American river otter',
      'Americas Pavilion',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      5,5,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      5,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The North American river otters are a highly active species, and can be usually seen swimming around their water feature
         during the day. You can watch them swim around from above, at the outdoor viewing, or venture inside the pavilion to their
         underwater viewing to get a more up-close view. If you don't spot them playing in the water, they may be taking a rest,
         either in their indoor habitat, which can be viewed from inside the pavilion, or in one of their toys in their outdoor habitat.
         '''.replace( '\n', ' ' ),
      '''The North-American river otter is a semi-aquatic species of mustelid. They are carnivorous and do most of their hunting in the
         water, feeding on fish, amphibians, and crustaceans. They have a wide habitat across North America, spanning from Canada down to
         Mexico. Their fur is insulated, which allows them to be outside at the zoo, exploring the water year-round. They are highly
         social, and enjoy one-another's company.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of North American river otters, a younger female Maybelle, and an older male, RJ. Maybelle
         arrived from the Calgary Zoo as a companion for RJ. They can often be spotted swimming around together, but if you see one otter
         being active, and the other not, it is likely that RJ is the one needing a rest.'''.replace( '\n', ' ' )
   ),
   (
      'Opal-rumped tanagar',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Painted anemone',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Panamanian golden frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Plumose anemone',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Plush-crested jay',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Puerto Rican crested toad',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Pumpkinseed sunfish',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red Island bird-eating tarantula',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red-crested finch',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Reticulate gila monster',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Round goby',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Rufous-collared sparrow',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'San-Esteban Island chuckwalla',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Snapping turtle',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Spot prawn',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Spotted river stingray',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Spotted turtle',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Timber rattlesnake',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Turquoise tanager',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Two-toed sloth',
      'Americas Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,2,4,5,5,5,5,3,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Sep (Outdoor + Indoor), Oct-Apr (Indoor Only)',           # Seasonal VISIBILITY summary
      '''The two-toed sloth is endemic to the rainforests of South America, and is suited to be outside in the warm weather. You have
         a good chance of spotting them outside through May into September, with a chance as well on warm days in April or October. Even
         on warm days, the sloths opt to spend their time inside. During the cooler months, they can always be spotted inside.'''
         .replace( '\n', ' ' ),
      '''The outdoor enclosure for the two-toed sloth is located near the boardwalk connecting the Americas to Africa. If you don't spot
         the sloths outside, you can see them in the primate wing of the Americas Pavilion, just past the macaws.'''
         .replace( '\n', ' ' ),
      '''The two-toed sloth is an arboreal animal, which lives high in the tree canopies in the tropical forests of South and Central
         America. They use their two claws to hang from tree branches. Sloths are herbivorous and solitary. Their fur serves as a mini-
         ecosystem for algae, insects, and fungi. Surprisingly, sloths are good swimmers, using their long arms to paddle.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo has two female two-toed sloths, and younger sloth Sally, and an older sloth, Netta.'''.replace( '\n', ' ' )
   ),
   (
      'Western blacknose dace',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'White-faced saki',
      'Americas Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      12,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,2,4,5,5,5,5,3,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      '''May-Sep (Outdoor + Indoor), Oct-Apr (Indoor Only)''',       # Seasonal VISIBILITY summary''
      '''White-faced sakis are warm weather primates, and are only comfortable outside in the warmer months. They are frequently spotted
         outdoors from May through September, but may also venture outside on other warmer days.'''.replace( '\n', ' ' ),
      '''The outdoor habitat for the white-faced saki is near the boardwalk connecting the Americas to Africa. If you don't spot them
         outdoors, enter the Americas Pavilion and go past the macaws to the primate wing, where they should be viewable.'''
         .replace( '\n', ' ' ),
      '''White-faced sakis are a small, arboreal species of primate endemic to the rainforests of Northern South America. These monkeys
         are social, but only live in small groups with 2-5 individuals. They are named for the white fur on the males' faces. Males are
         black in colour with the white face, while females are covered in a dark greyish-brown fur. White-faced sakis have strong jaws
         used to crack open seeds, which many other monkeys cannot.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female white-faced saki, Cora.'''.replace( '\n', ' ' )
   ),
   (
      'Yellow-banded poison dart frog',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Zebra finch',
      'Americas Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),

   # Canadian Domain
   (
      'Cougar',
      'Canadian Domain',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      -20,                                                           # Minimum temperature (only for animals with outdoor viewing)
      4,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Dec',                                                     # Seasonal VISIBILITY summary
      '''The cougar is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom of
         the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March. To
         check whether the domain is open, consult the Toronto Zoo's official website. Cougars thrive in all seasons, and if the domain
         is open, then the cougar will be viewable.'''.replace( '\n', ' ' ),
      '''The cougars at the zoo have access to a behind-the-scenes indoor habitat which they often spend time in. The cougars are fairly
         interested in zoo guests, and thus if you don't see them right away, but wait for a few minutes, you may get a close encounter
         with one of them. Also be sure to check for them inside their cave in the back right corner of the habitat, on top of all of
         the platforms, and along the fence on the left side of the exhibit.'''.replace( '\n', ' ' ),
      '''Cougars go by many different names--mountain lion, puma, Florida panther, and of course, cougar. Cougars are found all
         throughout the Americas. In Canada, they are usually called cougars. People in the U.S. refer to them as mountain lions most
         often, except in Florida where they are called Florida panthers, and in South and Central America they are called pumas.
         Living across such a wide range, cougars are adapted to live in a variety of habitats, including woodlands, rainforests, and
         alpines. They are carnivorous and can hunt large ungulates like deer, and young moose and caribou. Cougars are solitary and
         cannot roar. They instead purr, hiss, and growl.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two cougars--a male, Bowen, and a female Teeka. They are on exhibit together for companionship.'''
         .replace( '\n', ' ' )
   ),
   (
      'Grizzly bear',
      'Canadian Domain',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,5,5,5,5,5,5,4,2,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Apr-Oct',                                                     # Seasonal VISIBILITY summary
      '''The grizzly bear is viewable seasonably due to its hibernating patterns. Grizzly bears hibernate from sometime in November,
         usually until sometime in March, depending on the exact weather conditions of that year. Leading up to and coming out of
         hibernation, grizzly bears spend more of their time resting, and thus the bears at the zoo may be less visible as they spend
         more of their time resting off-display. The grizzly bear can usually be spotted on exhibit from April through October. 
         *The grizzly bear is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the
         bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in
         March. To check whether the domain is open, consult the Toronto Zoo's official website.'''.replace( '\n', ' ' )
         .replace( '*', '\n' ),
      '''The grizzly bear at the Toronto Zoo, Shintay, is in her golden years and may choose to spend some of her time behind the scenes.
         She can often be seen resting in the shade near the viewing areas of the exhibit, or by peering through the bars into her
         behind-the-scenes area. She is most active during wild encounters, where she will forage around her habitat, enjoying a variety
         of foods which she retrieves by performing enrichment activities.'''.replace( '\n', ' ' ),
      '''Grizzly bears are one of the largest bear species. They are found in Western Canada, and in Alaska, Wyoming, Montana, and
         Washington. The males are significantly larger than the females, and can get up to 1300 lb in weight. They are omnivorous and
         feed on mammals, fish, berries, and roots, to name a few. Grizzly bears are solitary except during mating season, and a mother
         with her cubs. Grizzly bears are very fast for their size, reaching speeds of up to 56 km/h. Grizzlies hibernate during the
         winter months in a state called torpor, from which they may wake up occasionally and exit their den.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one elderly grizzly bear, Shintay. Shintay is in her golden years and spends much of her time
         resting. Your best chance of seeing her active is to visit her habitat during a wild encounter.'''.replace( '\n', ' ' )
   ),
   (
      'Northern bald eagle',
      'Canadian Domain',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      -30,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Dec',                                                     # Seasonal VISIBILITY summary
      '''The Northern bald eagle is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at
         the bottom of the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime
         in March. To check whether the domain is open, consult the Toronto Zoo's official website. If the domain is open, then the
         Northern bald eagle will be viewable. Additionally, this species is viewable year-round in the Tundra Trek.'''
         .replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''The recovery of bald eagles in North America is one of the greatest conservation stories of our time. In 1964 there were
         approximately 400 breeding pairs, and now there ~71,000. Banning DDT and habitat protection initiatives allowed their
         population to grow exponentially. Bald eagles feed on fish and mammals, and are often year-round residents at their nests
         as long as the water bodies they get their food from do not freeze over.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Raccoon',
      'Canadian Domain',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      -35,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Dec',                                                     # Seasonal VISIBILITY summary
      '''The raccoon is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom of
         the Rouge Valley, and for the safety of guests, the domain closes from about the start of January until sometime in March. To
         check whether the domain is open, consult the Toronto Zoo's official website. If the domain is open, then the raccoon will be
         viewable.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Wood bison',
      'Canadian Domain',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      -40,                                                           # Minimum temperature (only for animals with outdoor viewing)
      5,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,5,5,5,5,5,5,5,5,5,5,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Dec',                                                     # Seasonal VISIBILITY summary
      '''The wood bison is part of the Canadian Domain exhibit at the zoo, which is open seasonally. The domain is located at the bottom
         of the Rouge Valley, and for the safety of guests, the domain closes from about the start of Jaunary until sometime in March.
         To check whether the domain is open, consult the Toronto Zoo's official website. If the domain is open, then the wood bison
         will be viewable.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
         '''The wood bison is the largest land animal in North America, slightly edging out the plains bison. Adult males can weigh up to
         2200 lb. Bison calves are born a reddish-brown colour, and gain the shaggy, multi-coloured fur as they age. Bison grow their
         coats in the winter to survive the harsh conditions of Northern Canada, and Alaska, where the originate from, and shed it in
         the summer to stay cooler. Bison are highly social and remarkably fast, reaching speeds of up to 60 km/h.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two groups of bison. The males are located in a paddock on the way down the hill, across from the
         cougars, and the females are located at the bottom of the hill, just past the bald eagle.'''.replace( '\n', ' ' )
   ),

   # Africa Savanna
   (
      'African lion',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      3,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The African lions are more or less viewable year round. During the den of winter they are given access to indoor spaces so
         they may decide to be inside if it is particularly cold or icy. In the winter, they are most often seen in their den, since
         this space is heated. You have the best chance of spotting the lions being active by visiting on a cooler day in the spring or
         fall.'''.replace( '\n', ' ' ),
      '''The lions are one of the most lethargic species at the zoo. They spend much of their time sleeping in the back of their
         habitat, above the underground viewing. Your best chance to see them active is to visit their exhibit first thing in the
         morning.'''.replace( '\n', ' ' ),
      '''Lions are the second largest cat, and the only social cat. They live in large groups called prides led by one dominant male.
         The females do the hunting in the prides. Male lions are identified by their large manes which exist for protection when males
         fight over territory, or for the control of a pride. White lions are the same species as 'regular', tawny lions. They simply
         get their white fur from a genetic mutation.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two female, white African lions named Lemon and Makali.'''.replace( '\n', ' ' )
   ),
   (
      'African penguin',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,4,5,5,5,5,5,5,3,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Apr-Nov (Outdoor + Indoor), Dec-Mar (Indoor Only)',           # Seasonal VISIBILITY summary
      '''African penguins are adapted to handle temperate climates, and thus can be seen outdoors for most of the year. They should be
         viewable on any day between April and November where the temperature is above 0°C and there is no snow on the ground. They may
         additionally be viewable on some days in March. From December to February and parts of March and April, they can be seen
         exclusively in their indoor habitat.'''.replace( '\n', ' ' ),
      '''Even on warmer days many of the penguins may choose to spend their time indoors. Many of the penguins also enjoy being in shade
         along the back of their exhibit among the trees or in between the rocks. They are most likely to be swimming on temperate days.
         '''.replace( '\n', ' ' ),
      '''African penguins have mixed black and white plumage, and are native to the Southwestern coast of Africa, specifically along
         South African and Nambia. They form large colonies along the coast, and also create monogamous bonds. They nest in burrows,
         rocks, and among vegetation to protect their eggs from predators.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Cheetah',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      3,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The cheetahs are on exhibit year-round. In the coldest months of the year they are given access to indoor spaces, so on very
         cold and/or icy days they may decide to spend their time inside. They are most active on cooler days in the fall and spring.
         ''',
      '''Most of the time, the cheetahs can be seen in the back right part of their enclosure. Look for a head just past the trees. Your
         best chance to see the cheetahs active is early in the day,'''.replace( '\n', ' ' ),
      '''Cheetahs are not considered one of the big cats. They are significantly smaller than lions, tigers, jaguars and leopards, and
         they cannot roar. Cheetahs can be distinguished from the other larger spotted cats, jaguars and leopards, through their smaller
         size, solid black spots, and their facial markings used to protect their eyes from the sun, which some athletes have adopted.
         Adult cheetahs are generally solitary, but sometimes males form a coalition to become more formidable.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a number of cheetahs, but there are only ever one or two on exhibit together.'''
         .replace( '\n', ' ' )
   ),
   (
      'Common eland',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      2,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,4,5,5,5,5,5,5,3,1,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Apr-Nov',                                                     # Seasonal VISIBILITY summary
      '''Elands are one of the most-cold resistant antelopes, and can be seen outside during most months of the year through April into
         November. They may also be viewable on warmer March days where there is no snow on the ground, as they are not adapted to walk
         in it.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''The common eland is the largest species of antelope in Africa. The males are larger than the females and can weigh up to
         2200 lb. They are herbivorous and social, living in groups that can range in size from a few individuals, up to around 100.
         Elands have loose skin around the necks to regulate their body temperatures. They can also survive on very little water, getting
         most of it from moisture in the vegetation they eat.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Greater kudu',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,3,5,5,5,5,5,4,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct',                                                     # Seasonal VISIBILITY summary
      '''Kudu are a warm weather antelope with little protection from the cold, and thus they are generally only viewable during the
         warmer months of the year. They can generally be viewed from May until October, and perhaps also on other warm days in spring
         or fall.'''.replace( '\n', ' ' ),
      '''The kudu habitat at the zoo is large and has several different viewing points. The kudu tend to move across their habitat and
         thus the best spot to view them changes from visit to visit. The three viewing points to check are the savanna outlook in the
         African Rainforest Pavilion near the meerkats, the path offshoot between the hippos and white rhinos, and the main viewing
         area across from the white rhinos.'''.replace( '\n', ' ' ),
      '''Greater kudus are medium-sized species of antelope native to Eastern and Southern Africa. The males can be told apart from the
         females via their large spiral horns which can grow up to 6 ft in length. Kudu are considered to be very shy and elusive, with
         the females and juveniles generally forming their own groups, and the males being more solitary.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to three female greater kudu, which all go out on exhibit together.'''.replace( '\n', ' ' )
   ),
   (
      'Grevy\'s zebra',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      1,                                                             # Snow resistance (only for animals with outdoor viewing)
      1,1,3,5,5,5,5,5,5,5,4,2,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      1,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Nov',                                                     # Seasonal VISIBILITY summary
      '''Grevy's zebras are a very hardy species, tolerating temperatures around freezing. They are generally viewable outside from
         ealrly Spring through to the start of winter. On a lot of warmer winter days they would be able to go outside if not for the
         snow/ice on the ground. Zebras have no adaptation to allow them to move across the snow, and if one were to fall, it could be
         life-threatening.'''.replace( '\n', ' ' ),
      '''The zebra exhibit is very long and has a very different viewing points. The best spot to see them is usually across from the
         glass viewing area from which the cheetahs and baboons can both be seen. The zebras tend to move across their habitat quite a
         lot as they graze, so you may have to wait to get the best view.'''.replace( '\n', ' ' ),
      '''Grevy's zebras are the largest species of zebra. They are native to arid regions, and can survive on little water. They are
         more predominantly white than other zebras, having thinner black stripes, white bellies, and not having black snouts. Their
         social structures are also more fluid. Typically, they comprise of fewer individuals, and the males are relatively solitary,
         usually only interacting with females for breeding.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to five grevy's zebras, including some males and some females. They never all go out on exhibit
         together. If you see one zebra on its own, it is likely one of the males. If you see several zebras together, it is likely to
         be the females, but sometimes a male will be on exhibit with the females, particularly for breeding purposes.'''
         .replace( '\n', ' ' )
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,3,5,5,5,5,2,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep',                                                     # Seasonal VISIBILITY summary
      '''Marabou storks are a warm weather bird and can only go on exhibit in the warmer months, particularly from June to September,
         but perhaps longer than that, depending on the specific weather.'''.replace( '\n', ' ' ),
      '''There are a couple different spots to spot the marabou storks. They go on exhibit with the kudu and can be spotted in that
         exhibit. You may see them from any of the three viewings, at the savanna overlook in the African Rainforest Pavilion by the
         meerkats, on the offshoot between the hippos and rhinos, or at the main viewing across from the white rhinos. You may have the
         most success on the offshoot path between the hippos and rhinos. The other spot to see them is by the zebra enclosure, roughly
         across from the main cheetah viewing.'''.replace( '\n', ' ' ),
      '''Marabou storks are large wadding birds native to sub-Saharan Africa. They are recognized for their bald heads, and are often
         considered quite an ugly bird. They are quite an important part of the ecosystem, feeding on carcasses and carrion.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Masai giraffe',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,3,5,5,5,5,5,4,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct (Outdoor), Nov-Apr (Indoor)',                         # Winter VISIBILITY (only for animals with outdoor viewing)
      '''Masai giraffes are warm-weather animals and have little protection against the cold. They can usually be seen outside from May
         until October and on other days above 10°C. If you don't see them outside, you can stop by the giraffe house, right beside
         their outdoor habitat and see them inside.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Masai giraffes are the tallest subspecies of giraffe, with the males being able to reach heights of up to 6 m/19 ft. Being the
         tallest animal on the serengeti, giraffes are usually the first animal to spot approaching predators. For this reason, many
         other species stay nearby giraffes so that they know when predators are approaching. Despite their incredible length, giraffes'
         necks actually have the same number of vertebrae as our own--seven. Giraffes sleep very little--approximately two hours in one
         day, and do so while standing up.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female Masai giraffe, Mstari, who is currently pregnant. She is expected to give birth sometime
         from late February into March. Giraffes' gestation period is around 15 months, and when they give birth, they do so standing up
         with the calves dropping right to the ground. Newborn giraffes are already around 6 ft in height.'''.replace( '\n', ' ' )
   ),
   (
      'Olive baboon',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      4,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The olive baboons can generally be seen year-round. In the coldest months they may be given access to indoor spaces, but they
         can generally be seen outside, most often on their main structure in the center of their enclosure.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Baboons are a large and powerful primate native to much of Africa. They live in large groups, and are very ferocious and
         territorial. They regularly fight off large predators like leopards and lions. This species of baboons is identified by their
         brownish fur, dog-like snout, and expressive faces. Baboon troops have complicated social structures with individuals forming
         strong bonds through grooming and play.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Ostrich',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      1,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,3,5,5,5,5,5,5,5,3,1,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Mar-Nov',                                                     # Seasonal VISIBILITY summary
      '''Ostriches are quite adaptive birds, comfortable in temperatures down to around 0°C. They can be fairly reliably seen between
         March and November, minus any freezing days, or days where there is much snow on the ground.'''.replace( '\n', ' ' ),
      '''The ostrich habitat has two main vantage points. One is between the lions and the baboons, while the other is across from the
         top of the hill that yields access to the Canadian domain. The ostrich moves across its enclosure quite regularly.'''
         .replace( '\n', ' ' ),
      '''Ostriches are the world's largest bird, standing up to 9 ft tall. Ostriches are endemic to Africa where they live in savannas,
         grasslands, and semi-deserts. Ostriches can run up to 70 km/h, and take strides of up to 5 m. They have very powerful kicks,
         which are used to defend themselves from predators. Male ostriches have black and white feathers, while the females are
         covered in greyish-brown feathers.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a male ostrich, Omelette, who loves to dance and interact with his caretakers.'''.replace( '\n', ' ' )
   ),
   (
      'River hippopotamus',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,2,5,5,5,5,5,3,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct',                                                     # Seasonal VISIBILITY summary
      '''River hippos are native to sub-Saharan African and have exposed skin, and are thus not very adapted to the cold. At the zoo,
         they can be seen outside reliably from May through the warmer part of October, and occasionally on other warm spring and fall
         days.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''River hippos are the third largest land mammal behind rhinos and elephants. They are known for being highly territorial and
         aggresisve, but they are actually herbivorous. Hippos live in large groups and spend most of their time in the water with only
         their ears, eyes, and nostrils above the surface. Despite all the time they spend in the water, technically, they cannot swim.
         They move through the water by walking on the bottom, and pushing themselves against the river's edge.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female river hippopotamus, Perky.'''.replace( '\n', ' ' )
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,3,5,5,5,5,2,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep',                                                     # Seasonal VISIBILITY summary
      '''Southern ground hornbills are warm-weather birds which are usually only viewable during the warmest months of the year.'''
         .replace( '\n', ' ' ),
      '''Southern ground hornbills can be spotted in two habitats at the zoo. Some of them share a habitat with the kudus and other
         savanna birds. They can be viewed in this habitat from any of the three viewings: the savanna outlook in the African Rainforest
         pavilion near the meerkats, on the offshoot path between the rhinos and hippos, or in the main viewing across from the white
         rhinos, but they may be most reliably seen at the viewing on the offshoot path. The other spot that they can be viewed is in
         the small enclosure between the lions and hyenas, and across from the elands.'''.replace( '\n', ' ' ),
      '''The Southern ground hornbill is one of the largest hornbill species in the world, and is unique for how it walks on the ground
         instead of flying around. These hornbills are carnivorous, feeding on small mammals, insects, and snakes. They hunt by walking
         slowly, scanning around for the prey, and lunging at it with their powerful beaks.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Southern white rhinoceros',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,3,5,5,5,5,5,4,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct',                                                     # Seasonal VISIBILITY summary
      '''Southern white rhinoceroses are warm-weather animals and have exposed skin, and are only viewable outside during the warmer
         months of the year. They can be reliably seen from May through October, and on other warm spring or fall days.'''
         .replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Southern white rhinos are the second largest land mammal behind elephants, and they are the largest and heaviest species at the
         zoo. Rhinos are social animals, and live in colonies called crashes. They have poor eyesight, but they are very fast. These
         rhinos have two horns, with the front one being longer, wheras Asian species of rhinos have just one. The other species of
         African rhino is the black rhino. White rhinos can be distinguished from black rhinos through their lighter pigmentation, and
         their wider snouts. White rhinos actually got their name from a mistranslation of the word 'wide'.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to four Southern white rhinoceros. There is an adult male, Tom, adult females Sabi and Zohari, and
         youngster Kifaru. Kifaru is a male and was born in December of 2023. Sabi, Zohari, and Kifaru all go on exhibit together, while
         Tom is solitary.'''.replace( '\n', ' ' )
   ),
   (
      'Spotted hyena',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      3,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The spotted hyenas can generally be seen year-round, but during the coldest months they may be given indoor spaces, and decide
         to spend their time inside, specifically on the coldest and snowiest day. On the coldest days, look for them in their den,
         viewable from the glass viewing across from the watusi, which is heated.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Despite their dog-like appearance, hyenas are more closely related to cats. Physically, hyenas are like a stronger, stockier,
         more aggressive wolf. Like wolves, they also live in groups called clans. While many believe them to be scavengers, they are
         also quite effective hunters. They prey on medium-large animals like wildebeest, zebras, and antelope. Hyenas also have one
         of the strongest bites of any land animal, allowing them to crush bones and eat every part of a carcass.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to several hyenas. Unlike their wild counterparts, the hyenas at the zoo are solitary, and thus you
         will only ever see one on exhibit at a time.'''.replace( '\n', ' ' )
   ),
   (
      'Warthog',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,3,5,5,5,5,2,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep',                                                     # Seasonal VISIBILITY summary
      '''Warthogs are very sensitive to the cold, and thus are only viewable outside during the warmest months, June to September, and
         on other warm days.'''.replace( '\n', ' ' ),
      '''The warthogs can most often be seen by looking directly down from their viewing. One of the warthogs at the zoo likes to rest
         right near the close fence of the enclosure.'''.replace( '\n', ' ' ),
      '''The warthog is a member of the pig family, known for their large tusks and facial warts. Warthogs are also quite agile and
         fast. Warthogs often kneel on the ground as they graze. When startled, warthogs run with their tails up, which serves as a 
         signal for other warthogs to get out. Warthogs use abandoned burrows, usually made by other animals such as aardvarks, for
         shelter and protection.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Watusi cattle',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      2,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The watusi cattle can generally be seen outside year-round, as they have been bred to have a very high tolerance against the
         cold. On the iciest days, they may opt to stay inside as they need to move around a lot each day to graze.'''
         .replace( '\n', ' ' ),
      '''These cattle are most well-known for their large horns, which can be up to 8 ft in length from tip to tip. Despite their
         appearance, these horns are actually quite light, and hollow. They contain air vessels and are used to regulate the cattle's
         body temperature.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'White-breasted cormorant',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      0,                                                             # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,4,5,5,5,5,5,5,3,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Apr-Nov (Outdoor + Indoor), Dec-Mar (Indoor Only)',           # Seasonal VISIBILITY summary
      '''The white-breasted cormorant can handle temperate environments, and can thus be outside for most of the year, but cannot handle
         snow or ice. During the coldest months, from December through most of March, these birds are only visible indoors. When
         weather permits, this bird can normally be seen outside by the water's edge in the African penguin habitat.'''
         .replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'White-headed vulture',
      'Africa Savanna',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      15,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,3,5,5,5,5,2,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Jun-Sep',                                                     # Seasonal VISIBILITY summary
      '''The white-headed vulture is a warm-weather bird which can only be seen outside during the warmest months, and on other very
         warm days.'''.replace( '\n', ' ' ),
      '''The zoo is home to one white-headed vulture, Lloyd, and he is one of the more reclusive residents. He resides in the enclosure
         with the kudu and other savanna birds. He may be spotted from any of the three viewing areas for this exhibit: the savanna
         outlook in the African Rainforest Pavilion near the meerkats, on the offshoot path between the hippos and rhinos, or at the
         main viewing across from the white rhinos, but you will have the best chance at the offshoot viewing followed by the main
         viewing area.'''.replace( '\n', ' ' ),
      '''White-headed vultures get their name from their snow-white necks and heads. They also have a light pinkish beak. Unlike many
         other vulture species which are usually seen in large flocks, white-headed vultures are often seen alone or in pairs. Like
         other species, these vultures are scavengers, and feed primarily on carcasses left by other animals.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one white-headed vulture, a male named Lloyd. Lloyd is one of just two white-headed vultures in
         North America.'''.replace( '\n', ' ' )
   ),

   # African Rainforest Pavilion
   (
      'African clawed frog',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
   ),
   (
      'African spoonbill',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Aldabra tortoise',
      'African Rainforest Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      20,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,0,1,3,4,4,3,1,0,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      '''Jul-Aug (Outdoor), Sep-Jun (Indoor)''',                     # Seasonal VISIBILITY summary
      '''The Aldabra tortoises only thrive in very warm weather and thus can only be reliably seen outdoors in the peak of summer,
         during July and August, and other very warm days. The rest of the time they can be seen inside the African Rainforest pavilion
         in their shared habitat with the ring-tailed lemurs and the grey-necked crowned cranes.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''Aldabra tortoises are one of the largest species of tortoises, weighing up to 550 lb and living over 100 years. These
         tortoises are very calm and docile, and they live in small groups.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to two female Aldabra tortoises Queenie and Malila, who returned to the zoo in 2018. They originally
         arrived at the zoo in 1976. They are currently estimated to be between 50 and 60 years old.'''.replace( '\n', ' ' )
   ),
   (
      'Black crake',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Blue-bellied roller',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Grey-necked crowned crane',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The grey-necked crowned crane is known for the golden features on the top of its head, and its multi-coloured plumage. Both
         the males and females have grey, white, and black feathers. These birds are diurnal and feed on insects, reptiles, seeds, and
         plants.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Lake Malawi cichlids',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Lau banded iguana',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Naked mole rat',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Nile soft-shelled turtle',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''This turtle has a soft, leathery shell, unlike the hard, boney ones which most others have. This soft shell helps them move
         through the water, where they spend most of their time. These turtles are carnivorous, using an ambush technique, and feeding
         on animals including fish, amphibians, crustaceans, and small birds and mammals when they come near the water.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Pygmy hippopotamus',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''Pygmy hippos are significantly smaller, more timid, and less social than their counterparts. Unlike river hippos, pgymy hippos
         are mostly solitary, except for during breeding season, and a mother and her offspring. Pygmy hippos live in rainforests, as
         opposed to river hippos which live in water bodies in savannas and grasslands. Pygmy hippos are also nocturnal, feeding on
         leaves, fruits, and ferns during the night.'''.replace( '\n', ' ' ),
      '''The zoo is home to a breeding pair of pygmy hippos, a male Harvey and a female Kindia. Unless they are being put together for
         breeding, they can each be seen in on of their two habitats in the African Rainforest Pavilion.'''.replace( '\n', ' ' )
   ),
   (
      'Red-footed tortoise',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red river hog',
      'African Rainforest Pavilion',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      0,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      5,                                                             # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,2,4,5,5,5,5,5,5,3,1,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Apr-Nov',                                                     # Seasonal VISIBILITY summary
      '''Red river hogs do surprisingly well in cooler temperatures can usually be seen outside from April until November.'''
         .replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''The red river hog is a medium-sized pig endemic to Central and Western African where it lives in forests, savannas and
         woodlands. This species is identified by its yellowish-brown body, elaborate snout, and tufted ears. Like other pig species,
         red river hogs are omnivorous and will occasionally feed on small animals and carrion. Red river hogs have powerful senses of
         smell, and noses used to uncover food below the surface. They are social and generally live in groups of 6-10 individuals.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Ring-tailed lemur',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The ring-tailed lemur gets its name from the alternating black and white rings on its tail. Being a species of lemur, these
         primates are found exclusively on the island of Madagascar. Lemurs generally have their tails lifted upwards. This mechanism
         serves as a flag to keep to the group together as they move across the forest floor, which they do quite often since they are
         much more terrestrial than other lemur species. Lemurs are actually not monkeys, but rather prosimians. Prosimians are
         generally considered to be the earliest order of primates, making lemurs a more primitive version of monkeys.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Royal python',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Sacred ibis',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Slender-tailed meerkat',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The slender-tailed meerkat is a small species of mongoose native to the savannas and semi-desert regions of Southern Africa.
         They are known for standing on their rear legs, which they do on lookout as they watch for predators. Meerkats live in large
         family groups called mobs or clans. These groups use strong social collaboration, where they share the tasks of babysitting
         and sentinel behaviour. They also create burrows which they use for protection from the heat and predators.'''
         .replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'South African shelduck',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Speckled mousebird',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Straw coloured fruit bat',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Veiled chameleon',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'West African dwarf crocodile',
      'African Rainforest Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The West African dwarf crocodile is the smallest species of crocodile in Africa. They can grow up to 5-6 ft, and are very
         stocky, and heavily armoured. Unlike many other species of crocodile, West African dwarf crocodiles are pimarily nocturnal, 
         spending daylight hours hiding under vegetation and in burrows. Females build nests near the water and lay 10-30 eggs, which
         they guard fiercly until they hatch.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Western lowland gorilla',
      'African Rainforest Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,3,5,5,5,5,5,4,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct (Outdoor + Indoor), Nov-Apr (Indoor Only)',           # Seasonal VISIBILITY summary
      '''Western lowland gorillas are warm weather primates and are only comfortable outside during the warmer months of the year,
         usually from May to October, and perhaps on other warmer days, specifically in the later part of April.'''.replace( '\n', ' ' ),
      '''In the warmer months, you can generally find the females in the outdoor habitat, and the males inside. When it is too cold for
         any gorillas to be outside, they alternate between the day room (in between the outdoor habitat and the indoor habitat), and
         the indoor habitat.'''.replace( '\n', ' ' ),
      '''Western lowland gorillas live in the rainforests in central Africa, in countries like Republic of Congo, Gabon, and Cameroon.
         Gorillas live in complex social structures led by a dominant male, called a silverback. Male gorillas are significantly larger
         than the females, and can also be identified by the colouration on their backs and their larger foreheads. Males also form
         their own bachelor troops in the wild, if they cannot find a troop to lead. Gorillas are terrestrial and mostly herbivorous,
         feeding on leaves, fruits, stems and occasionally insects.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to several groups of gorillas. They have a bachelor troop of two recently matured males, Sadiki and
         Nassir, who are usually visible in the indoor habitat. There is also a family troop of females, Ngozi, Nneka and Charlie, who
         generally reside in the outdoor habitat when the weather permits. In summer of 2025 the zoo acquired a male gorilla, Zwalani
         to join the females. Introductions between the girls and Zwalani are still ongoing, as it takes time for these highly
         intelligent animals to welcome a new member into their social group. You may spot Zwalani in the day room in when it is not
         being occupied by the family troop of the bachelor troop.'''.replace( '\n', ' ' )
   ),

   # Indo-Malaya Pavilion
   (
      'Asian brown tortoise',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Bighead carp',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Black carp',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Black-breasted leaf turtle',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Black-throated laughing thrush',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Burmese star tortoise',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Concave casqued hornbill',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Crested wood partridge',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Crocodile lizard',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Crocodile newt',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Grass carp',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Green crested basilisk',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Luzon bleeding-heart dove',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Malayan bonytongue',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Malayan crested fireback pheasant',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Malaysian painted turtle',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Mekong barb',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Monocled cobra',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Nicobar pigeon',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Reticulated python',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The reticulated python is the longest snake species in the world. At their max, they can get up to 9 m (30 ft) in length. They
         are constrictors, which means they kill their prey by wrapping their bodies around it. Large individuals can take down large
         prey items like deer, boars, and small antelopes.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Siamese catfish',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Spiny turtle',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Sumatran orangutan',
      'Indo-Malaya Pavilion',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,0,1,4,5,5,5,5,3,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct (Outdoor + Indoor), Nov-Apr (Indoor Only)',           # Seasonal VISIBILITY summary
      '''Sumatran orangutans come from the tropical rainforests of Sumatra, and can only be outside during the warmer months. During the
         warmer months you may find these apes in their new, state-of-the-art outdoor habitat which opened in 2023, and their indoor
         habitat. If looking to see the orangutans outside, your best chance of seeing them actively exploring the habitat is to go
         there first thing in the morning.'''.replace( '\n', ' ' ),
      '''The orangutans at the zoo are still getting used to their new outdoor habitat, and thus viewing them in this habitat is far 
         from given. Your best chance of seeing them is to visit early in the day. The Toronto zoo has seven orangutans, but orangutans
         are not a highly social species like most other apes and primates. In each of the habitats you will only ever see one or two
         orangutans on exhibit at a time.'''.replace( '\n', ' ' ),
      '''Sumatran orangutans are a species of great ape that come from the rainforests of Sumatra. They are highly arboreal, and spend
         most of their time high up in the trees. There long and powerful limbs allow them to easily move through the canopy. At the zoo
         they can be seen high up in their habitats quite often. Unlike other apes, orangutans are fairly solitary. Similar to gorillas,
         the male orangutans are much larger than the females. Their fur is also much longer and shaggier, and they have these large,
         dark flaps of skin on their faces.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to seven orangutans. Puppe was born in 1967 and is the oldest orangutan in North America. The zoo also
         has adult males Budi and Kembali, and females Jingga, Rami, and Sekali. Youngster Wali, is a male born in 2022. Puppe is the
         only orangutan who goes exhibit by herself, so if you see just one orangutan in one of the habitats then it is likely her.
         Kembali and Jingga, and Budi and Rami form adult pairs on exhibit. Wali goes on exhibit with his mother, Sekali.'''
         .replace( '\n', ' ' )
   ),
   (
      'Tentacled snake',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Tinfoil barb',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The tomistoma, also known as the false gharial, is a medium-sized crocodilian native to Southeast Asia. Despite their
         appearance, tomistomas are not directly related to gharials, hence their name. Their long, peculiar-looking mouths are used
         primarily to catch fish and other prey in the water.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Tri-coloured shark',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'White-handed gibbon',
      'Indo-Malaya Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      '''The white-handed or Lar gibbon is a species of lesser ape known for its long limbs and agility, allowing them to cruise
         through the rainforest canopy. White-handed gibbons can come in a range of colours from black to a light tan. Gibbons are
         territorial and use loud calls and whoops to mark their territory and communicate with neighbouring groups. Gibbons have long,
         slender fingers, which allow them to achieve their signature swinging motion, in which they can cover gaps of up to 33 ft/10 m.
         '''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      1,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      10,                                                            # Minimum temperature (only for animals with outdoor viewing)
      0,                                                             # Snow resistance (only for animals with outdoor viewing)
      0,0,1,3,5,5,5,5,5,4,1,0,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      0,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'May-Oct (Outdoor), Nov-Apr (Indoor)',                         # Seasonal VISIBILITY summary
      '''Babirusa are a tropical species of pig and thus can only be outside in the warmer months, mostly from May to October, plus
         other warmer days. The rest of the time they can be viewed inside the greater one-horned rhino building to the left of their
         habitat.'''.replace( '\n', ' ' ),
      '''If you don't see the babirusa outside, check inside the Indian rhino building. The babirusa shares this space with the rhino,
         and is sometimes viewable inside.'''.replace( '\n', ' ' ),
      '''The babirusa is a medium-sized species of pig that is found in Southeast Asia. The babirusa is often called the deer-pig,
         because of how the males grow these curved, horn-like tusks which can actually be very dangerous to the babirusa as they can
         curve back towards the animal and protrude through the skin. Babirusa are either solitary, or live in small family groups.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to one female babirusa, a female named Olive.'''.replace( '\n', ' ' )
   ),
   (
      'Greater one-horned rhinoceros',
      'Indo-Malaya Outdoor',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The greater one-horned rhinoceros shares its indoor space with the babirusa. They rotate between the on-exhibit and off-exhibit
         spaces, and thus the rhino may not always be viewable. Your best chance of spotting him involves visiting the rhino house in
         the afternoon, and checking both sides.'''.replace( '\n', ' ' ),
      '''The greater one-horned or Indian rhinoceros varies from its African counterparts in a few key ways; for one, these rhinos are
         notoriously covered in armour-like skin. These rhinos also have one-horned as opposed to the two that the African white and
         black rhinos have. Additionally, these rhinos are solitary, only coming together for breeding, and when a mother raises her
         calf. Rhinos split most of their time between grazing on vegetation, and wallowing in waterholes to regulate their body
         temperature.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo has one male greater one-horned rhinoceros, Vishnu. Vishnu has had some skin problems recently, which is why
         you may see bandages on his body. His condition has made the outdoor rhino habitat unusable for him, due to the changes in
         terrain. There have been efforts made to smoothen the terrain to make it accessible for him, so hopefully in the future,
         Vishnu will be able to spend more time outdoors.'''.replace( '\n', ' ' )
   ),
   (
      'Indian peafowl',
      'Indo-Malaya Outdoor',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -15,                                                           # Minimum temperature (only for animals with outdoor viewing)
      4,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The Indian peafowl are very well adapted to stay in the cold, but they also have access to indoor spaces in the winter, so they
         may choose to go inside on colder days.'''.replace( '\n', ' ' ),
      None,                                                          # General viewing tips
      '''The Indian peafowl is most famous for its colourful tail feathers which only the males have, and are used in courtship and
         mating rituals. Peafowl are land-dwelling birds, but they enter trees to sleep in during the night to avoid predators.
         Peafowl are commonly called peacocks, but a peacock actually refers to a male peafowl. A female peafowl is called a peahen,
         and a baby is called a peachick.'''.replace( '\n', ' ' ),
      None                                                           # Specific animal information
   ),
   (
      'Sumatran tiger',
      'Indo-Malaya Outdoor',
      1,                                                             # Has outdoor viewing
      0,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      1,                                                             # Always viewable outdoors
      -5,                                                            # Minimum temperature (only for animals with outdoor viewing)
      4,                                                             # Snow resistance (only for animals with outdoor viewing)
      4,4,5,5,5,5,5,5,5,5,5,4,                                       # Monthly outdoor viewing (only for animals with outdoor viewing)
      4,                                                             # Winter VISIBILITY (only for animals with outdoor viewing)
      'Year-round',                                                  # Seasonal VISIBILITY summary
      '''The Sumatran tigers are generally comfortable being outside year-round, but on cooler winter days they may choose to retreat
         inside.'''.replace( '\n', ' ' ),
      '''Like most cat species, the Sumatran tigers sleep quite a lot and are the most active when it is cooler. Your best chance to
         see them active is to visit their habitat earlier or later in the day.'''.replace( '\n', ' ' ),
      '''The Sumatran tiger is the smallest species of tiger. They are endemic to the island of Sumatra, where only a few hundred
         individuals remain. These tigers are darker in colour than other species, and their stripes are placed more closely together.
         These tigers are solitary and territorial. They are carnivorous and prey on medium-sized mammals like deer and boar.'''
         .replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of Sumatran tigers, male Hari and female Kemala. Hari is significantly larger than Kemala.
         The tigers are kept in separate habitats, rotating between them. On a given visit you will see each one on either side of
         the bridge.'''.replace( '\n', ' ' )
   ),

   # Malayan Woods Pavilion
   (
      'Asian giant millipede',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Clouded leopard',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      '''The clouded leopard is a nocturnal species, and thus your best chance of seeing them active is to visit their habitat earlier
         in the morning.'''.replace( '\n', ' ' ),
      '''The clouded leopard is a medium-sized species of cat recognized for the cloud-like spotted pattern on its fur. Clouded leopards
         are usually between 2 and 3.5 ft in length with the tail being roughly the same length as the body, which it uses for balance.
         Clouded leopards are nocturnal and solitary, and they prey on birds, monkeys, deer, and other small mammals. They are able to
         hunt prey as large as themselves due to their strong jaws and sharp claws. Clouded leopards are sometimes referred to as a
         modern saber-tooth cat due to the size of their canines.'''.replace( '\n', ' ' ),
      '''The Toronto Zoo is home to a pair of clouded leopards, a male Mingma and a female Pavarti. Only one is ever on exhibit at a 
         time.'''.replace( '\n', ' ' )
   ),
   (
      'Giant gourami',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Gooty sapphire ornamental tarantula',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Malaysian stick insect jungle wood nymph',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Red-tailed green ratsnake',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   ),
   (
      'Wrinkled hornbill',
      'Malayan Woods Pavilion',
      0,                                                             # Has outdoor viewing
      1,                                                             # Has indoor viewing
      1,                                                             # Always viewable
      0,                                                             # Always viewable outdoors
      None,                                                          # Minimum temperature (only for animals with outdoor viewing)
      None,                                                          # Snow resistance (only for animals with outdoor viewing)
      None,None,None,None,None,None,None,None,None,None,None,None,   # Monthly outdoor viewing (only for animals with outdoor viewing)
      None,                                                          # Winter VISIBILITY (only for animals with outdoor viewing)
      None,                                                          # Seasonal VISIBILITY summary
      None,                                                          # Seasonal viewing tips
      None,                                                          # General viewing tips
      None,                                                          # Animal information
      None                                                           # Specific animal information
   )
]

enclosures =\
[
   # Australasia Pavilion indoor enclosures
   (
      'Brownbanded bamboo shark',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Central bearded dragon',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Clown triggerfish',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Crimson rosella',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Eastern rosella',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Emerald tree boa',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Fly river turtle',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Green tree python',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Galah',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Green-winged dove',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Komodo dragon',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Lau banded iguana',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Lionfish',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Live coral reefs',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Longnose butterflyfish',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'MacLeay\'s spectres',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Moon jellyfish',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Nicobar pigeon',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Pennant coral fish',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Pot-bellied seahorse',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Red claw yabby',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Red-tailed black cockatoo',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Short-beaked echidna',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Solomon Island leaf frog',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Southern hairy-nosed wombat',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Thorny devil stick insect',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Victoria crowned pigeon',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'White\'s tree frog',
      'Australasia Pavilion',
      'Indoor',
      65,
      41,
   ),
   (
      'Demoiselle crane',
      'Australasia Pavilion',
      'Outdoor',
      63,
      39.75,
   ),
   (
      'Kookaburra',
      'Australasia Pavilion',
      'Outdoor',
      63,
      39.75,
   ),
   (
      'Southern hairy-nosed wombat',
      'Australasia Pavilion',
      'Outdoor',
      66.75,
      40.25,
   ),

   # Australasia Outdoor
   (
      'Western grey kangaroo',
      'Australasia Outdoor',
      'Outdoor',
      68,
      42.5,
   ),

   # Eurasia Wilds
   (
      'Amur tiger',
      'Eurasia Wilds',
      'Outdoor',
      71.5,
      39,
   ),
   (
      'Asian wild horse',
      'Eurasia Wilds',
      'Outdoor',
      71.5,
      39
   ),
   (
      'Asian wild horse',
      'Eurasia Wilds',
      'Outdoor',
      67.5,
      25.75
   ),
   (
      'Bactrian camel',
      'Eurasia Wilds',
      'Outdoor',
      78.25,
      34.25
   ),
   (
      'Bactrian camel',
      'Eurasia Wilds',
      'Outdoor',
      80.5,
      28.5
   ),
   (
      'Domestic yak',
      'Eurasia Wilds',
      'Outdoor',
      86,
      27.5
   ),
   (
      'Highland cattle',
      'Eurasia Wilds',
      'Outdoor',
      87.75,
      41.25
   ),
   (
      'Mouflon',
      'Eurasia Wilds',
      'Outdoor',
      68.75,
      32.25
   ),
   (
      'Red panda',
      'Eurasia Wilds',
      'Outdoor',
      77.625,
      38.125
   ),
   (
      'Snow leopard',
      'Eurasia Wilds',
      'Outdoor',
      75.125,
      25.25
   ),
   (
      'Steller\'s sea eagle',
      'Eurasia Wilds',
      'Outdoor',
      77.125,
      24.875
   ),
   (
      'West Caucasian tur',
      'Eurasia Wilds',
      'Outdoor',
      72.5,
      25.5
   ),
   (
      'West Caucasian tur',
      'Eurasia Wilds',
      'Outdoor',
      85.75,
      31
   ),

   # Tundra Trek
   (
      'Arctic wolf',
      'Tundra Trek',
      'Outdoor',
      56,
      33.25
   ),
   (
      'Caribou',
      'Tundra Trek',
      'Outdoor',
      50.25,
      28.75
   ),
   (
      'Lesser snow goose',
      'Tundra Trek',
      'Outdoor',
      53.75,
      37
   ),
   (
      'Northern bald eagle',
      'Tundra Trek',
      'Outdoor',
      51.25,
      33.5
   ),
   (
      'Polar bear',
      'Tundra Trek',
      'Outdoor',
      55.5,
      29.375
   ),

   # Americas Outdoor Mayan Temple Ruins
   (
      'American flamingo',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      46,
      25.875
   ),
   (
      'Black-handed spider monkey',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      44.125,
      26.5
   ),
   (
      'Capybara',
      'Americas Outdoor Mayan Temple Ruins',
      'Outdoor',
      46.5,
      29.75
   ),

   # Americas Pavilion
   (
      'American alligator',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'American eel',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'American lobster',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Axolotl',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Black-footed ferret',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Black-widow spider',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Blanding\'s turtle',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Blue and yellow macaw',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Boa constrictor',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Blue poison dart frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Brazilian giant cockroach',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Brazilian salmon pink bird-eating tarantula',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Butterfly goodied',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Cuvier\'s smooth-fronted caiman',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Crested tinamou',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Desert grassland whiptail',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Dyeing poison dart frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Eastern loggerhead shrike',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Eastern lubber grasshopper',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Eyelash viper',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Ferocious water bug',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Golden lion tamarin',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Green and black poison dart frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Green surf anemone',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Green-winged macaw',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Jamaican boa',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Leather sea star',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Lemur leaf frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Longnose dace',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Massasauga rattlesnake',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Painted anemone',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Panamanian golden frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Plumose anemone',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Plush-crested jay',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Puerto Rican crested toad',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Pumpkinseed sunfish',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Red Island bird-eating tarantula',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Reticulate gila monster',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Round goby',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Rufous-collared sparrow',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'San-Esteban Island chuckwalla',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Snapping turtle',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Spot prawn',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Spotted river stingray',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Spotted turtle',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Timber rattlesnake',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Turquoise tanager',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Two-toed sloth',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Western blacknose dace',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'White-faced saki',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Yellow-banded poison dart frog',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Zebra finch',
      'Americas Pavilion',
      'Indoor',
      51.375,
      41.75
   ),
   (
      'Golden lion tamarin',
      'Americas Pavilion',
      'Outdoor',
      53,
      42.5
   ),
   (
      'Two-toed sloth',
      'Americas Pavilion',
      'Outdoor',
      53,
      42.5
   ),
   (
      'White-faced saki',
      'Americas Pavilion',
      'Outdoor',
      53,
      42.5
   ),
   (
      'Great-horned owl',
      'Americas Pavilion',
      'Outdoor',
      50.375,
      40.75
   ),
   (
      'North American river otter',
      'Americas Pavilion',
      'Outdoor',
      49,
      40.625
   ),

   # Canadian Domain
   (
      'Cougar',
      'Canadian Domain',
      'Outdoor',
      9.25,
      60.75
   ),
   (
      'Grizzly bear',
      'Canadian Domain',
      'Outdoor',
      6.125,
      65
   ),
   (
      'Northern bald eagle',
      'Canadian Domain',
      'Outdoor',
      7.5,
      71
   ),
   (
      'Raccoon',
      'Canadian Domain',
      'Outdoor',
      15,
      65.5
   ),
   (
      'Wood bison',
      'Canadian Domain',
      'Outdoor',
      11,
      58.75
   ),
   (
      'Wood bison',
      'Canadian Domain',
      'Outdoor',
      8.5,
      76.125
   ),

   # Africa Savanna
   (
      'African lion',
      'Africa Savanna',
      'Outdoor',
      39,
      62
   ),
   (
      'African penguin',
      'Africa Savanna',
      'Outdoor',
      45.5,
      66
   ),
   (
      'White-breasted cormorant',
      'Africa Savanna',
      'Outdoor',
      45.5,
      66
   ),
   (
      'African penguin',
      'Africa Savanna',
      'Indoor',
      46.25,
      63.75
   ),
   (
      'White-breasted cormorant',
      'Africa Savanna',
      'Indoor',
      46.25,
      63.75
   ),
   (
      'Cheetah',
      'Africa Savanna',
      'Outdoor',
      36.125,
      75.5
   ),
   (
      'Common eland',
      'Africa Savanna',
      'Outdoor',
      41.375,
      65.5
   ),
   (
      'Greater kudu',
      'Africa Savanna',
      'Outdoor',
      45.5,
      80
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      'Outdoor',
      45.5,
      80
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      'Outdoor',
      45.5,
      80
   ),
   (
      'White-headed vulture',
      'Africa Savanna',
      'Outdoor',
      45.5,
      80
   ),
   (
      'Greater kudu',
      'Africa Savanna',
      'Outdoor',
      47.375,
      81.75
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      'Outdoor',
      47.375,
      81.75
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      'Outdoor',
      47.375,
      81.75
   ),
   (
      'White-headed vulture',
      'Africa Savanna',
      'Outdoor',
      47.375,
      81.75
   ),
   (
      'Greater kudu',
      'Africa Savanna',
      'Outdoor',
      51.25,
      77.875
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      'Outdoor',
      51.25,
      77.875
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      'Outdoor',
      51.25,
      77.875
   ),
   (
      'White-headed vulture',
      'Africa Savanna',
      'Outdoor',
      51.25,
      77.875
   ),
   (
      'Grevy\'s zebra',
      'Africa Savanna',
      'Outdoor',
      38.5,
      70.25
   ),
   (
      'Marabou stork',
      'Africa Savanna',
      'Outdoor',
      38.375,
      73.875
   ),
   (
      'Masai giraffe',
      'Africa Savanna',
      'Outdoor',
      55,
      86.25
   ),
   (
      'Masai giraffe',
      'Africa Savanna',
      'Indoor',
      55.875,
      82.5
   ),
   (
      'Olive baboon',
      'Africa Savanna',
      'Outdoor',
      36,
      68
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Outdoor',
      36.25,
      65.5
   ),
   (
      'Ostrich',
      'Africa Savanna',
      'Outdoor',
      32,
      63
   ),
   (
      'River hippopotamus',
      'Africa Savanna',
      'Outdoor',
      52.5,
      87.375
   ),
   (
      'Southern ground hornbill',
      'Africa Savanna',
      'Outdoor',
      40.5,
      61.75
   ),
   (
      'Southern white rhinoceros',
      'Africa Savanna',
      'Outdoor',
      43.25,
      78.375
   ),
   (
      'Spotted hyena',
      'Africa Savanna',
      'Outdoor',
      41.125,
      60
   ),
   (
      'Warthog',
      'Africa Savanna',
      'Outdoor',
      51.75,
      82.5
   ),
   (
      'Watusi cattle',
      'Africa Savanna',
      'Outdoor',
      44.75,
      58.5
   ),

   # African Rainforest Pavilion
   (
      'African clawed frog',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Black crake',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Blue-bellied roller',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Hamerkop',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Lake Malawi cichlids',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Lau banded iguana',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Naked mole rat',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Ngege',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Speckled mousebird',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Veiled chameleon',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'West African dwarf crocodile',
      'African Rainforest Pavilion',
      'Indoor',
      53,
      76
   ),
   (
      'Aldabra tortoise',
      'African Rainforest Pavilion',
      'Indoor',
      54,
      80.5
   ),
   (
      'Grey-necked crowned crane',
      'African Rainforest Pavilion',
      'Indoor',
      54,
      80.5
   ),
   (
      'Ring-tailed lemur',
      'African Rainforest Pavilion',
      'Indoor',
      54,
      80.5
   ),
   (
      'Royal python',
      'African Rainforest Pavilion',
      'Indoor',
      54,
      80.5
   ),
   (
      'Aldabra tortoise',
      'African Rainforest Pavilion',
      'Outdoor',
      55,
      74
   ),
   (
      'African spoonbill',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Nile soft-shelled turtle',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Pygmy hippopotamus',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Red-footed tortoise',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Sacred ibis',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'South African shelduck',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Straw coloured fruit bat',
      'African Rainforest Pavilion',
      'Indoor',
      53.75,
      78.625
   ),
   (
      'Red river hog',
      'African Rainforest Pavilion',
      'Outdoor',
      55.5,
      78.375
   ),
   (
      'Western lowland gorilla',
      'African Rainforest Pavilion',
      'Indoor',
      52.25,
      73.25
   ),
   (
      'Western lowland gorilla',
      'African Rainforest Pavilion',
      'Outdoor',
      51.75,
      70.125
   ),

   # Indo-Malaya Pavilion
   (
      'Asian brown tortoise',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Bighead carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Black carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Black-breasted leaf turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Black-throated laughing thrush',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Burmese star tortoise',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Concave casqued hornbill',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Crested wood partridge',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Crocodile lizard',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Crocodile newt',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Grass carp',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Green crested basilisk',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Luzon bleeding-heart dove',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Malayan bonytongue',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Malayan crested fireback pheasant',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Malaysian painted turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Mekong barb',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Monocled cobra',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Nicobar pigeon',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Reticulated python',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Siamese catfish',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Spiny turtle',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),

   (
      'Sumatran orangutan',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Tentacled snake',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Tinfoil barb',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Tomistoma',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Tri-coloured shark',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'White-handed gibbon',
      'Indo-Malaya Pavilion',
      'Indoor',
      60.75,
      78.75
   ),
   (
      'Sumatran orangutan',
      'Indo-Malaya Pavilion',
      'Outdoor',
      61.75,
      85
   ),

   # Indo-Malaya Outdoor
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Outdoor',
      68.75,
      69.5
   ),
   (
      'Babirusa',
      'Indo-Malaya Outdoor',
      'Indoor',
      68.625,
      71.375
   ),
   (
      'Greater one-horned rhinoceros',
      'Indo-Malaya Outdoor',
      'Indoor',
      68.625,
      71.375
   ),
   (
      'Indian peafowl',
      'Indo-Malaya Outdoor',
      'Outdoor',
      65.125,
      71
   ),
   (
      'Sumatran tiger',
      'Indo-Malaya Outdoor',
      'Outdoor',
      61.25,
      73.25
   ),
   (
      'Sumatran tiger',
      'Indo-Malaya Outdoor',
      'Outdoor',
      59.75,
      74
   ),

   # Malayan Woods Pavilion
   (
      'Asian giant millipede',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Clouded leopard',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Giant gourami',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Gooty sapphire ornamental tarantula',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Malaysian stick insect jungle wood nymph',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Red-tailed green ratsnake',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   ),
   (
      'Wrinkled hornbill',
      'Malayan Woods Pavilion',
      'Indoor',
      66.25,
      74.5
   )
]

for a in animals:
    if len(a) != 26:
        print(len(a), a[0])

cursor.executemany( ''' INSERT INTO Animal (
                           SPECIES,
                           LOCATION,
                           HAS_OUTDOOR_VIEWING,
                           HAS_INDOOR_VIEWING,
                           ALWAYS_VIEWABLE,
                           ALWAYS_VIEWABLE_OUTDOORS,
                           MIN_TEMPERATURE,
                           SNOW_RESISTANCE,
                           JAN_VISIBILITY,
                           FEB_VISIBILITY,
                           MAR_VISIBILITY,
                           APR_VISIBILITY,
                           MAY_VISIBILITY,
                           JUN_VISIBILITY,
                           JUL_VISIBILITY,
                           AUG_VISIBILITY,
                           SEP_VISIBILITY,
                           OCT_VISIBILITY,
                           NOV_VISIBILITY,
                           DEC_VISIBILITY,
                           WINTER_VISIBILITY,
                           SEASONAL_VIEWING_SUMMARY,
                           SEASONAL_VIEWING_TIPS,
                           GENERAL_VIEWING_TIPS,
                           ANIMAL_INFO,
                           SPECIFIC_ANIMAL_INFO
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', animals )

cursor.executemany( ''' INSERT INTO Enclosure (
                           SPECIES,
                           LOCATION,
                           EXHIBIT_TYPE,
                           X_COORD,
                           Y_COORD
                        ) 
                        VALUES (?, ?, ?, ?, ?) ''', enclosures )

conn.commit()
conn.close()

print( 'Database and Animal table created successfully.' )