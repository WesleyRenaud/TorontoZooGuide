from __future__ import annotations

import sqlite3

from seed_schema_support import column_names

from api.seed.loaders import seed_static_data
from api.seed.migrations.runner import run_migrations_on_cursor
from api.seed.schema import create_schema


def marker_ids(
      prefix: str,
      start: int,
      end: int,
      maximum: int ) -> set[ str ]:
   marker_numbers = (
      range( start, end + 1 )
      if start <= end
      else [ *range( start, maximum + 1 ), *range( 1, end + 1 ) ]
   )

   return {
      f'{ prefix }-{ str( marker_number ).zfill( 3 ) }'
      for marker_number in marker_numbers
   }


EXPECTED_ZOOMOBILE_STATIONS = {
   'Main Zoomobile Station',
   'Indo-Malaya Zoomobile Station',
   'Canadian Domain Zoomobile Station',
   'Africa Zoomobile Station',
   'Tundra Zoomobile Station',
   'Eurasia Zoomobile Station',
}

EXPECTED_ZOOMOBILE_ROUTES = {
   'summer',
   'winter',
}

EXPECTED_SUMMER_ROUTE_STATIONS = {
   'Main Zoomobile Station',
   'Canadian Domain Zoomobile Station',
   'Africa Zoomobile Station',
   'Tundra Zoomobile Station',
   'Eurasia Zoomobile Station',
}

EXPECTED_WINTER_ROUTE_STATIONS = {
   'Main Zoomobile Station',
   'Indo-Malaya Zoomobile Station',
   'Tundra Zoomobile Station',
   'Eurasia Zoomobile Station',
}

