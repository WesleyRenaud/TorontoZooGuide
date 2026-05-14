def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Region;' )
   cursor.execute( ''' CREATE TABLE Region
                     (  NAME  VARCHAR(64) NOT NULL,
                        PRIMARY KEY (NAME) ); ''' )

regions = [
   (
      'Australasia',
   ),
   (
      'Eurasia Wilds',
   ),
   (
      'Tundra Trek',
   ),
   (
      'Americas',
   ),
   (
      'Canadian Domain',
   ),
   (
      'Africa',
   ),
   (
      'Indo-Malaya',
   ),
   (
      'Discovery Zone',
   ),
   (
      'Front Courtyard',
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Region (
                              NAME
                           ) 
                           VALUES (?) ''', regions )
