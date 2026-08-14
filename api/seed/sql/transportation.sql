DROP TABLE IF EXISTS Transportation;

CREATE TABLE Transportation
(  NAME                 VARCHAR(64) NOT NULL,
   IS_ALSO_ATTRACTION   BOOL        NOT NULL,
   PRIMARY KEY (NAME) );
