def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Exhibit;' )
   cursor.execute( ''' CREATE TABLE Exhibit
                     (  NAME              VARCHAR(64) NOT NULL,
                        REGION            VARCHAR(64) NOT NULL,
                        FOREIGN KEY (REGION) REFERENCES Region(Name),
                        PRIMARY KEY (NAME) ); ''' )

exhibits = [
   (
      'Australasia Pavilion',
      'Australasia',
   ),
   (
      'Australasia Outdoor',
      'Australasia',
   ),
   (
      'Eurasia Wilds',
      'Eurasia Wilds',
   ),
   (
      'Tundra Trek',
      'Tundra Trek',
   ),
   (
      'Americas Outdoor Mayan Temple Ruins',
      'Americas',
   ),
   (
      'Americas Pavilion',
      'Americas',
   ),
   (
      'Canadian Domain',
      'Canadian Domain',
   ),
   (
      'Africa Savanna',
      'Africa',
   ),
   (
      'African Rainforest Pavilion',
      'Africa',
   ),
   (
      'Indo-Malaya Pavilion',
      'Indo-Malaya',
   ),
   (
      'Indo-Malaya Outdoor',
      'Indo-Malaya',
   ),
   (
      'Malayan Woods Pavilion',
      'Indo-Malaya',
   ),
   (
      'Goat World',
      'Discovery Zone',
   ),
   (
      'Kids Zoo',
      'Discovery Zone',
   ),
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Exhibit (
                              NAME,
                              REGION
                           ) 
                           VALUES (?, ?) ''', exhibits )
