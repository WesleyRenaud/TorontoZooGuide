DROP TABLE IF EXISTS ZoomobileStation;

CREATE TABLE ZoomobileStation
(  NAME              VARCHAR(64) NOT NULL,
   ON_WINTER_ROUTE   BOOL        NOT NULL,
   DESCRIPTION       TEXT        NOT NULL,
   X_COORD           FLOAT       NOT NULL,
   Y_COORD           FLOAT       NOT NULL,
   PRIMARY KEY (NAME) );
