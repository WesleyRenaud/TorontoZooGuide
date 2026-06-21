CREATE TABLE IF NOT EXISTS ItineraryWalkRouteStop
(  STOP_SEQUENCE          INTEGER     NOT NULL,
   SCHEDULE_ITEM_KIND     TEXT        NOT NULL,
   ITEM_KEY               TEXT        NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   START_TIME             TEXT,
   END_TIME               TEXT,
   PRIMARY KEY ( STOP_SEQUENCE ) );

CREATE TABLE IF NOT EXISTS ItineraryWalkRoutePoint
(  POINT_SEQUENCE         INTEGER     NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   X                      REAL        NOT NULL,
   Y                      REAL        NOT NULL,
   X_PX                   REAL        NOT NULL,
   Y_PX                   REAL        NOT NULL,
   PRIMARY KEY ( POINT_SEQUENCE ) );

CREATE TABLE IF NOT EXISTS ItineraryWalkRouteLeg
(  LEG_SEQUENCE               INTEGER     NOT NULL,
   FROM_ITEM_KEY              TEXT        NOT NULL,
   TO_ITEM_KEY                TEXT        NOT NULL,
   FROM_SCHEDULE_ITEM_KIND    TEXT        NOT NULL,
   TO_SCHEDULE_ITEM_KIND      TEXT        NOT NULL,
   FROM_POINT_SEQUENCE        INTEGER     NOT NULL,
   TO_POINT_SEQUENCE          INTEGER     NOT NULL,
   PRIMARY KEY ( LEG_SEQUENCE ) );
