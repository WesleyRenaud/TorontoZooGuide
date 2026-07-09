DROP TABLE IF EXISTS WildEncounterMeetingSpot;

CREATE TABLE WildEncounterMeetingSpot
(  NAME                     TEXT    NOT NULL,
   X_COORD                  FLOAT   NOT NULL,
   Y_COORD                  FLOAT   NOT NULL,
   LOOP_ID                  TEXT,
   LOOP_VIEWING_SPOT_INDEX  INTEGER,
   PRIMARY KEY (NAME) );
