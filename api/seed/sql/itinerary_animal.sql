CREATE TABLE IF NOT EXISTS ItineraryAnimal
(  SPECIES              VARCHAR(64) NOT NULL,
   EXHIBIT              VARCHAR(64) NOT NULL,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             BOOL        NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT,
   -- TODO: extend scheduling to support multiple EnclosureViewing rows per
   -- species+exhibit (e.g. include NAME in the primary key and schedule each
   -- viewing spot separately).
   PRIMARY KEY ( SPECIES, EXHIBIT ),
   FOREIGN KEY ( SPECIES, EXHIBIT )
      REFERENCES Enclosure( SPECIES, EXHIBIT ) );
