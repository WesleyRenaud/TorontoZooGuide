DROP TABLE IF EXISTS Attraction;

CREATE TABLE Attraction
(  NAME                                  VARCHAR(64) NOT NULL,
   FREE_WITH_ADMISSION                   BOOL        NOT NULL,
   DESCRIPTION                           TEXT        NOT NULL,
   INFO_LINK                             TEXT        NOT NULL,
   HYPERLINK_TEXT                        TEXT        NOT NULL,
   X_COORD                               FLOAT       NOT NULL,
   Y_COORD                               FLOAT       NOT NULL,
   DEFAULT_ITINERARY_DURATION_MINUTES    INTEGER     NOT NULL,
   REGION                                VARCHAR(64) NOT NULL,
   IS_ALSO_TRANSPORTATION                BOOL        NOT NULL,
   CLOSED_FOR_SEASON_UNTIL_MONTH         INTEGER,
   WEEKDAY_START_MONTH                   INTEGER,
   WEEKDAY_END_MONTH                     INTEGER,
   WEEKEND_START_MONTH                   INTEGER,
   WEEKEND_END_MONTH                     INTEGER,
   FOREIGN KEY (REGION) REFERENCES Region(Name),
   PRIMARY KEY (NAME) );
