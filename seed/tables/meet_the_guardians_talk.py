def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS MeetTheGuardiansTalk;' )
   cursor.execute( ''' CREATE TABLE MeetTheGuardiansTalk
                     (  NAME     VARCHAR(64) NOT NULL,
                        LOCATION VARCHAR(64) NOT NULL,
                        X_COORD  FLOAT       NOT NULL,
                        Y_COORD  FLOAT       NOT NULL,    
                        FOREIGN KEY (LOCATION)  REFERENCES Exhibit(NAME), 
                        PRIMARY KEY (NAME, LOCATION) ); ''' )

guardians_talks = [
   (
      'Arctic Wolf',                   # Talk name
      'Tundra Trek',                   # Location
      75.246,                          # X coordinate on map
      55.427                           # Y coordinate on map
   ),
   (
      'Sumatran Tiger',                # Talk name
      'Indo-Malaya Outdoor',           # Location
      50.259,                          # X coordinate on map
      71.641                           # Y coordinate on map
   ),
   (
      'Komodo Dragon',                 # Talk name
      'Australasia Pavilion',          # Location
      72.266,                          # X coordinate on map
      66.987                           # Y coordinate on map
   ),
   (
      'Slender-Tailed Meerkat',        # Talk name
      'African Rainforest Pavilion',   # Location
      44.708,                          # X coordinate on map
      64.671                           # Y coordinate on map
   ),
   (
      'Highland Cattle',               # Talk name
      'Eurasia Wilds',                 # Location
      81.211,                          # X coordinate on map
      94.71                            # Y coordinate on map
   ),
   (
      'Domestic Goat',                 # Talk name
      'Goat World',                    # Location
      65.363,                          # X coordinate on map
      73.687                           # Y coordinate on map
   ),
   (
      'North American River Otter',    # Talk name
      'Americas Pavilion',             # Location
      69.437,                          # X coordinate on map
      47.675                           # Y coordinate on map
   ),
   (
      'Bactrian Camel',                # Talk name
      'Eurasia Wilds',                 # Location
      82.038,                          # X coordinate on map
      84.526                           # Y coordinate on map
   ),
   (
      'Nile Soft-Shelled Turtle',      # Talk name
      'African Rainforest Pavilion',   # Location
      43.724,                          # X coordinate on map
      65.371                           # Y coordinate on map
   ),
   (
      'Snow Leopard',                  # Talk name
      'Eurasia Wilds',                 # Location
      85.478,                          # X coordinate on map
      75.529                           # Y coordinate on map
   ),
   (
      'Spotted Hyena',                 # Talk name
      'Africa Savanna',                # Location
      54.873,                          # X coordinate on map
      42.598                           # Y coordinate on map
   ),
   (
      'Western Lowland Gorilla',       # Talk name
      'African Rainforest Pavilion',   # Location
      47.812,                          # X coordinate on map
      61.419                           # Y coordinate on map
   ),
   (
      'Amur Tiger',                    # Talk name
      'Eurasia Wilds',                 # Location
      75.979,                          # X coordinate on map
      74.707                           # Y coordinate on map
   ),
   (
      'Sumatran Orangutan',            # Talk name
      'Indo-Malaya Pavilion',          # Location
      45.806,                          # X coordinate on map
      74.345                           # Y coordinate on map
   ),
   (
      'New World Primates',            # Talk name
      'Americas Pavilion',             # Location
      68.239,                          # X coordinate on map
      50.929                           # Y coordinate on map
   ),
   (
      'White-Handed Gibbon',           # Talk name
      'Indo-Malaya Pavilion',          # Location
      46.297,                          # X coordinate on map
      73.699                           # Y coordinate on map
   ),
   (
      'Northern Bald Eagle',           # Talk name
      'Tundra Trek',                   # Location
      74.67,                           # X coordinate on map
      46.213                           # Y coordinate on map
   ),
   (
      'African Lion',                  # Talk name
      'Africa Savanna',                # Location
      51.138,                          # X coordinate on map
      41.279                           # Y coordinate on map
   ),
   (
      'Guardians of Plants Talk',      # Talk name
      'Greenhouse',                    # Location
      56,                              # X coordinate on map
      15                               # Y coordinate on map
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO MeetTheGuardiansTalk (
                              NAME,                           
                              LOCATION,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?) ''', guardians_talks )
