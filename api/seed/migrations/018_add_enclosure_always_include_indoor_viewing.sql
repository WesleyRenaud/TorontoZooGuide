ALTER TABLE Enclosure ADD COLUMN ALWAYS_INCLUDE_INDOOR_VIEWING BOOL;

UPDATE Enclosure
SET ALWAYS_INCLUDE_INDOOR_VIEWING = 1
WHERE ( SPECIES, EXHIBIT ) IN (
   ( 'African Penguin', 'Africa Savanna' ),
   ( 'White-Breasted Cormorant', 'Africa Savanna' ),
   ( 'Western Lowland Gorilla', 'African Rainforest Pavilion' ),
   ( 'Golden Lion Tamarin', 'Americas Pavilion' ),
   ( 'North American River Otter', 'Americas Pavilion' ),
   ( 'Two-Toed Sloth', 'Americas Pavilion' ),
   ( 'White-Faced Saki', 'Americas Pavilion' ),
   ( 'Southern Hairy-Nosed Wombat', 'Australasia Pavilion' ),
   ( 'Greater One-Horned Rhinoceros', 'Indo-Malaya Outdoor' ),
   ( 'Sumatran Orangutan', 'Indo-Malaya Pavilion' )
);

UPDATE Enclosure
SET ALWAYS_INCLUDE_INDOOR_VIEWING = 0
WHERE ( SPECIES, EXHIBIT ) IN (
   ( 'Masai Giraffe', 'Africa Savanna' ),
   ( 'Aldabra Tortoise', 'African Rainforest Pavilion' ),
   ( 'Kookaburra', 'Australasia Pavilion' ),
   ( 'Babirusa', 'Indo-Malaya Outdoor' )
);