EXPECTED_ZOOMOBILE_LEGS = {
   ( 'Main Zoomobile Station', 'Canadian Domain Zoomobile Station', 20 ),
   ( 'Canadian Domain Zoomobile Station', 'Africa Zoomobile Station', 10 ),
   ( 'Africa Zoomobile Station', 'Tundra Zoomobile Station', 15 ),
   ( 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station', 15 ),
   ( 'Eurasia Zoomobile Station', 'Main Zoomobile Station', 15 ),
   ( 'Main Zoomobile Station', 'Indo-Malaya Zoomobile Station', 10 ),
   ( 'Indo-Malaya Zoomobile Station', 'Tundra Zoomobile Station', 20 ),
}

EXPECTED_ZOOMOBILE_ROUTE_LEGS = {
   ( 'summer', 'Main Zoomobile Station', 'Canadian Domain Zoomobile Station' ),
   ( 'summer', 'Canadian Domain Zoomobile Station', 'Africa Zoomobile Station' ),
   ( 'summer', 'Africa Zoomobile Station', 'Tundra Zoomobile Station' ),
   ( 'summer', 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ),
   ( 'summer', 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ),
   ( 'winter', 'Main Zoomobile Station', 'Indo-Malaya Zoomobile Station' ),
   ( 'winter', 'Indo-Malaya Zoomobile Station', 'Tundra Zoomobile Station' ),
   ( 'winter', 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ),
   ( 'winter', 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ),
}

EXPECTED_ROUTE_LEG_MARKERS = {
   ( 'summer', 'Main Zoomobile Station', 'Canadian Domain Zoomobile Station' ):
      marker_ids( 'zm-s', 5, 85, 296 ),
   ( 'summer', 'Canadian Domain Zoomobile Station', 'Africa Zoomobile Station' ):
      marker_ids( 'zm-s', 86, 127, 296 ),
   ( 'summer', 'Africa Zoomobile Station', 'Tundra Zoomobile Station' ):
      marker_ids( 'zm-s', 128, 184, 296 ),
   ( 'summer', 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ):
      marker_ids( 'zm-s', 185, 251, 296 ),
   ( 'summer', 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ):
      marker_ids( 'zm-s', 252, 4, 296 ),
   ( 'winter', 'Main Zoomobile Station', 'Indo-Malaya Zoomobile Station' ):
      marker_ids( 'zm-w', 6, 31, 241 ),
   ( 'winter', 'Indo-Malaya Zoomobile Station', 'Tundra Zoomobile Station' ):
      marker_ids( 'zm-w', 32, 112, 241 ),
   ( 'winter', 'Tundra Zoomobile Station', 'Eurasia Zoomobile Station' ):
      marker_ids( 'zm-w', 113, 209, 241 ),
   ( 'winter', 'Eurasia Zoomobile Station', 'Main Zoomobile Station' ):
      marker_ids( 'zm-w', 210, 5, 241 ),
}

MAPPED_ZOOMOBILE_STATIONS = EXPECTED_ZOOMOBILE_STATIONS


def test_zoomobile_transportation_seed_graph() -> None:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()

   create_schema( cursor )
   run_migrations_on_cursor( cursor, skip_before='011_runtime_schema_column_additions.sql' )
   seed_static_data( cursor )
   conn.commit()

   assert 'IS_ALSO_ATTRACTION' in column_names( cursor, 'Transportation' )
   assert column_names( cursor, 'TransportationStation' ) >= {
      'TRANSPORTATION',
      'NAME',
      'DESCRIPTION',
      'X_COORD',
      'Y_COORD',
      'IS_MAIN_STATION',
   }
   assert 'ON_WINTER_ROUTE' not in column_names( cursor, 'TransportationStation' )
   assert column_names( cursor, 'TransportationRoute' ) >= {
      'TRANSPORTATION',
      'ROUTE',
   }
   assert column_names( cursor, 'TransportationRouteStation' ) >= {
      'TRANSPORTATION',
      'ROUTE',
      'STATION',
   }
   assert column_names( cursor, 'TransportationDayRoute' ) >= {
      'TRANSPORTATION',
      'MONTH',
      'DAY',
      'ROUTE',
   }
   assert column_names( cursor, 'TransportationLeg' ) >= {
      'TRANSPORTATION',
      'FROM_STATION',
      'TO_STATION',
      'DURATION_MINUTES',
   }
   assert column_names( cursor, 'TransportationRouteLeg' ) >= {
      'TRANSPORTATION',
      'ROUTE',
      'FROM_STATION',
      'TO_STATION',
   }
   assert column_names( cursor, 'TransportationRouteLegMarker' ) >= {
      'TRANSPORTATION',
      'ROUTE',
      'FROM_STATION',
      'TO_STATION',
      'MARKER_ID',
   }
   assert column_names( cursor, 'TransportationStationStatus' ) >= {
      'TRANSPORTATION',
      'STATION',
   }
   table_names = {
      row[ 0 ]
      for row in cursor.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }
   assert 'ZoomobileStation' not in table_names
   assert 'ZoomobileStationStatus' not in table_names
   assert 'ZoomobileDayRoute' not in table_names
   assert 'ZoomobileRouteSchedule' not in table_names

   zoomobile = cursor.execute(
      """   SELECT NAME, IS_ALSO_ATTRACTION
            FROM Transportation
            WHERE NAME = 'Zoomobile';
      """
   ).fetchone()
   assert zoomobile is not None
   assert zoomobile[ 'IS_ALSO_ATTRACTION' ] == 1

   stations = {
      row[ 'NAME' ]
      for row in cursor.execute(
         """   SELECT NAME
               FROM TransportationStation
               WHERE TRANSPORTATION = 'Zoomobile';
         """
      ).fetchall()
   }
   assert stations == EXPECTED_ZOOMOBILE_STATIONS

   main_stations = {
      row[ 'NAME' ]
      for row in cursor.execute(
         """   SELECT NAME
               FROM TransportationStation
               WHERE TRANSPORTATION = 'Zoomobile'
               AND IS_MAIN_STATION = 1;
         """
      ).fetchall()
   }
   assert main_stations == { 'Main Zoomobile Station' }

   routes = {
      row[ 'ROUTE' ]
      for row in cursor.execute(
         """   SELECT ROUTE
               FROM TransportationRoute
               WHERE TRANSPORTATION = 'Zoomobile';
         """
      ).fetchall()
   }
   assert routes == EXPECTED_ZOOMOBILE_ROUTES

   summer_stations = {
      row[ 'STATION' ]
      for row in cursor.execute(
         """   SELECT STATION
               FROM TransportationRouteStation
               WHERE TRANSPORTATION = 'Zoomobile'
               AND ROUTE = 'summer';
         """
      ).fetchall()
   }
   assert summer_stations == EXPECTED_SUMMER_ROUTE_STATIONS

   winter_stations = {
      row[ 'STATION' ]
      for row in cursor.execute(
         """   SELECT STATION
               FROM TransportationRouteStation
               WHERE TRANSPORTATION = 'Zoomobile'
               AND ROUTE = 'winter';
         """
      ).fetchall()
   }
   assert winter_stations == EXPECTED_WINTER_ROUTE_STATIONS

   indo_malaya = cursor.execute(
      """   SELECT DESCRIPTION, X_COORD, Y_COORD
            FROM TransportationStation
            WHERE TRANSPORTATION = 'Zoomobile'
            AND NAME = 'Indo-Malaya Zoomobile Station';
      """
   ).fetchone()
   assert indo_malaya[ 'DESCRIPTION' ] is not None
   assert 'Indo-Malaya station' in indo_malaya[ 'DESCRIPTION' ]
   assert indo_malaya[ 'X_COORD' ] == 51.847
   assert indo_malaya[ 'Y_COORD' ] == 83.383

   mapped_stations = {
      row[ 'NAME' ]
      for row in cursor.execute(
         """   SELECT NAME
               FROM TransportationStation
               WHERE TRANSPORTATION = 'Zoomobile'
               AND X_COORD IS NOT NULL
               AND Y_COORD IS NOT NULL;
         """
      ).fetchall()
   }
   assert mapped_stations == MAPPED_ZOOMOBILE_STATIONS

   legs = {
      ( row[ 'FROM_STATION' ], row[ 'TO_STATION' ], row[ 'DURATION_MINUTES' ] )
      for row in cursor.execute(
         """   SELECT FROM_STATION, TO_STATION, DURATION_MINUTES
               FROM TransportationLeg
               WHERE TRANSPORTATION = 'Zoomobile';
         """
      ).fetchall()
   }
   assert legs == EXPECTED_ZOOMOBILE_LEGS

   route_legs = {
      ( row[ 'ROUTE' ], row[ 'FROM_STATION' ], row[ 'TO_STATION' ] )
      for row in cursor.execute(
         """   SELECT ROUTE, FROM_STATION, TO_STATION
               FROM TransportationRouteLeg
               WHERE TRANSPORTATION = 'Zoomobile';
         """
      ).fetchall()
   }
   assert route_legs == EXPECTED_ZOOMOBILE_ROUTE_LEGS

   route_leg_markers: dict[ tuple[ str, str, str ], set[ str ] ] = {}

   for row in cursor.execute(
         """   SELECT ROUTE, FROM_STATION, TO_STATION, MARKER_ID
               FROM TransportationRouteLegMarker
               WHERE TRANSPORTATION = 'Zoomobile';
         """
      ).fetchall():
      leg = ( row[ 'ROUTE' ], row[ 'FROM_STATION' ], row[ 'TO_STATION' ] )

      if leg not in route_leg_markers:
         route_leg_markers[ leg ] = set()

      route_leg_markers[ leg ].add( row[ 'MARKER_ID' ] )

   assert route_leg_markers == EXPECTED_ROUTE_LEG_MARKERS
   assert sum( len( markers ) for markers in route_leg_markers.values() ) == 537

   conn.close()
