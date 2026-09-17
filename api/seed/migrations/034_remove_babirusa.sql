DELETE FROM ItineraryAnimal
   WHERE SPECIES = 'Babirusa';

DELETE FROM ItineraryGuardiansTalk
   WHERE TALK_NAME = 'Babirusa';

DELETE FROM AttractionAnimal
   WHERE SPECIES = 'Babirusa';

DELETE FROM GuardiansTalkAnimal
   WHERE TALK_NAME = 'Babirusa'
      OR SPECIES = 'Babirusa';

DELETE FROM GuardiansTalkOccurrence
   WHERE TALK_NAME = 'Babirusa';

DELETE FROM GuardiansTalkCancellation
   WHERE TALK_NAME = 'Babirusa';

DELETE FROM GuardiansTalkSchedule
   WHERE TALK_NAME = 'Babirusa';

DELETE FROM AnimalStatus
   WHERE SPECIES = 'Babirusa';

DELETE FROM AnimalVisibilitySchedule
   WHERE SPECIES = 'Babirusa';

DELETE FROM AnimalViewingAlert
   WHERE SPECIES = 'Babirusa';

DELETE FROM AnimalDaySeasonalViewabilityMultiplier
   WHERE SPECIES = 'Babirusa';

DELETE FROM EnclosureViewing
   WHERE SPECIES = 'Babirusa';

DELETE FROM Enclosure
   WHERE SPECIES = 'Babirusa';

DELETE FROM MeetTheGuardiansTalk
   WHERE NAME = 'Babirusa';

DELETE FROM Animal
   WHERE SPECIES = 'Babirusa';
