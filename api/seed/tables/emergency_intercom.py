def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS EmergencyIntercom;' )
   cursor.execute( ''' CREATE TABLE EmergencyIntercom
                     (  X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL,
                        PRIMARY KEY (X_COORD, Y_COORD) ); ''' )


emergency_intercoms = [
   (
      51.228,  # X coordinate on map
      56.667   # Y coordinate on map
   ),
   (
      45.700,  # X coordinate on map
      68.533   # Y coordinate on map
   ),
   (
      47.082,  # X coordinate on map
      64.940   # Y coordinate on map
   ),
   (
      41.132,  # X coordinate on map
      77.714   # Y coordinate on map
   ),
   (
      44.811,  # X coordinate on map
      77.853   # Y coordinate on map
   ),
   (
      72.217,  # X coordinate on map
      69.166   # Y coordinate on map
   ),
   (
      48.225,  # X coordinate on map
      77.606   # Y coordinate on map
   ),
   (
      69.416,  # X coordinate on map
      48.717   # Y coordinate on map
   ),
]


def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO EmergencyIntercom (
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?) ''', emergency_intercoms )
