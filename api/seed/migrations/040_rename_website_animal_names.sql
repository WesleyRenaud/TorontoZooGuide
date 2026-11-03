PRAGMA foreign_keys = OFF;

UPDATE AnimalStatus
SET SPECIES = 'Edwards''s Pheasant'
WHERE SPECIES = 'Edward''s Pheasant';

UPDATE AnimalStatus
SET SPECIES = 'Live Reef Corals'
WHERE SPECIES = 'Live Coral Reefs';

UPDATE AnimalStatus
SET SPECIES = 'White Rhinoceros'
WHERE SPECIES = 'Southern White Rhinoceros';

UPDATE AnimalStatus
SET SPECIES = 'Tri-Colour Shark'
WHERE SPECIES = 'Tri-Coloured Shark';

UPDATE AnimalVisibilitySchedule
SET SPECIES = 'Edwards''s Pheasant'
WHERE SPECIES = 'Edward''s Pheasant';

UPDATE AnimalVisibilitySchedule
SET SPECIES = 'Live Reef Corals'
WHERE SPECIES = 'Live Coral Reefs';

UPDATE AnimalVisibilitySchedule
SET SPECIES = 'White Rhinoceros'
WHERE SPECIES = 'Southern White Rhinoceros';

UPDATE AnimalVisibilitySchedule
SET SPECIES = 'Tri-Colour Shark'
WHERE SPECIES = 'Tri-Coloured Shark';

UPDATE AnimalViewingAlert
SET SPECIES = 'Edwards''s Pheasant'
WHERE SPECIES = 'Edward''s Pheasant';

UPDATE AnimalViewingAlert
SET SPECIES = 'Live Reef Corals'
WHERE SPECIES = 'Live Coral Reefs';

UPDATE AnimalViewingAlert
SET SPECIES = 'White Rhinoceros'
WHERE SPECIES = 'Southern White Rhinoceros';

UPDATE AnimalViewingAlert
SET SPECIES = 'Tri-Colour Shark'
WHERE SPECIES = 'Tri-Coloured Shark';

UPDATE ItineraryAnimal
SET SPECIES = 'Edwards''s Pheasant'
WHERE SPECIES = 'Edward''s Pheasant';

UPDATE ItineraryAnimal
SET SPECIES = 'Live Reef Corals'
WHERE SPECIES = 'Live Coral Reefs';

UPDATE ItineraryAnimal
SET SPECIES = 'White Rhinoceros'
WHERE SPECIES = 'Southern White Rhinoceros';

UPDATE ItineraryAnimal
SET SPECIES = 'Tri-Colour Shark'
WHERE SPECIES = 'Tri-Coloured Shark';

UPDATE GuardiansTalkSchedule
SET TALK_NAME = 'White Rhinoceros'
WHERE TALK_NAME = 'Southern White Rhinoceros';

UPDATE GuardiansTalkSchedule
SET SCHEDULE_MESSAGE = REPLACE( SCHEDULE_MESSAGE, 'Southern White Rhinoceros', 'White Rhinoceros' )
WHERE SCHEDULE_MESSAGE LIKE '%Southern White Rhinoceros%';

UPDATE GuardiansTalkOccurrence
SET TALK_NAME = 'White Rhinoceros'
WHERE TALK_NAME = 'Southern White Rhinoceros';

UPDATE GuardiansTalkCancellation
SET TALK_NAME = 'White Rhinoceros'
WHERE TALK_NAME = 'Southern White Rhinoceros';

UPDATE ItineraryGuardiansTalk
SET TALK_NAME = 'White Rhinoceros'
WHERE TALK_NAME = 'Southern White Rhinoceros';

DELETE FROM AnimalStatus
WHERE ( SPECIES = 'Asian Brown Tortoise' AND EXHIBIT = 'Indo-Malaya Pavilion' )
   OR ( SPECIES = 'Marabou Stork' AND EXHIBIT = 'Kids Zoo' );

DELETE FROM AnimalVisibilitySchedule
WHERE ( SPECIES = 'Asian Brown Tortoise' AND EXHIBIT = 'Indo-Malaya Pavilion' )
   OR ( SPECIES = 'Marabou Stork' AND EXHIBIT = 'Kids Zoo' );

DELETE FROM AnimalViewingAlert
WHERE ( SPECIES = 'Asian Brown Tortoise' AND EXHIBIT = 'Indo-Malaya Pavilion' )
   OR ( SPECIES = 'Marabou Stork' AND EXHIBIT = 'Kids Zoo' );

DELETE FROM ItineraryAnimal
WHERE ( SPECIES = 'Asian Brown Tortoise' AND EXHIBIT = 'Indo-Malaya Pavilion' )
   OR ( SPECIES = 'Marabou Stork' AND EXHIBIT = 'Kids Zoo' );
