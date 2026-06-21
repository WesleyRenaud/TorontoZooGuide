CREATE TABLE IF NOT EXISTS ItineraryWalkRouteStop
(  STOP_SEQUENCE          INTEGER     NOT NULL,
   SCHEDULE_ITEM_KIND     TEXT        NOT NULL,
   ITEM_KEY               TEXT        NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   START_TIME             TEXT,
   END_TIME               TEXT,
   PRIMARY KEY ( STOP_SEQUENCE ) );
