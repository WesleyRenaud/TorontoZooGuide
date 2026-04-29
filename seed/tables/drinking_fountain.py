def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS DrinkingFountain;' )
   cursor.execute( ''' CREATE TABLE DrinkingFountain
                     (  X_COORD  FLOAT NOT NULL,
                        Y_COORD  FLOAT NOT NULL,
                        PRIMARY KEY (X_COORD, Y_COORD) ); ''' )


drinking_fountains = [
   (
      18.191,  # X coordinate on map
      12.561   # Y coordinate on map
   ),
   (
      35.991,  # X coordinate on map
      26.851   # Y coordinate on map
   ),
   (
      40.183,  # X coordinate on map
      41.038   # Y coordinate on map
   ),
   (
      37.163,  # X coordinate on map
      66.635   # Y coordinate on map
   ),
   (
      43.691,  # X coordinate on map
      68.230   # Y coordinate on map
   ),
   (
      47.469,  # X coordinate on map
      64.203   # Y coordinate on map
   ),
   (
      51.050,  # X coordinate on map
      57.762   # Y coordinate on map
   ),
   (
      54.169,  # X coordinate on map
      49.189   # Y coordinate on map
   ),
   (
      68.531,  # X coordinate on map
      87.915   # Y coordinate on map
   ),
   (
      69.556,  # X coordinate on map
      50.206   # Y coordinate on map
   ),
   (
      53.395,  # X coordinate on map
      80.674   # Y coordinate on map
   ),
   (
      78.858,  # X coordinate on map
      38.899   # Y coordinate on map
   ),
   (
      60.893,  # X coordinate on map
      73.071   # Y coordinate on map
   ),
   (
      66.570,  # X coordinate on map
      72.953   # Y coordinate on map
   ),
   (
      73.436,  # X coordinate on map
      69.038   # Y coordinate on map
   ),
   (
      76.386,  # X coordinate on map
      84.090   # Y coordinate on map
   ),
]


def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO DrinkingFountain (
                              X_COORD,
                              Y_COORD
                           )
                           VALUES (?, ?) ''', drinking_fountains )
