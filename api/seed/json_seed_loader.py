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


def load_json_records(
      path: Path,
      *,
      fields: list[ str ] ) -> list[ list[ Any ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      records = json.load( seed_file )

   if not isinstance( records, list ):
      raise ValueError( f'Expected a JSON array in { path }.' )

   rows: list[ list[ Any ] ] = []

   for index, record in enumerate( records ):
      if not isinstance( record, dict ):
         raise ValueError( f'Expected record { index } in { path } to be an object.' )

      try:
         rows.append( [ record[ field ] for field in fields ] )
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on record { index } in { path }.' ) from error

   return rows


def load_json_rows( path: Path ) -> list[ list[ Any ] ]:
   with path.open( encoding='utf-8' ) as seed_file:
      rows = json.load( seed_file )

   if not isinstance( rows, list ):
      raise ValueError( f'Expected a JSON array in { path }.' )

   return [ list( row ) for row in rows ]


def _load_day_curve_payload( path: Path ) -> dict[ str, Any ]:
   with path.open( encoding='utf-8' ) as seed_file:
      payload = json.load( seed_file )

   if not isinstance( payload, dict ):
      raise ValueError( f'Expected a JSON object in { path }.' )

   return payload


def _entity_values(
      path: Path,
      payload: dict[ str, Any ],
      entity_fields: list[ str ] ) -> list[ Any ]:
   values: list[ Any ] = []

   for field in entity_fields:
      value = payload.get( field )

      if not isinstance( value, str ) or not value:
         raise ValueError( f'Expected a non-empty { field } string in { path }.' )

      values.append( value )

   return values


def load_day_curve_file(
      path: Path,
      *,
      entity_fields: list[ str ] | None = None,
      day_fields: list[ str ] ) -> list[ list[ Any ] ]:
   payload = _load_day_curve_payload( path )
   entity_values = _entity_values(
      path,
      payload,
      entity_fields or [] )
   days = payload.get( 'days' )

   if not isinstance( days, list ):
      raise ValueError( f'Expected a days array in { path }.' )

   rows: list[ list[ Any ] ] = []

   for index, day in enumerate( days ):
      if not isinstance( day, dict ):
         raise ValueError( f'Expected day { index } in { path } to be an object.' )

      try:
         day_values = [ day[ field ] for field in day_fields ]
      except KeyError as error:
         raise ValueError(
            f'Missing { error } on day { index } in { path }.' ) from error

      rows.append( entity_values + day_values )

   return rows


def load_day_curve_directory(
      directory: Path,
      *,
      entity_fields: list[ str ] | None = None,
      day_fields: list[ str ] ) -> list[ list[ Any ] ]:
   rows: list[ list[ Any ] ] = []

   for path in sorted( directory.glob( '*.json' ) ):
      rows.extend( load_day_curve_file(
         path,
         entity_fields=entity_fields,
         day_fields=day_fields ) )

   return rows


def insert_rows(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      rows: list[ list[ Any ] ] ) -> None:
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


def insert_json_records(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      fields: list[ str ],
      path: Path ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=columns,
      rows=load_json_records( path, fields=fields ) )


def insert_day_curve_file(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      path: Path,
      entity_fields: list[ str ] | None = None,
      day_fields: list[ str ] ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=columns,
      rows=load_day_curve_file(
         path,
         entity_fields=entity_fields,
         day_fields=day_fields ) )


def insert_day_curve_directory(
      cursor: Cursor,
      *,
      table: str,
      columns: list[ str ],
      directory: Path,
      entity_fields: list[ str ] | None = None,
      day_fields: list[ str ] ) -> None:
   insert_rows(
      cursor,
      table=table,
      columns=columns,
      rows=load_day_curve_directory(
         directory,
         entity_fields=entity_fields,
         day_fields=day_fields ) )
