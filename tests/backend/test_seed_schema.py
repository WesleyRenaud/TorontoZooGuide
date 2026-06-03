from __future__ import annotations

import sqlite3

from api.seed import data
from api.seed.schema import create_schema
from api.seed.user_itinerary_data import clear_user_itinerary_data
from api.types import Cursor, Row


def column_names( cursor: Cursor, table: str ) -> set[ str ]:
   return {
      row[ 1 ]
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
   }


def column_info( cursor: Cursor, table: str, column: str ) -> Row:
   return next(
      row
      for row in cursor.execute( f'PRAGMA table_info( { table } );' ).fetchall()
      if row[ 1 ] == column
   )


def table_count( cursor: Cursor, table: str ) -> int:
   return cursor.execute( f'SELECT COUNT(*) FROM { table };' ).fetchone()[ 0 ]


def test_seed_data_exports_all_static_table_rows() -> None:
   assert data.regions
   assert data.exhibits
   assert data.exhibit_day_seasonal_availability_multipliers
   assert data.animals
   assert data.enclosures
   assert data.enclosure_viewings
   assert data.animal_day_seasonal_viewability_multipliers
   assert data.pavilions
   assert data.restaurants
   assert data.restaurant_day_seasonal_availability_multipliers
   assert data.restrooms
   assert data.gift_shops
   assert data.gift_shop_day_seasonal_availability_multipliers
   assert data.attractions
   assert data.attraction_day_seasonal_availability_multipliers
   assert data.zoomobile_stations
   assert data.zoomobile_day_routes
   assert data.guardians_talks
   assert data.wild_encounter_meeting_spots
   assert data.wild_encounters
   assert data.drinking_fountain_day_seasonal_availability_multipliers
   assert data.drinking_fountains
   assert data.defibrillators
   assert data.emergency_intercoms
   assert data.guest_services
   assert data.picnic_sites
   assert data.event_sites
   assert data.itinerary_error_types
   assert data.itinerary_event_defaults
   assert data.zoo_hours


