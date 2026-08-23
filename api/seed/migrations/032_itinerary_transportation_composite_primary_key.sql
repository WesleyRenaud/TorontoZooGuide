DROP TABLE IF EXISTS ItineraryTransportationMigration;

CREATE TABLE ItineraryTransportationMigration
(  TRANSPORTATION        VARCHAR(64) NOT NULL,
   OLD_LIKELIHOOD        INTEGER,
   NEW_LIKELIHOOD        INTEGER,
   ADDED_AS_ATTRACTION   BOOL        NOT NULL,
   START_TIME            TEXT,
   END_TIME              TEXT,
   ROUTE                 VARCHAR(64),
   PRIMARY KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION ),
   FOREIGN KEY ( TRANSPORTATION ) REFERENCES Transportation(NAME) );

INSERT INTO ItineraryTransportationMigration (
   TRANSPORTATION,
   OLD_LIKELIHOOD,
   NEW_LIKELIHOOD,
   ADDED_AS_ATTRACTION,
   START_TIME,
   END_TIME,
   ROUTE
)
SELECT
   TRANSPORTATION,
   OLD_LIKELIHOOD,
   NEW_LIKELIHOOD,
   ADDED_AS_ATTRACTION,
   START_TIME,
   END_TIME,
   ROUTE
FROM ItineraryTransportation;

DROP TABLE ItineraryTransportation;

ALTER TABLE ItineraryTransportationMigration RENAME TO ItineraryTransportation;

DROP TABLE IF EXISTS ItineraryTransportationLegMigration;

CREATE TABLE ItineraryTransportationLegMigration
(  TRANSPORTATION        VARCHAR(64) NOT NULL,
   ADDED_AS_ATTRACTION   BOOL        NOT NULL,
   FROM_STATION          VARCHAR(64) NOT NULL,
   TO_STATION            VARCHAR(64) NOT NULL,
   START_TIME            TEXT        NOT NULL,
   END_TIME              TEXT        NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION, START_TIME ),
   FOREIGN KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION )
      REFERENCES ItineraryTransportation( TRANSPORTATION, ADDED_AS_ATTRACTION ),
   FOREIGN KEY ( TRANSPORTATION, FROM_STATION, TO_STATION )
      REFERENCES TransportationLeg( TRANSPORTATION, FROM_STATION, TO_STATION ) );

INSERT INTO ItineraryTransportationLegMigration (
   TRANSPORTATION,
   ADDED_AS_ATTRACTION,
   FROM_STATION,
   TO_STATION,
   START_TIME,
   END_TIME
)
SELECT
   leg.TRANSPORTATION,
   parent.ADDED_AS_ATTRACTION,
   leg.FROM_STATION,
   leg.TO_STATION,
   leg.START_TIME,
   leg.END_TIME
FROM ItineraryTransportationLeg leg
INNER JOIN ItineraryTransportation parent
  ON parent.TRANSPORTATION = leg.TRANSPORTATION;

DROP TABLE ItineraryTransportationLeg;

ALTER TABLE ItineraryTransportationLegMigration RENAME TO ItineraryTransportationLeg;

DROP TABLE IF EXISTS ItineraryTransportationRouteMarkerMigration;

CREATE TABLE ItineraryTransportationRouteMarkerMigration
(  TRANSPORTATION        VARCHAR(64) NOT NULL,
   ADDED_AS_ATTRACTION   BOOL        NOT NULL,
   SEQUENCE              INTEGER     NOT NULL,
   MARKER_ORDER          INTEGER     NOT NULL,
   MARKER_ID             VARCHAR(64) NOT NULL,
   PRIMARY KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION, SEQUENCE, MARKER_ORDER ),
   FOREIGN KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION )
      REFERENCES ItineraryTransportation( TRANSPORTATION, ADDED_AS_ATTRACTION ) );

INSERT INTO ItineraryTransportationRouteMarkerMigration (
   TRANSPORTATION,
   ADDED_AS_ATTRACTION,
   SEQUENCE,
   MARKER_ORDER,
   MARKER_ID
)
SELECT
   marker.TRANSPORTATION,
   parent.ADDED_AS_ATTRACTION,
   marker.SEQUENCE,
   marker.MARKER_ORDER,
   marker.MARKER_ID
FROM ItineraryTransportationRouteMarker marker
INNER JOIN ItineraryTransportation parent
  ON parent.TRANSPORTATION = marker.TRANSPORTATION;

DROP TABLE ItineraryTransportationRouteMarker;

ALTER TABLE ItineraryTransportationRouteMarkerMigration RENAME TO ItineraryTransportationRouteMarker;
