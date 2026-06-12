CREATE TABLE IF NOT EXISTS ItineraryEvent
(  EVENT_TYPE           TEXT        NOT NULL,
   START_TIME           TEXT        NOT NULL,
   END_TIME             TEXT,
   PRIMARY KEY ( EVENT_TYPE, START_TIME ) );
