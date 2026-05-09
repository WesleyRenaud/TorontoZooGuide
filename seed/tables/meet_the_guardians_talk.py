def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS MeetTheGuardiansTalk;' )
   cursor.execute( ''' CREATE TABLE MeetTheGuardiansTalk
                     (  NAME     VARCHAR(64) NOT NULL,
                        LOCATION VARCHAR(64) NOT NULL,
                        X_COORD  FLOAT       NOT NULL,
                        Y_COORD  FLOAT       NOT NULL,
                        DURATION INTEGER     NOT NULL,
                        FOREIGN KEY (LOCATION)  REFERENCES Exhibit(NAME), 
                        PRIMARY KEY (NAME, LOCATION) ); ''' )

guardians_talks = [
   (
      'Arctic Wolf',                   # Talk name
      'Tundra Trek',                   # Location
      75.246,                          # X coordinate on map
      55.427,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Komodo Dragon',                 # Talk name
      'Australasia Pavilion',          # Location
      72.266,                          # X coordinate on map
      66.987,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Slender-Tailed Meerkat',        # Talk name
      'African Rainforest Pavilion',   # Location
      44.708,                          # X coordinate on map
      64.671,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Highland Cattle',               # Talk name
      'Eurasia Wilds',                 # Location
      81.211,                          # X coordinate on map
      94.71,                           # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Domestic Goat',                 # Talk name
      'Goat World',                    # Location
      65.363,                          # X coordinate on map
      73.687,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'North American River Otter',    # Talk name
      'Americas Pavilion',             # Location
      69.437,                          # X coordinate on map
      47.675,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Bactrian Camel',                # Talk name
      'Eurasia Wilds',                 # Location
      82.038,                          # X coordinate on map
      84.526,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Nile Soft-Shelled Turtle',      # Talk name
      'African Rainforest Pavilion',   # Location
      43.724,                          # X coordinate on map
      65.371,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Snow Leopard',                  # Talk name
      'Eurasia Wilds',                 # Location
      85.478,                          # X coordinate on map
      75.529,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Spotted Hyena',                 # Talk name
      'Africa Savanna',                # Location
      54.873,                          # X coordinate on map
      42.598,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Western Lowland Gorilla',       # Talk name
      'African Rainforest Pavilion',   # Location
      47.812,                          # X coordinate on map
      61.419,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Amur Tiger',                    # Talk name
      'Eurasia Wilds',                 # Location
      75.979,                          # X coordinate on map
      74.707,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Sumatran Orangutan',            # Talk name
      'Indo-Malaya Pavilion',          # Location
      45.806,                          # X coordinate on map
      74.345,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'New World Primates',            # Talk name
      'Americas Pavilion',             # Location
      68.239,                          # X coordinate on map
      50.929,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'White-Handed Gibbon',           # Talk name
      'Indo-Malaya Pavilion',          # Location
      46.297,                          # X coordinate on map
      73.699,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Northern Bald Eagle',           # Talk name
      'Tundra Trek',                   # Location
      74.67,                           # X coordinate on map
      46.213,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'African Lion',                  # Talk name
      'Africa Savanna',                # Location
      51.138,                          # X coordinate on map
      41.279,                          # Y coordinate on map
      30                               # Duration in minutes
   ),
   (
      'Guardians of Plants Talk',      # Talk name
      'Greenhouse',                    # Location
      56,                              # X coordinate on map
      15,                              # Y coordinate on map
      30                               # Duration in minutes
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO MeetTheGuardiansTalk (
                              NAME,                           
                              LOCATION,
                              X_COORD,
                              Y_COORD,
                              DURATION
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', guardians_talks )
