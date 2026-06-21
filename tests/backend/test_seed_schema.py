from __future__ import annotations

import sqlite3

from seed_schema_support import column_info
from seed_schema_support import column_names
from seed_schema_support import EXPECTED_RUNTIME_COLUMNS
from seed_schema_support import PARTIAL_RUNTIME_TABLES
from seed_schema_support import table_count

from api.seed import data
from api.seed.migrations.runner import ensure_migration_table
from api.seed.migrations.runner import migration_files
from api.seed.migrations.runner import run_migrations_on_cursor
from api.seed.schema import create_schema
from api.seed.user_itinerary_data import clear_user_itinerary_data


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
   assert data.itinerary_statuses
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
   cursor.execute(
      """   INSERT INTO ItineraryWalkRouteStop (
               STOP_SEQUENCE,
               SCHEDULE_ITEM_KIND,
               ITEM_KEY,
               WALK_NODE_ID
            )
            VALUES ( 0, 'entrance', 'entrance', '1' );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryWalkRoutePoint (
               POINT_SEQUENCE,
               WALK_NODE_ID,
               X,
               Y,
               X_PX,
               Y_PX
            )
            VALUES ( 0, '1', 0.1, 0.2, 100.0, 200.0 );
      """
   )
   cursor.execute(
      """   INSERT INTO ItineraryWalkRouteLeg (
               LEG_SEQUENCE,
               FROM_ITEM_KEY,
               TO_ITEM_KEY,
               FROM_SCHEDULE_ITEM_KIND,
               TO_SCHEDULE_ITEM_KIND,
               FROM_POINT_SEQUENCE,
               TO_POINT_SEQUENCE
            )
            VALUES (
               0,
               'entrance',
               'African Lion||Africa Savanna',
               'entrance',
               'animal',
               0,
               0
            );
      """
   )

   clear_user_itinerary_data( cursor )

   assert table_count( cursor, 'ItineraryDate' ) == 0
   assert table_count( cursor, 'ItineraryAnimal' ) == 0
   assert table_count( cursor, 'ItineraryAttraction' ) == 0
   assert table_count( cursor, 'ItineraryGuardiansTalk' ) == 0
   assert table_count( cursor, 'ItineraryWildEncounter' ) == 0
   assert table_count( cursor, 'ItineraryEvent' ) == 0
   assert table_count( cursor, 'ItineraryWalkRouteStop' ) == 0
   assert table_count( cursor, 'ItineraryWalkRoutePoint' ) == 0
   assert table_count( cursor, 'ItineraryWalkRouteLeg' ) == 0

   conn.close()


def test_migrations_upgrade_partial_runtime_tables() -> None:
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   for table, columns in PARTIAL_RUNTIME_TABLES.items():
      cursor.execute( f'CREATE TABLE { table } ( { columns } );' )

   ensure_migration_table( cursor )

   for migration_file in migration_files():
      if migration_file.name < '011_runtime_schema_column_additions.sql':
         cursor.execute(
            'INSERT INTO SchemaMigration ( MIGRATION_NAME ) VALUES ( ? );',
            ( migration_file.name, ),
         )

   run_migrations_on_cursor( cursor )
   create_schema( cursor )

   for table, expected in EXPECTED_RUNTIME_COLUMNS.items():
      assert expected <= column_names( cursor, table )

   assert column_info( cursor, 'ZooUpdate', 'END_DATE' )[ 3 ] == 0

   assert cursor.execute(
      """   SELECT COUNT(*) FROM sqlite_master
            WHERE type = 'table' AND name = 'ItineraryDate';
      """
   ).fetchone()[ 0 ] == 1

   conn.close()
