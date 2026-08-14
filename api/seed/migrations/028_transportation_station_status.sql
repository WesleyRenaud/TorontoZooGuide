DROP TABLE IF EXISTS TransportationStationStatusMigration;

CREATE TABLE TransportationStationStatusMigration
(  TRANSPORTATION      VARCHAR(64) NOT NULL,
   STATION             VARCHAR(64) NOT NULL,
   IS_CLOSED           BOOL        NOT NULL DEFAULT 0,
   CLOSED_MESSAGE      TEXT,
   CLOSED_START        DATE,
   CLOSED_END          DATE,
   PRIMARY KEY (TRANSPORTATION, STATION),
   FOREIGN KEY (TRANSPORTATION, STATION)
      REFERENCES TransportationStation(TRANSPORTATION, NAME) );

INSERT OR IGNORE INTO TransportationStationStatusMigration (
   TRANSPORTATION,
   STATION,
   IS_CLOSED,
   CLOSED_MESSAGE,
   CLOSED_START,
   CLOSED_END
)
SELECT
   'Zoomobile',
   ZOOMOBILE_STATION,
   IS_CLOSED,
   CLOSED_MESSAGE,
   CLOSED_START,
   CLOSED_END
FROM ZoomobileStationStatus;

DROP TABLE IF EXISTS ZoomobileStationStatus;

DROP TABLE IF EXISTS TransportationStationStatus;

ALTER TABLE TransportationStationStatusMigration RENAME TO TransportationStationStatus;

DROP TABLE IF EXISTS ZoomobileStation;

DROP TABLE IF EXISTS ZoomobileDayRoute;

DROP TABLE IF EXISTS ZoomobileRouteScheduleMigration;

CREATE TABLE ZoomobileRouteScheduleMigration
(  SCHEDULE_START_DATE   DATE        NOT NULL,
   SCHEDULE_END_DATE     DATE,
   ROUTE                 VARCHAR(64) NOT NULL,
   PRIMARY KEY (SCHEDULE_START_DATE) );

INSERT OR IGNORE INTO ZoomobileRouteScheduleMigration (
   SCHEDULE_START_DATE,
   SCHEDULE_END_DATE,
   ROUTE
)
SELECT
   SCHEDULE_START_DATE,
   SCHEDULE_END_DATE,
   ROUTE
FROM ZoomobileRouteSchedule;

DROP TABLE IF EXISTS ZoomobileRouteSchedule;

ALTER TABLE ZoomobileRouteScheduleMigration RENAME TO ZoomobileRouteSchedule;