def test_clear_user_itinerary_data_removes_saved_itinerary_rows() -> None:
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   create_schema( cursor )

   cursor.execute(
      "INSERT INTO ItineraryDate ( ITINERARY_DATE ) VALUES ( '2026-06-15' );"
   )
   cursor.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( 'Tiger', 'Tiger Exhibit', 50, 75 );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES ( 'Splash Island', 50, 75 );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( 'Guardians of White Rhinos', '14:00', '14:30', 0 );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES ( 'Capybara', '13:30', '14:00', 0 );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryEvent (
               EVENT_TYPE,
               START_TIME,
               END_TIME
            )
            VALUES ( 'lunch', '12:00', '12:30' );
      """
   )

   clear_user_itinerary_data( cursor )

   assert table_count( cursor, 'ItineraryDate' ) == 0
   assert table_count( cursor, 'ItineraryAnimal' ) == 0
   assert table_count( cursor, 'ItineraryAttraction' ) == 0
   assert table_count( cursor, 'ItineraryGuardiansTalk' ) == 0
   assert table_count( cursor, 'ItineraryWildEncounter' ) == 0
   assert table_count( cursor, 'ItineraryEvent' ) == 0

   conn.close()


def test_create_schema_migrates_partial_dynamic_tables() -> None:
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   partial_tables = {
      'AnimalStatus': 'SPECIES TEXT, EXHIBIT TEXT',
      'AnimalVisibilitySchedule': 'SPECIES TEXT, EXHIBIT TEXT',
      'AnimalViewingAlert': 'SPECIES TEXT, EXHIBIT TEXT',
      'ExhibitStatus': 'EXHIBIT TEXT',
      'RestroomStatus': 'RESTROOM TEXT',
      'RestroomAlert': 'RESTROOM TEXT',
      'ZooUpdate': 'TITLE TEXT, START_DATE DATE',
      'RestaurantOpeningSchedule': 'RESTAURANT TEXT',
      'RestaurantScheduleOverride': 'RESTAURANT TEXT',
      'GiftShopOpeningSchedule': 'GIFT_SHOP TEXT',
      'GiftShopScheduleOverride': 'GIFT_SHOP TEXT',
      'AppSetting': 'ID INTEGER',
      'AttractionOpeningSchedule': 'ATTRACTION TEXT',
      'AttractionScheduleOverride': 'ATTRACTION TEXT',
      'ZoomobileRouteSchedule': 'ID INTEGER',
      'ZoomobileStationStatus': 'ZOOMOBILE_STATION TEXT',
      'GuardiansTalkSchedule': 'TALK_NAME TEXT, LOCATION TEXT',
      'GuardiansTalkCancellation': 'TALK_NAME TEXT, LOCATION TEXT',
      'WildEncounterSchedule': 'WILD_ENCOUNTER TEXT',
      'WildEncounterCancellation': 'WILD_ENCOUNTER TEXT',
      'ItineraryDate': 'ITINERARY_DATE DATE',
      'ItineraryAnimal': 'SPECIES TEXT',
      'ItineraryGuardiansTalk': 'TALK_NAME TEXT',
      'ItineraryWildEncounter': 'WILD_ENCOUNTER TEXT',
      'ItineraryEvent': 'EVENT_TYPE TEXT'
   }

   for table, columns in partial_tables.items():
      cursor.execute( f'CREATE TABLE { table } ( { columns } );' )

   create_schema( cursor )

   expected_columns = {
      'AnimalStatus': {
         'SPECIES',
         'EXHIBIT',
         'IS_OFF_DISPLAY',
         'VIEWING_SCOPE',
         'OFF_DISPLAY_MESSAGE',
         'OFF_DISPLAY_START',
         'OFF_DISPLAY_END'
      },
      'AnimalVisibilitySchedule': {
         'SPECIES',
         'EXHIBIT',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'DAILY_START_TIME',
         'DAILY_END_TIME',
         'VIEWING_MESSAGE'
      },
      'AnimalViewingAlert': {
         'SPECIES',
         'EXHIBIT',
         'ALERT_MESSAGE',
         'ALERT_START_DATE',
         'ALERT_END_DATE'
      },
      'ExhibitStatus': {
         'EXHIBIT',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'RestroomStatus': {
         'RESTROOM',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'RestroomAlert': {
         'RESTROOM',
         'ALERT_MESSAGE',
         'ALERT_START_DATE',
         'ALERT_END_DATE'
      },
      'ZooUpdate': {
         'TITLE',
         'DESCRIPTION',
         'UPDATE_TYPE',
         'START_DATE',
         'END_DATE'
      },
      'RestaurantOpeningSchedule': {
         'RESTAURANT',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'RestaurantScheduleOverride': {
         'RESTAURANT',
         'OVERRIDE_START_DATE',
         'OVERRIDE_END_DATE',
         'IS_CLOSED',
         'OVERRIDE_MESSAGE'
      },
      'GiftShopOpeningSchedule': {
         'GIFT_SHOP',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'GiftShopScheduleOverride': {
         'GIFT_SHOP',
         'OVERRIDE_START_DATE',
         'OVERRIDE_END_DATE',
         'IS_CLOSED',
         'OVERRIDE_MESSAGE'
      },
      'AppSetting': {
         'ID',
         'SETTING_KEY',
         'SETTING_VALUE'
      },
      'AttractionOpeningSchedule': {
         'ATTRACTION',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'HOLIDAYS_ONLY',
         'SCHEDULE_MESSAGE'
      },
      'AttractionScheduleOverride': {
         'ATTRACTION',
         'OVERRIDE_START_DATE',
         'OVERRIDE_END_DATE',
         'IS_CLOSED',
         'OVERRIDE_MESSAGE'
      },
      'ZoomobileRouteSchedule': {
         'ID',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'ROUTE'
      },
      'ZoomobileStationStatus': {
         'ZOOMOBILE_STATION',
         'IS_CLOSED',
         'CLOSED_MESSAGE',
         'CLOSED_START',
         'CLOSED_END'
      },
      'GuardiansTalkSchedule': {
         'TALK_NAME',
         'LOCATION',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY_TIME',
         'TUESDAY_TIME',
         'WEDNESDAY_TIME',
         'THURSDAY_TIME',
         'FRIDAY_TIME',
         'SATURDAY_TIME',
         'SUNDAY_TIME',
         'SCHEDULE_MESSAGE'
      },
      'GuardiansTalkCancellation': {
         'TALK_NAME',
         'LOCATION',
         'CANCELLATION_DATE',
         'TALK_TIME'
      },
      'WildEncounterSchedule': {
         'WILD_ENCOUNTER',
         'SCHEDULE_START_DATE',
         'SCHEDULE_END_DATE',
         'MONDAY',
         'TUESDAY',
         'WEDNESDAY',
         'THURSDAY',
         'FRIDAY',
         'SATURDAY',
         'SUNDAY',
         'ENCOUNTER_TIME',
         'SCHEDULE_MESSAGE'
      },
      'WildEncounterCancellation': {
         'WILD_ENCOUNTER',
         'CANCELLATION_DATE',
         'ENCOUNTER_TIME'
      },
      'ItineraryDate': {
         'ITINERARY_DATE',
         'ARRIVAL_TIME',
         'DEPARTURE_TIME'
      },
      'ItineraryAnimal': {
         'SPECIES',
         'EXHIBIT',
         'OLD_LIKELIHOOD',
         'NEW_LIKELIHOOD',
         'IS_ADDED',
         'START_TIME',
         'END_TIME'
      },
      'ItineraryAttraction': {
         'ATTRACTION',
         'OLD_LIKELIHOOD',
         'NEW_LIKELIHOOD',
         'START_TIME',
         'END_TIME'
      },
      'ItineraryGuardiansTalk': {
         'TALK_NAME',
         'START_TIME',
         'END_TIME',
         'IS_DELETED'
      },
      'ItineraryWildEncounter': {
         'WILD_ENCOUNTER',
         'START_TIME',
         'END_TIME',
         'IS_DELETED'
      },
      'ItineraryEvent': {
         'EVENT_TYPE',
         'START_TIME',
         'END_TIME'
      },
   }

   for table, expected in expected_columns.items():
      assert expected <= column_names( cursor, table )

   assert column_info( cursor, 'ZooUpdate', 'END_DATE' )[ 3 ] == 0

   assert cursor.execute(
      """   SELECT COUNT(*) FROM sqlite_master
            WHERE type = 'table' AND name = 'ItineraryDate';
      """
   ).fetchone()[ 0 ] == 1

   conn.close()
