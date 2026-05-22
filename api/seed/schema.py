from .tables import static_tables


def create_schema( cursor ):
   for table in static_tables:
      table.create_table( cursor )

   # Old tables

   cursor.execute( 'DROP TABLE IF EXISTS GiftShopStatus;' )
   cursor.execute( 'DROP TABLE IF EXISTS MeetTheGuardiansTalkDateTime;' )
   cursor.execute( 'DROP TABLE IF EXISTS WildEncounterMeetingTime;' )
   cursor.execute( 'DROP TABLE IF EXISTS RestaurantStatus;' )
   cursor.execute( 'DROP TABLE IF EXISTS ZoomobileRouteOverride;' )
   cursor.execute( 'DROP TABLE IF EXISTS Itinerary;' )

   # Dynamic tables

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AnimalStatus
                     (  SPECIES              VARCHAR(64) NOT NULL,
                        EXHIBIT              VARCHAR(64) NOT NULL,
                        IS_OFF_DISPLAY       BOOL        NOT NULL DEFAULT 0,
                        OFF_DISPLAY_MESSAGE  TEXT,
                        OFF_DISPLAY_START    DATE,
                        OFF_DISPLAY_END      DATE,
                        PRIMARY KEY (SPECIES, EXHIBIT),
                        FOREIGN KEY (SPECIES) REFERENCES Animal(SPECIES),
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(NAME) ); ''' )

   animal_status_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( AnimalStatus );' ).fetchall()
   }

   if 'IS_OFF_DISPLAY' not in animal_status_columns:
      cursor.execute(
         'ALTER TABLE AnimalStatus ADD COLUMN IS_OFF_DISPLAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'OFF_DISPLAY_MESSAGE' not in animal_status_columns:
      cursor.execute(
         'ALTER TABLE AnimalStatus ADD COLUMN OFF_DISPLAY_MESSAGE TEXT;'
      )

   if 'OFF_DISPLAY_START' not in animal_status_columns:
      cursor.execute(
         'ALTER TABLE AnimalStatus ADD COLUMN OFF_DISPLAY_START DATE;'
      )

   if 'OFF_DISPLAY_END' not in animal_status_columns:
      cursor.execute(
         'ALTER TABLE AnimalStatus ADD COLUMN OFF_DISPLAY_END DATE;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AnimalVisibilitySchedule
                     (  SPECIES               VARCHAR(64) NOT NULL,
                        EXHIBIT               VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE   DATE,
                        SCHEDULE_END_DATE     DATE,
                        DAILY_START_TIME      VARCHAR(8) NOT NULL,
                        DAILY_END_TIME        VARCHAR(8) NOT NULL,
                        VIEWING_MESSAGE       TEXT,
                        PRIMARY KEY (SPECIES, EXHIBIT),
                        FOREIGN KEY (SPECIES) REFERENCES Animal(SPECIES),
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(NAME) ); ''' )

   animal_visibility_schedule_columns = {
      row[ 1 ] for row in cursor.execute(
         'PRAGMA table_info( AnimalVisibilitySchedule );'
      ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in animal_visibility_schedule_columns:
      cursor.execute(
         'ALTER TABLE AnimalVisibilitySchedule ADD COLUMN SCHEDULE_START_DATE DATE;'
      )

   if 'SCHEDULE_END_DATE' not in animal_visibility_schedule_columns:
      cursor.execute(
         'ALTER TABLE AnimalVisibilitySchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'DAILY_START_TIME' not in animal_visibility_schedule_columns:
      cursor.execute(
         "ALTER TABLE AnimalVisibilitySchedule ADD COLUMN DAILY_START_TIME VARCHAR(8) NOT NULL DEFAULT '09:00';"
      )

   if 'DAILY_END_TIME' not in animal_visibility_schedule_columns:
      cursor.execute(
         "ALTER TABLE AnimalVisibilitySchedule ADD COLUMN DAILY_END_TIME VARCHAR(8) NOT NULL DEFAULT '17:00';"
      )

   if 'VIEWING_MESSAGE' not in animal_visibility_schedule_columns:
      cursor.execute(
         'ALTER TABLE AnimalVisibilitySchedule ADD COLUMN VIEWING_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AnimalViewingAlert
                     (  SPECIES             VARCHAR(64) NOT NULL,
                        EXHIBIT             VARCHAR(64) NOT NULL,
                        ALERT_MESSAGE       TEXT        NOT NULL,
                        ALERT_START_DATE    DATE,
                        ALERT_END_DATE      DATE,
                        PRIMARY KEY (SPECIES, EXHIBIT),
                        FOREIGN KEY (SPECIES) REFERENCES Animal(SPECIES),
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(NAME) ); ''' )

   animal_viewing_alert_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( AnimalViewingAlert );' ).fetchall()
   }

   if 'ALERT_MESSAGE' not in animal_viewing_alert_columns:
      cursor.execute(
         'ALTER TABLE AnimalViewingAlert ADD COLUMN ALERT_MESSAGE TEXT;'
      )

   if 'ALERT_START_DATE' not in animal_viewing_alert_columns:
      cursor.execute(
         'ALTER TABLE AnimalViewingAlert ADD COLUMN ALERT_START_DATE DATE;'
      )

   if 'ALERT_END_DATE' not in animal_viewing_alert_columns:
      cursor.execute(
         'ALTER TABLE AnimalViewingAlert ADD COLUMN ALERT_END_DATE DATE;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ExhibitStatus
                     (  EXHIBIT           VARCHAR(64) NOT NULL,
                        IS_CLOSED         BOOL        NOT NULL DEFAULT 0,
                        CLOSED_MESSAGE    TEXT,
                        CLOSED_START      DATE,
                        CLOSED_END        DATE,
                        PRIMARY KEY (EXHIBIT),
                        FOREIGN KEY (EXHIBIT) REFERENCES Exhibit(NAME) ); ''' )

   exhibit_status_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ExhibitStatus );' ).fetchall()
   }

   if 'IS_CLOSED' not in exhibit_status_columns:
      cursor.execute(
         'ALTER TABLE ExhibitStatus ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 0;'
      )

   if 'CLOSED_MESSAGE' not in exhibit_status_columns:
      cursor.execute(
         'ALTER TABLE ExhibitStatus ADD COLUMN CLOSED_MESSAGE TEXT;'
      )

   if 'CLOSED_START' not in exhibit_status_columns:
      cursor.execute(
         'ALTER TABLE ExhibitStatus ADD COLUMN CLOSED_START DATE;'
      )

   if 'CLOSED_END' not in exhibit_status_columns:
      cursor.execute(
         'ALTER TABLE ExhibitStatus ADD COLUMN CLOSED_END DATE;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS RestroomStatus
                     (  RESTROOM          VARCHAR(64) NOT NULL,
                        IS_CLOSED         BOOL        NOT NULL DEFAULT 0,
                        CLOSED_MESSAGE    TEXT,
                        CLOSED_START      DATE,
                        CLOSED_END        DATE,
                        PRIMARY KEY (RESTROOM),
                        FOREIGN KEY (RESTROOM) REFERENCES Restroom(TITLE) ); ''' )

   restroom_status_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( RestroomStatus );' ).fetchall()
   }

   if 'IS_CLOSED' not in restroom_status_columns:
      cursor.execute(
         'ALTER TABLE RestroomStatus ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 0;'
      )

   if 'CLOSED_MESSAGE' not in restroom_status_columns:
      cursor.execute(
         'ALTER TABLE RestroomStatus ADD COLUMN CLOSED_MESSAGE TEXT;'
      )

   if 'CLOSED_START' not in restroom_status_columns:
      cursor.execute(
         'ALTER TABLE RestroomStatus ADD COLUMN CLOSED_START DATE;'
      )

   if 'CLOSED_END' not in restroom_status_columns:
      cursor.execute(
         'ALTER TABLE RestroomStatus ADD COLUMN CLOSED_END DATE;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS RestroomAlert
                     (  RESTROOM            VARCHAR(64) NOT NULL,
                        ALERT_MESSAGE       TEXT        NOT NULL,
                        ALERT_START_DATE    DATE,
                        ALERT_END_DATE      DATE,
                        PRIMARY KEY (RESTROOM),
                        FOREIGN KEY (RESTROOM) REFERENCES Restroom(TITLE) ); ''' )

   restroom_alert_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( RestroomAlert );' ).fetchall()
   }

   if 'ALERT_MESSAGE' not in restroom_alert_columns:
      cursor.execute(
         'ALTER TABLE RestroomAlert ADD COLUMN ALERT_MESSAGE TEXT;'
      )

   if 'ALERT_START_DATE' not in restroom_alert_columns:
      cursor.execute(
         'ALTER TABLE RestroomAlert ADD COLUMN ALERT_START_DATE DATE;'
      )

   if 'ALERT_END_DATE' not in restroom_alert_columns:
      cursor.execute(
         'ALTER TABLE RestroomAlert ADD COLUMN ALERT_END_DATE DATE;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ZooUpdate
                     (  TITLE          VARCHAR(128) NOT NULL,
                        DESCRIPTION    TEXT         NOT NULL,
                        UPDATE_TYPE    VARCHAR(32)  NOT NULL,
                        START_DATE     DATE         NOT NULL,
                        END_DATE       DATE,
                        PRIMARY KEY (TITLE, START_DATE) ); ''' )

   zoo_update_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ZooUpdate );' ).fetchall()
   }

   if 'TITLE' not in zoo_update_columns:
      cursor.execute(
         'ALTER TABLE ZooUpdate ADD COLUMN TITLE VARCHAR(128);'
      )

   if 'DESCRIPTION' not in zoo_update_columns:
      cursor.execute(
         'ALTER TABLE ZooUpdate ADD COLUMN DESCRIPTION TEXT;'
      )

   if 'UPDATE_TYPE' not in zoo_update_columns:
      cursor.execute(
         'ALTER TABLE ZooUpdate ADD COLUMN UPDATE_TYPE VARCHAR(32);'
      )

   if 'START_DATE' not in zoo_update_columns:
      cursor.execute(
         'ALTER TABLE ZooUpdate ADD COLUMN START_DATE DATE;'
      )

   if 'END_DATE' not in zoo_update_columns:
      cursor.execute(
         'ALTER TABLE ZooUpdate ADD COLUMN END_DATE DATE;'
      )

   cursor.execute(
      ''' CREATE UNIQUE INDEX IF NOT EXISTS ZooUpdateTitleStartDateIndex
          ON ZooUpdate (TITLE, START_DATE); '''
   )


   cursor.execute( ''' CREATE TABLE IF NOT EXISTS RestaurantOpeningSchedule
                     (  RESTAURANT            VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE   DATE        NOT NULL,
                        SCHEDULE_END_DATE     DATE,
                        MONDAY                BOOL        NOT NULL DEFAULT 0,
                        TUESDAY               BOOL        NOT NULL DEFAULT 0,
                        WEDNESDAY             BOOL        NOT NULL DEFAULT 0,
                        THURSDAY              BOOL        NOT NULL DEFAULT 0,
                        FRIDAY                BOOL        NOT NULL DEFAULT 0,
                        SATURDAY              BOOL        NOT NULL DEFAULT 0,
                        SUNDAY                BOOL        NOT NULL DEFAULT 0,
                        HOLIDAYS_ONLY         BOOL        NOT NULL DEFAULT 0,
                        SCHEDULE_MESSAGE      TEXT,
                        PRIMARY KEY (RESTAURANT, SCHEDULE_START_DATE),
                        FOREIGN KEY (RESTAURANT) REFERENCES Restaurant(NAME) ); ''' )

   restaurant_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( RestaurantOpeningSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'MONDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN MONDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TUESDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN TUESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'WEDNESDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN WEDNESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'THURSDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN THURSDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'FRIDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN FRIDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SATURDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN SATURDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SUNDAY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN SUNDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'HOLIDAYS_ONLY' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN HOLIDAYS_ONLY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SCHEDULE_MESSAGE' not in restaurant_schedule_columns:
      cursor.execute(
         'ALTER TABLE RestaurantOpeningSchedule ADD COLUMN SCHEDULE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS RestaurantScheduleOverride
                     (  RESTAURANT            VARCHAR(64) NOT NULL,
                        OVERRIDE_START_DATE   DATE        NOT NULL,
                        OVERRIDE_END_DATE     DATE,
                        IS_CLOSED             BOOL        NOT NULL DEFAULT 1,
                        OVERRIDE_MESSAGE      TEXT,
                        PRIMARY KEY (RESTAURANT, OVERRIDE_START_DATE),
                        FOREIGN KEY (RESTAURANT) REFERENCES Restaurant(NAME) ); ''' )

   restaurant_schedule_override_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( RestaurantScheduleOverride );' ).fetchall()
   }

   if 'OVERRIDE_START_DATE' not in restaurant_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE RestaurantScheduleOverride ADD COLUMN OVERRIDE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'OVERRIDE_END_DATE' not in restaurant_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE RestaurantScheduleOverride ADD COLUMN OVERRIDE_END_DATE DATE;'
      )

   if 'IS_CLOSED' not in restaurant_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE RestaurantScheduleOverride ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 1;'
      )

   if 'OVERRIDE_MESSAGE' not in restaurant_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE RestaurantScheduleOverride ADD COLUMN OVERRIDE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS GiftShopOpeningSchedule
                     (  GIFT_SHOP             VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE   DATE        NOT NULL,
                        SCHEDULE_END_DATE     DATE,
                        MONDAY                BOOL        NOT NULL DEFAULT 0,
                        TUESDAY               BOOL        NOT NULL DEFAULT 0,
                        WEDNESDAY             BOOL        NOT NULL DEFAULT 0,
                        THURSDAY              BOOL        NOT NULL DEFAULT 0,
                        FRIDAY                BOOL        NOT NULL DEFAULT 0,
                        SATURDAY              BOOL        NOT NULL DEFAULT 0,
                        SUNDAY                BOOL        NOT NULL DEFAULT 0,
                        HOLIDAYS_ONLY         BOOL        NOT NULL DEFAULT 0,
                        SCHEDULE_MESSAGE      TEXT,
                        PRIMARY KEY (GIFT_SHOP, SCHEDULE_START_DATE),
                        FOREIGN KEY (GIFT_SHOP) REFERENCES GiftShop(NAME) ); ''' )

   gift_shop_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( GiftShopOpeningSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'MONDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN MONDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TUESDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN TUESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'WEDNESDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN WEDNESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'THURSDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN THURSDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'FRIDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN FRIDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SATURDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN SATURDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SUNDAY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN SUNDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'HOLIDAYS_ONLY' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN HOLIDAYS_ONLY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SCHEDULE_MESSAGE' not in gift_shop_schedule_columns:
      cursor.execute(
         'ALTER TABLE GiftShopOpeningSchedule ADD COLUMN SCHEDULE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS GiftShopScheduleOverride
                     (  GIFT_SHOP             VARCHAR(64) NOT NULL,
                        OVERRIDE_START_DATE   DATE        NOT NULL,
                        OVERRIDE_END_DATE     DATE,
                        IS_CLOSED             BOOL        NOT NULL DEFAULT 1,
                        OVERRIDE_MESSAGE      TEXT,
                        PRIMARY KEY (GIFT_SHOP, OVERRIDE_START_DATE),
                        FOREIGN KEY (GIFT_SHOP) REFERENCES GiftShop(NAME) ); ''' )

   gift_shop_schedule_override_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( GiftShopScheduleOverride );' ).fetchall()
   }

   if 'OVERRIDE_START_DATE' not in gift_shop_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE GiftShopScheduleOverride ADD COLUMN OVERRIDE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'OVERRIDE_END_DATE' not in gift_shop_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE GiftShopScheduleOverride ADD COLUMN OVERRIDE_END_DATE DATE;'
      )

   if 'IS_CLOSED' not in gift_shop_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE GiftShopScheduleOverride ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 1;'
      )

   if 'OVERRIDE_MESSAGE' not in gift_shop_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE GiftShopScheduleOverride ADD COLUMN OVERRIDE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AppSetting
                     (  SETTING_KEY     VARCHAR(64) NOT NULL,
                        SETTING_VALUE   VARCHAR(64) NOT NULL,
                        PRIMARY KEY (SETTING_KEY) ); ''' )

   app_setting_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( AppSetting );' ).fetchall()
   }

   if 'SETTING_KEY' not in app_setting_columns:
      cursor.execute(
         'ALTER TABLE AppSetting ADD COLUMN SETTING_KEY VARCHAR(64) NOT NULL;'
      )

   if 'SETTING_VALUE' not in app_setting_columns:
      cursor.execute(
         'ALTER TABLE AppSetting ADD COLUMN SETTING_VALUE VARCHAR(64) NOT NULL DEFAULT "";'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AttractionOpeningSchedule
                     (  ATTRACTION            VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE   DATE        NOT NULL,
                        SCHEDULE_END_DATE     DATE,
                        MONDAY                BOOL        NOT NULL DEFAULT 0,
                        TUESDAY               BOOL        NOT NULL DEFAULT 0,
                        WEDNESDAY             BOOL        NOT NULL DEFAULT 0,
                        THURSDAY              BOOL        NOT NULL DEFAULT 0,
                        FRIDAY                BOOL        NOT NULL DEFAULT 0,
                        SATURDAY              BOOL        NOT NULL DEFAULT 0,
                        SUNDAY                BOOL        NOT NULL DEFAULT 0,
                        HOLIDAYS_ONLY         BOOL        NOT NULL DEFAULT 0,
                        SCHEDULE_MESSAGE      TEXT,
                        PRIMARY KEY (ATTRACTION, SCHEDULE_START_DATE),
                        FOREIGN KEY (ATTRACTION) REFERENCES Attraction(NAME) ); ''' )

   attraction_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( AttractionOpeningSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'MONDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN MONDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TUESDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN TUESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'WEDNESDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN WEDNESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'THURSDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN THURSDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'FRIDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN FRIDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SATURDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN SATURDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SUNDAY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN SUNDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'HOLIDAYS_ONLY' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN HOLIDAYS_ONLY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SCHEDULE_MESSAGE' not in attraction_schedule_columns:
      cursor.execute(
         'ALTER TABLE AttractionOpeningSchedule ADD COLUMN SCHEDULE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS AttractionScheduleOverride
                     (  ATTRACTION            VARCHAR(64) NOT NULL,
                        OVERRIDE_START_DATE   DATE        NOT NULL,
                        OVERRIDE_END_DATE     DATE,
                        IS_CLOSED             BOOL        NOT NULL DEFAULT 1,
                        OVERRIDE_MESSAGE      TEXT,
                        PRIMARY KEY (ATTRACTION, OVERRIDE_START_DATE),
                        FOREIGN KEY (ATTRACTION) REFERENCES Attraction(NAME) ); ''' )

   attraction_schedule_override_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( AttractionScheduleOverride );' ).fetchall()
   }

   if 'OVERRIDE_START_DATE' not in attraction_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE AttractionScheduleOverride ADD COLUMN OVERRIDE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'OVERRIDE_END_DATE' not in attraction_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE AttractionScheduleOverride ADD COLUMN OVERRIDE_END_DATE DATE;'
      )

   if 'IS_CLOSED' not in attraction_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE AttractionScheduleOverride ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 1;'
      )

   if 'OVERRIDE_MESSAGE' not in attraction_schedule_override_columns:
      cursor.execute(
         'ALTER TABLE AttractionScheduleOverride ADD COLUMN OVERRIDE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ZoomobileRouteSchedule
                     (  SCHEDULE_START_DATE   DATE        NOT NULL,
                        SCHEDULE_END_DATE     DATE,
                        ROUTE                 VARCHAR(16) NOT NULL CHECK (ROUTE IN ('summer', 'winter')),
                        PRIMARY KEY (SCHEDULE_START_DATE) ); ''' )

   zoomobile_route_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ZoomobileRouteSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in zoomobile_route_schedule_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileRouteSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in zoomobile_route_schedule_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileRouteSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'ROUTE' not in zoomobile_route_schedule_columns:
      cursor.execute(
         "ALTER TABLE ZoomobileRouteSchedule ADD COLUMN ROUTE VARCHAR(16) NOT NULL DEFAULT 'summer';"
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ZoomobileStationStatus
                     (  ZOOMOBILE_STATION VARCHAR(64) NOT NULL,
                        IS_CLOSED         BOOL        NOT NULL DEFAULT 0,
                        CLOSED_MESSAGE    TEXT,
                        CLOSED_START      DATE,
                        CLOSED_END        DATE,
                        PRIMARY KEY (ZOOMOBILE_STATION),
                        FOREIGN KEY (ZOOMOBILE_STATION) REFERENCES ZoomobileStation(NAME) ); ''' )

   zoomobile_station_status_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ZoomobileStationStatus );' ).fetchall()
   }

   if 'IS_CLOSED' not in zoomobile_station_status_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileStationStatus ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 0;'
      )

   if 'CLOSED_MESSAGE' not in zoomobile_station_status_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileStationStatus ADD COLUMN CLOSED_MESSAGE TEXT;'
      )

   if 'CLOSED_START' not in zoomobile_station_status_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileStationStatus ADD COLUMN CLOSED_START DATE;'
      )

   if 'CLOSED_END' not in zoomobile_station_status_columns:
      cursor.execute(
         'ALTER TABLE ZoomobileStationStatus ADD COLUMN CLOSED_END DATE;'
      )


   cursor.execute( ''' CREATE TABLE IF NOT EXISTS GuardiansTalkSchedule
                     (  TALK_NAME              VARCHAR(64) NOT NULL,
                        LOCATION               VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE    DATE        NOT NULL,
                        SCHEDULE_END_DATE      DATE,
                        MONDAY                 BOOL        NOT NULL DEFAULT 0,
                        TUESDAY                BOOL        NOT NULL DEFAULT 0,
                        WEDNESDAY              BOOL        NOT NULL DEFAULT 0,
                        THURSDAY               BOOL        NOT NULL DEFAULT 0,
                        FRIDAY                 BOOL        NOT NULL DEFAULT 0,
                        SATURDAY               BOOL        NOT NULL DEFAULT 0,
                        SUNDAY                 BOOL        NOT NULL DEFAULT 0,
                        TALK_TIME              TEXT        NOT NULL,
                        SCHEDULE_MESSAGE       TEXT,
                        PRIMARY KEY (TALK_NAME, LOCATION),
                        FOREIGN KEY (TALK_NAME, LOCATION) REFERENCES MeetTheGuardiansTalk(NAME, LOCATION) ); ''' )

   guardians_talk_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( GuardiansTalkSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'MONDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN MONDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TUESDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN TUESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'WEDNESDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN WEDNESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'THURSDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN THURSDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'FRIDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN FRIDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SATURDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN SATURDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SUNDAY' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN SUNDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TALK_TIME' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN TALK_TIME TEXT NOT NULL DEFAULT "";'
      )

   if 'SCHEDULE_MESSAGE' not in guardians_talk_schedule_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkSchedule ADD COLUMN SCHEDULE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS GuardiansTalkCancellation
                     (  TALK_NAME             VARCHAR(64) NOT NULL,
                        LOCATION              VARCHAR(64) NOT NULL,
                        CANCELLATION_DATE     DATE        NOT NULL,
                        TALK_TIME             TEXT        NOT NULL,
                        PRIMARY KEY (TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME),
                        FOREIGN KEY (TALK_NAME, LOCATION) REFERENCES MeetTheGuardiansTalk(NAME, LOCATION) ); ''' )

   guardians_talk_cancellation_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( GuardiansTalkCancellation );' ).fetchall()
   }

   if 'CANCELLATION_DATE' not in guardians_talk_cancellation_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkCancellation ADD COLUMN CANCELLATION_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'TALK_TIME' not in guardians_talk_cancellation_columns:
      cursor.execute(
         'ALTER TABLE GuardiansTalkCancellation ADD COLUMN TALK_TIME TEXT NOT NULL DEFAULT "";'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS WildEncounterSchedule
                     (  WILD_ENCOUNTER         VARCHAR(64) NOT NULL,
                        SCHEDULE_START_DATE    DATE        NOT NULL,
                        SCHEDULE_END_DATE      DATE,
                        MONDAY                 BOOL        NOT NULL DEFAULT 0,
                        TUESDAY                BOOL        NOT NULL DEFAULT 0,
                        WEDNESDAY              BOOL        NOT NULL DEFAULT 0,
                        THURSDAY               BOOL        NOT NULL DEFAULT 0,
                        FRIDAY                 BOOL        NOT NULL DEFAULT 0,
                        SATURDAY               BOOL        NOT NULL DEFAULT 0,
                        SUNDAY                 BOOL        NOT NULL DEFAULT 0,
                        ENCOUNTER_TIME         TEXT        NOT NULL,
                        SCHEDULE_MESSAGE       TEXT,
                        PRIMARY KEY (WILD_ENCOUNTER),
                        FOREIGN KEY (WILD_ENCOUNTER) REFERENCES WildEncounter(NAME) ); ''' )

   wild_encounter_schedule_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( WildEncounterSchedule );' ).fetchall()
   }

   if 'SCHEDULE_START_DATE' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN SCHEDULE_START_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'SCHEDULE_END_DATE' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN SCHEDULE_END_DATE DATE;'
      )

   if 'MONDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN MONDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'TUESDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN TUESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'WEDNESDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN WEDNESDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'THURSDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN THURSDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'FRIDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN FRIDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SATURDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN SATURDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'SUNDAY' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN SUNDAY BOOL NOT NULL DEFAULT 0;'
      )

   if 'ENCOUNTER_TIME' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN ENCOUNTER_TIME TEXT NOT NULL DEFAULT "";'
      )

   if 'SCHEDULE_MESSAGE' not in wild_encounter_schedule_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterSchedule ADD COLUMN SCHEDULE_MESSAGE TEXT;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS WildEncounterCancellation
                     (  WILD_ENCOUNTER        VARCHAR(64) NOT NULL,
                        CANCELLATION_DATE     DATE        NOT NULL,
                        ENCOUNTER_TIME        TEXT        NOT NULL,
                        PRIMARY KEY (WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME),
                        FOREIGN KEY (WILD_ENCOUNTER) REFERENCES WildEncounter(NAME) ); ''' )

   wild_encounter_cancellation_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( WildEncounterCancellation );' ).fetchall()
   }

   if 'CANCELLATION_DATE' not in wild_encounter_cancellation_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterCancellation ADD COLUMN CANCELLATION_DATE DATE NOT NULL DEFAULT CURRENT_DATE;'
      )

   if 'ENCOUNTER_TIME' not in wild_encounter_cancellation_columns:
      cursor.execute(
         'ALTER TABLE WildEncounterCancellation ADD COLUMN ENCOUNTER_TIME TEXT NOT NULL DEFAULT "";'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS DrinkingFountainStatus
                     (  IS_CLOSED         BOOL        NOT NULL DEFAULT 0,
                        START_DATE        DATE,
                        END_DATE          DATE,
                        CLOSED_MESSAGE    TEXT ); ''' )

   drinking_fountain_status_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( DrinkingFountainStatus );' ).fetchall()
   }

   if 'IS_CLOSED' not in drinking_fountain_status_columns:
      cursor.execute(
         'ALTER TABLE DrinkingFountainStatus ADD COLUMN IS_CLOSED BOOL NOT NULL DEFAULT 0;'
      )

   if 'START_DATE' not in drinking_fountain_status_columns:
      cursor.execute(
         'ALTER TABLE DrinkingFountainStatus ADD COLUMN START_DATE DATE;'
      )

   if 'END_DATE' not in drinking_fountain_status_columns:
      cursor.execute(
         'ALTER TABLE DrinkingFountainStatus ADD COLUMN END_DATE DATE;'
      )

   if 'CLOSED_MESSAGE' not in drinking_fountain_status_columns:
      cursor.execute(
         'ALTER TABLE DrinkingFountainStatus ADD COLUMN CLOSED_MESSAGE TEXT;'
      )

   # Itinerary tables

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ItineraryDate
                     (  ITINERARY_DATE     DATE ); ''' )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ItineraryAnimal
                     (  SPECIES              VARCHAR(64) NOT NULL,
                        EXHIBIT              VARCHAR(64) NOT NULL,
                        OLD_LIKELIHOOD       INTEGER,
                        NEW_LIKELIHOOD       INTEGER,
                        PRIMARY KEY ( SPECIES, EXHIBIT ),
                        FOREIGN KEY ( SPECIES, EXHIBIT )
                           REFERENCES Enclosure( SPECIES, EXHIBIT ) ); ''' )

   itinerary_animal_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ItineraryAnimal );' ).fetchall()
   }

   if 'EXHIBIT' not in itinerary_animal_columns:
      cursor.execute(
         'ALTER TABLE ItineraryAnimal ADD COLUMN EXHIBIT VARCHAR(64) NOT NULL DEFAULT "";'
      )

   if 'OLD_LIKELIHOOD' not in itinerary_animal_columns:
      cursor.execute(
         'ALTER TABLE ItineraryAnimal ADD COLUMN OLD_LIKELIHOOD INTEGER;'
      )

   if 'NEW_LIKELIHOOD' not in itinerary_animal_columns:
      cursor.execute(
         'ALTER TABLE ItineraryAnimal ADD COLUMN NEW_LIKELIHOOD INTEGER;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ItineraryAttraction
                     (  ATTRACTION           VARCHAR(64) NOT NULL,
                        OLD_LIKELIHOOD       INTEGER,
                        NEW_LIKELIHOOD       INTEGER,
                        PRIMARY KEY ( ATTRACTION ),
                        FOREIGN KEY ( ATTRACTION ) REFERENCES Attraction(NAME) ); ''' )

   itinerary_attraction_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ItineraryAttraction );' ).fetchall()
   }

   if 'OLD_LIKELIHOOD' not in itinerary_attraction_columns:
      cursor.execute(
         'ALTER TABLE ItineraryAttraction ADD COLUMN OLD_LIKELIHOOD INTEGER;'
      )

   if 'NEW_LIKELIHOOD' not in itinerary_attraction_columns:
      cursor.execute(
         'ALTER TABLE ItineraryAttraction ADD COLUMN NEW_LIKELIHOOD INTEGER;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ItineraryGuardiansTalk
                     (  TALK_NAME            VARCHAR(64) NOT NULL,
                        START_TIME           TEXT,
                        END_TIME             TEXT,
                        IS_DELETED           BOOL        NOT NULL DEFAULT 0,
                        PRIMARY KEY ( TALK_NAME ),
                        FOREIGN KEY ( TALK_NAME ) REFERENCES MeetTheGuardiansTalk(NAME) ); ''' )

   itinerary_guardians_talk_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ItineraryGuardiansTalk );' ).fetchall()
   }

   if 'START_TIME' not in itinerary_guardians_talk_columns:
      cursor.execute(
         'ALTER TABLE ItineraryGuardiansTalk ADD COLUMN START_TIME TEXT;'
      )

   if 'END_TIME' not in itinerary_guardians_talk_columns:
      cursor.execute(
         'ALTER TABLE ItineraryGuardiansTalk ADD COLUMN END_TIME TEXT;'
      )

   if 'IS_DELETED' not in itinerary_guardians_talk_columns:
      cursor.execute(
         'ALTER TABLE ItineraryGuardiansTalk ADD COLUMN IS_DELETED BOOL NOT NULL DEFAULT 0;'
      )

   cursor.execute( ''' CREATE TABLE IF NOT EXISTS ItineraryWildEncounter
                     (  WILD_ENCOUNTER       VARCHAR(64) NOT NULL,
                        START_TIME           TEXT,
                        END_TIME             TEXT,
                        IS_DELETED           BOOL        NOT NULL DEFAULT 0,
                        PRIMARY KEY ( WILD_ENCOUNTER ),
                        FOREIGN KEY ( WILD_ENCOUNTER ) REFERENCES WildEncounter(NAME) ); ''' )

   itinerary_wild_encounter_columns = {
      row[ 1 ] for row in cursor.execute( 'PRAGMA table_info( ItineraryWildEncounter );' ).fetchall()
   }

   if 'START_TIME' not in itinerary_wild_encounter_columns:
      cursor.execute(
         'ALTER TABLE ItineraryWildEncounter ADD COLUMN START_TIME TEXT;'
      )

   if 'END_TIME' not in itinerary_wild_encounter_columns:
      cursor.execute(
         'ALTER TABLE ItineraryWildEncounter ADD COLUMN END_TIME TEXT;'
      )

   if 'IS_DELETED' not in itinerary_wild_encounter_columns:
      cursor.execute(
         'ALTER TABLE ItineraryWildEncounter ADD COLUMN IS_DELETED BOOL NOT NULL DEFAULT 0;'
      )
