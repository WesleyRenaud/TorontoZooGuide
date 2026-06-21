CREATE TABLE IF NOT EXISTS ItineraryWalkRoutePoint
(  POINT_SEQUENCE         INTEGER     NOT NULL,
   WALK_NODE_ID           TEXT        NOT NULL,
   X                      REAL        NOT NULL,
   Y                      REAL        NOT NULL,
   X_PX                   REAL        NOT NULL,
   Y_PX                   REAL        NOT NULL,
   PRIMARY KEY ( POINT_SEQUENCE ) );
