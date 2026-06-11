DROP TABLE IF EXISTS ItineraryEventDefault;

CREATE TABLE ItineraryEventDefault
(  EVENT_TYPE                            TEXT        NOT NULL PRIMARY KEY,
   DEFAULT_ITINERARY_DURATION_MINUTES    INTEGER     NOT NULL );
