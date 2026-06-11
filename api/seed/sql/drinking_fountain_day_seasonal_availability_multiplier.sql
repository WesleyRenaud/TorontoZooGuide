DROP TABLE IF EXISTS DrinkingFountainDaySeasonalAvailabilityMultiplier;

CREATE TABLE DrinkingFountainDaySeasonalAvailabilityMultiplier
(  MONTH        INTEGER     NOT NULL CHECK (MONTH BETWEEN 1 AND 12),
   DAY          INTEGER     NOT NULL CHECK (DAY BETWEEN 1 AND 31),
   LIKELIHOOD   FLOAT       NOT NULL CHECK (LIKELIHOOD BETWEEN 0.0 AND 1.0),
   PRIMARY KEY (MONTH, DAY) );
