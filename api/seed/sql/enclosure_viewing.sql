DROP TABLE IF EXISTS EnclosureViewing;

CREATE TABLE EnclosureViewing
(  SPECIES                          VARCHAR(64) NOT NULL,
   EXHIBIT                          VARCHAR(64) NOT NULL,
   NAME                             VARCHAR(64),
   ENCLOSURE_TYPE                   VARCHAR(64) NOT NULL,
   SEASONALLY_OFF_DISPLAY_MESSAGE   TEXT,
   X_COORD                          FLOAT       NOT NULL,
   Y_COORD                          FLOAT       NOT NULL,
   FOREIGN KEY (SPECIES, EXHIBIT) REFERENCES Enclosure(SPECIES, EXHIBIT),
   PRIMARY KEY (SPECIES, EXHIBIT, NAME) );
