DROP TABLE IF EXISTS EnclosureViewing;

CREATE TABLE EnclosureViewing
(  SPECIES                          VARCHAR(64) NOT NULL,
   EXHIBIT                          VARCHAR(64) NOT NULL,
   ENCLOSURE_TYPE                   VARCHAR(64) NOT NULL,
   SEASONALLY_OFF_DISPLAY_MESSAGE   TEXT,
   X_COORD                          FLOAT       NOT NULL,
   Y_COORD                          FLOAT       NOT NULL,
   FOREIGN KEY (SPECIES) REFERENCES Animal,
   FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(Name),
   PRIMARY KEY (SPECIES, EXHIBIT, X_COORD, Y_COORD) );
