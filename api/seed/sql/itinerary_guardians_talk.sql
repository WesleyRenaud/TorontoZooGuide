CREATE TABLE IF NOT EXISTS ItineraryGuardiansTalk
(  TALK_NAME            VARCHAR(64) NOT NULL,
   START_TIME           TEXT        NOT NULL,
   END_TIME             TEXT        NOT NULL,
   IS_DELETED           BOOL        NOT NULL DEFAULT 0,
   PRIMARY KEY ( TALK_NAME ),
   FOREIGN KEY ( TALK_NAME ) REFERENCES MeetTheGuardiansTalk(NAME) );
