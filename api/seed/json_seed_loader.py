from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..types import Cursor


SEED_DATA_DIR = Path( __file__ ).parent / 'data'


def seed_data_path( filename: str ) -> Path:
   return SEED_DATA_DIR / filename


def seed_data_dir( dirname: str ) -> Path:
   return SEED_DATA_DIR / dirname


def load_json_rows( path: Path ) -> list[ tuple[ Any, ... ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      rows = json.load( seed_file )

   if not isinstance( rows, list ):
      raise ValueError( f'Expected a JSON array in { path }.' )

   return [ tuple( row ) for row in rows ]


def load_day_seasonal_availability_curve_file(
      path: Path,
      *,
      entity_field: str ) -> list[ tuple[ Any, ... ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      payload = json.load( seed_file )

   if not isinstance( payload, dict ):
      raise ValueError( f'Expected a JSON object in { path }.' )

   entity_name = payload.get( entity_field )
   days = payload.get( 'days' )

   if not isinstance( entity_name, str ) or not entity_name:
      raise ValueError( f'Expected a non-empty { entity_field } string in { path }.' )

   if not isinstance( days, list ):
      raise ValueError( f'Expected a days array in { path }.' )

   rows: list[ tuple[ Any, ... ] ] = []

   for index, day in enumerate( days ):
      if not isinstance( day, dict ):
         raise ValueError( f'Expected day { index } in { path } to be an object.' )

      try:
         rows.append( (
            entity_name,
            day[ 'month' ],
            day[ 'day' ],
            day[ 'weekday' ],
            day[ 'weekend_holiday' ],
         ) )
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on day { index } in { path }.' ) from error

   return rows


def load_day_seasonal_availability_curve_directory(
      directory: Path,
      *,
      entity_field: str ) -> list[ tuple[ Any, ... ] ]:
   rows: list[ tuple[ Any, ... ] ] = []

   for path in sorted( directory.glob( '*.json' ) ):
      rows.extend( load_day_seasonal_availability_curve_file(
         path,
         entity_field=entity_field ) )

   return rows


def insert_rows(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      rows: list[ tuple[ Any, ... ] ] ) -> None:
   if not rows:
      return

   if any( len( row ) != len( columns ) for row in rows ):
      raise ValueError(
         f'Every row for { table } must have { len( columns ) } values.' )

   column_sql = ',\n'.join( f'                              { column }' for column in columns )
   placeholders = ', '.join( '?' for _ in columns )

   cursor.executemany(
      f''' INSERT INTO { table } (
                              { column_sql }
                           )
                           VALUES ( { placeholders } ) ''',
      rows )


def insert_json_rows(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      path: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=columns,
      rows=load_json_rows( path ) )


def insert_day_seasonal_availability_curve_directory(
      cursor: Cursor,
      *,
      table: str,
      entity_column: str,
      entity_field: str,
      directory: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=[
         entity_column,
         'MONTH',
         'DAY',
         'WEEKDAY_VALUE',
         'WEEKEND_HOLIDAY_VALUE',
      ],
      rows=load_day_seasonal_availability_curve_directory(
         directory,
         entity_field=entity_field ) )


def load_day_seasonal_value_curve_file( path: Path, *, entity_field: str ) -> list[ tuple[ Any, ... ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      payload = json.load( seed_file )

   if not isinstance( payload, dict ):
      raise ValueError( f'Expected a JSON object in { path }.' )

   entity_name = payload.get( entity_field )
   days = payload.get( 'days' )

   if not isinstance( entity_name, str ) or not entity_name:
      raise ValueError( f'Expected a non-empty { entity_field } string in { path }.' )

   if not isinstance( days, list ):
      raise ValueError( f'Expected a days array in { path }.' )

   rows: list[ tuple[ Any, ... ] ] = []

   for index, day in enumerate( days ):
      if not isinstance( day, dict ):
         raise ValueError( f'Expected day { index } in { path } to be an object.' )

      try:
         rows.append( (
            entity_name,
            day[ 'month' ],
            day[ 'day' ],
            day[ 'value' ],
         ) )
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on day { index } in { path }.' ) from error

   return rows


def load_day_seasonal_value_curve_directory(
      directory: Path,
      *,
      entity_field: str ) -> list[ tuple[ Any, ... ] ]:
   rows: list[ tuple[ Any, ... ] ] = []

   for path in sorted( directory.glob( '*.json' ) ):
      rows.extend( load_day_seasonal_value_curve_file(
         path,
         entity_field=entity_field ) )

   return rows


def insert_day_seasonal_value_curve_directory(
      cursor: Cursor,
      *,
      table: str,
      entity_column: str,
      entity_field: str,
      directory: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=[
         entity_column,
         'MONTH',
         'DAY',
         'VALUE',
      ],
      rows=load_day_seasonal_value_curve_directory(
         directory,
         entity_field=entity_field ) )


def load_animal_day_seasonal_viewability_curve_file( path: Path ) -> list[ tuple[ Any, ... ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      payload = json.load( seed_file )

   if not isinstance( payload, dict ):
      raise ValueError( f'Expected a JSON object in { path }.' )

   species = payload.get( 'species' )
   exhibit = payload.get( 'exhibit' )
   days = payload.get( 'days' )

   if not isinstance( species, str ) or not species:
      raise ValueError( f'Expected a non-empty species string in { path }.' )

   if not isinstance( exhibit, str ) or not exhibit:
      raise ValueError( f'Expected a non-empty exhibit string in { path }.' )

   if not isinstance( days, list ):
      raise ValueError( f'Expected a days array in { path }.' )

   rows: list[ tuple[ Any, ... ] ] = []

   for index, day in enumerate( days ):
      if not isinstance( day, dict ):
         raise ValueError( f'Expected day { index } in { path } to be an object.' )

      try:
         rows.append( (
            species,
            exhibit,
            day[ 'month' ],
            day[ 'day' ],
            day[ 'value' ],
         ) )
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on day { index } in { path }.' ) from error

   return rows


def load_animal_day_seasonal_viewability_curve_directory(
      directory: Path ) -> list[ tuple[ Any, ... ] ]:
   rows: list[ tuple[ Any, ... ] ] = []

   for path in sorted( directory.glob( '*.json' ) ):
      rows.extend( load_animal_day_seasonal_viewability_curve_file( path ) )

   return rows


def insert_animal_day_seasonal_viewability_curve_directory(
      cursor: Cursor,
      *,
      table: str,
      directory: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=[
         'SPECIES',
         'EXHIBIT',
         'MONTH',
         'DAY',
         'VALUE',
      ],
      rows=load_animal_day_seasonal_viewability_curve_directory( directory ) )


def load_drinking_fountain_day_seasonal_curve_file( path: Path ) -> list[ tuple[ Any, ... ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      payload = json.load( seed_file )

   if not isinstance( payload, dict ):
      raise ValueError( f'Expected a JSON object in { path }.' )

   days = payload.get( 'days' )

   if not isinstance( days, list ):
      raise ValueError( f'Expected a days array in { path }.' )

   rows: list[ tuple[ Any, ... ] ] = []

   for index, day in enumerate( days ):
      if not isinstance( day, dict ):
         raise ValueError( f'Expected day { index } in { path } to be an object.' )

      try:
         rows.append( (
            day[ 'month' ],
            day[ 'day' ],
            day[ 'likelihood' ],
         ) )
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on day { index } in { path }.' ) from error

   return rows


def insert_drinking_fountain_day_seasonal_curve_file(
      cursor: Cursor,
      *,
      table: str,
      path: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=[
         'MONTH',
         'DAY',
         'LIKELIHOOD',
      ],
      rows=load_drinking_fountain_day_seasonal_curve_file( path ) )
