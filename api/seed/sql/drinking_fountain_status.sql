CREATE TABLE IF NOT EXISTS DrinkingFountainStatus
(  IS_CLOSED         BOOL        NOT NULL DEFAULT 0,
   START_DATE        DATE,
   END_DATE          DATE,
   CLOSED_MESSAGE    TEXT );
