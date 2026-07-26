DROP TABLE IF EXISTS WildEncounterMeetingSpot;

CREATE TABLE WildEncounterMeetingSpot
(  NAME                     TEXT          NOT NULL,
   X_COORD                  FLOAT         NOT NULL,
   Y_COORD                  FLOAT         NOT NULL,
   LOOP_ID                  TEXT,
   LOOP_VIEWING_SPOT_INDEX  INTEGER,
   REGION                   VARCHAR(64)   NOT NULL,
   FOREIGN KEY (REGION) REFERENCES Region(Name),
   PRIMARY KEY (NAME) );
