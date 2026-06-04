CREATE TABLE IF NOT EXISTS ItineraryStatusSuppression
(  STATUS             TEXT NOT NULL PRIMARY KEY,
   IS_SUPPRESSED      BOOL NOT NULL DEFAULT 0 );

INSERT OR IGNORE INTO ItineraryStatusSuppression ( STATUS, IS_SUPPRESSED )
   SELECT ERROR_TYPE, SUPPRESS_WARNING
   FROM ItineraryErrorSuppression
   WHERE SUPPRESS_WARNING = 1;

DROP TABLE IF EXISTS ItineraryErrorSuppression;
DROP TABLE IF EXISTS ItinerarySuppression;
DROP TABLE IF EXISTS ItineraryErrorType;
DROP TABLE IF EXISTS ItineraryErrorTypePolicy;
DROP TABLE IF EXISTS ItineraryNonSuppressableErrorType;
