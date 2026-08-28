from __future__ import annotations

import sqlite3

from seed_schema_support import column_names

from api.seed.migrations.migration_runner import MigrationRunner
from api.seed.schema_creator import SchemaCreator
from api.seed.static_data_seeder import StaticDataSeeder


def test_attraction_and_meeting_spot_region_columns_are_seeded() -> None:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()

   SchemaCreator.create( cursor )
   MigrationRunner.run_on_cursor( cursor, skip_before='011_runtime_schema_column_additions.sql' )
   StaticDataSeeder.seed( cursor )
   conn.commit()

   assert 'REGION' in column_names( cursor, 'Attraction' )
   assert 'IS_ALSO_TRANSPORTATION' in column_names( cursor, 'Attraction' )
   assert 'REGION' in column_names( cursor, 'WildEncounterMeetingSpot' )
   assert 'Wildlife Science Campus' in {
      row[ 0 ]
      for row in cursor.execute( 'SELECT NAME FROM Region;' ).fetchall()
   }

   attraction_regions = {
      row[ 'NAME' ]: row[ 'REGION' ]
      for row in cursor.execute(
         'SELECT NAME, REGION FROM Attraction;'
      ).fetchall()
   }
   assert attraction_regions[ 'Zoomobile' ] == 'Front Courtyard'
   assert attraction_regions[ 'Conservation Carousel' ] == 'Front Courtyard'
   assert attraction_regions[ 'Kangaroo Walk-Thru' ] == 'Australasia'
   assert attraction_regions[ 'Greenhouse' ] == 'Wildlife Science Campus'
   assert attraction_regions[ 'Wildlife Health & Science Centre' ] == 'Wildlife Science Campus'
   assert attraction_regions[ 'Gorilla Climb Ropes Course' ] == 'Africa'
   assert attraction_regions[ 'Splash Island' ] == 'Discovery Zone'

   transportation_flags = {
      row[ 'NAME' ]: row[ 'IS_ALSO_TRANSPORTATION' ]
      for row in cursor.execute(
         'SELECT NAME, IS_ALSO_TRANSPORTATION FROM Attraction;'
      ).fetchall()
   }
   assert transportation_flags[ 'Zoomobile' ] == 1
   assert transportation_flags[ 'Conservation Carousel' ] == 0

   meeting_spot_regions = {
      row[ 'NAME' ]: row[ 'REGION' ]
      for row in cursor.execute(
         'SELECT NAME, REGION FROM WildEncounterMeetingSpot;'
      ).fetchall()
   }
   assert (
      meeting_spot_regions[ 'Wild Encounter - Zoo Front Entrance Gates Meeting Spot' ]
      == 'Front Courtyard'
   )
   assert (
      meeting_spot_regions[ 'Wild Encounter - Mayan Temple Meeting Spot' ]
      == 'Americas'
   )
   assert meeting_spot_regions[ 'Wild Encounter - Africa Meeting Spot' ] == 'Africa'

   conn.close()
