UPDATE ZooUpdate
SET UPDATE_TYPE = 'Animal Arrival'
WHERE UPDATE_TYPE = 'New Arrival';

UPDATE ZooUpdate
SET UPDATE_TYPE = 'Animal Departure'
WHERE UPDATE_TYPE = 'Departure';
