def create_table( cursor ):
   cursor.execute( 'DROP TABLE IF EXISTS Pavilion;' )
   cursor.execute( ''' CREATE TABLE Pavilion
                     (  NAME        VARCHAR(64) NOT NULL,
                        REGION      VARCHAR(64),
                        DESCRIPTION TEXT        NOT NULL,
                        X_COORD     FLOAT       NOT NULL,
                        Y_COORD     FLOAT       NOT NULL,
                        FOREIGN KEY (REGION) REFERENCES Region(Name),
                        PRIMARY KEY (NAME) ); ''' )

pavilions = [
   (
      'Australasia Pavilion',
      'Australasia',
      '''Explore a variety of flora and fauna from Oceania and Southeast Asia. Birdwatch for species like cockatoos, Victoria
         crowned pigeons, and the elusive tawny frogmouth. Venture through the jungle to find a variety of species of reptiles and
         invertebrates, most notably the Komodo dragons. Stop by the Southern hairy-nosed wombats, and then exit through the Great
         Barrier Reef exhibit where you can spot lionfish, seahorses, jellyfish, and much more.'''.replace( '\n', ' ' ),
      74.183,                                   # X coordinate on map
      65.2                                      # Y coordinate on map
   ),
   (
      'Americas Pavilion',
      'Americas',
      '''View species in a variety of habitats from all across the Americas. Begin with the tropical birds and primates of South
         America. Next venture through a number of aquatic habitats, and into the everglades wing where you can spot a number of
         invertebrates and the American Alligators. Move through the Costa Rican wing, and enjoy the playful river otters. Finally
         see a variety of North American reptiles, including the native Blanding's turtle.'''.replace( '\n', ' ' ),
      67.517,                                   # X coordinate on map
      49.129                                    # Y coordinate on map
   ),
   (
      'African Rainforest Pavilion',
      'Africa',
      '''Experience Africa's breathtaking rainforests as this pavilion provides a home to a wide range of Africa's most stunning
         species. Watch intelligent gorillas, playful lemurs, charismatic pygmy hippos, and so much more.'''.replace( '\n', ' ' ),
      45.746,                                   # X coordinate on map
      66.798                                    # Y coordinate on map
   ),
   (
      'Indo-Malaya Pavilion',
      'Indo-Malaya',
      '''Walk through this expansive pavilion which captures the beauty and scale of the beautiful Indonesian rainforest pavilions.
         Watch orangutans and gibbons swing through the tree canopy, listen to the calls of the tropical birds, and watch a number
         of species of reptile scurry across the forest floor.'''.replace( '\n', ' ' ),
      47.879,                                   # X coordinate on map
      76.223                                    # Y coordinate on map
   ),
   (
      'Malayan Woods Pavilion',
      'Indo-Malaya',
      '''Come in and spot the clouded leopards and experience the forests of Malaysian as you walk through this pavilion.''',
      51.28,                                    # X coordinate on map
      81.497                                    # Y coordinate on map
   ),
   (
      'Greater One-Horned Rhinoceros Pavilion',
      'Indo-Malaya',
      '''Enter this building to perhaps catch of glimpse of the greater one-horned rhinoceros or babirusa.''',
      53.275,                                   # X coordinate on map
      82.823                                    # Y coordinate on map
   )
]

def insert_rows( cursor ):
   cursor.executemany( ''' INSERT INTO Pavilion (
                              NAME,
                              REGION,
                              DESCRIPTION,
                              X_COORD,
                              Y_COORD
                           ) 
                           VALUES (?, ?, ?, ?, ?) ''', pavilions )
