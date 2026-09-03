from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

from api.seed.json_seed_loader import JsonSeedLoader, SEED_DATA_DIR
from api.types import Types

class StubCursor:
   def __init__( self ) -> None:
      self.executemany_calls: list[ tuple[ str, list[ list[ Any ] ] ] ] = []


   def executemany( self, sql: str, rows: list[ list[ Any ] ] ) -> None:
      self.executemany_calls.append( ( sql, rows ) )

def _cursor() -> tuple[ StubCursor, Types.Cursor ]:
   stub = StubCursor()
   return stub, cast( Types.Cursor, stub )

def Test_SeedDataPath_TestFilename_ExpectUnderSeedDataDir() -> None:
   assert JsonSeedLoader.seed_data_path( 'animals.json' ) == SEED_DATA_DIR / 'animals.json'

def Test_SeedDataDir_TestDirname_ExpectUnderSeedDataDir() -> None:
   assert JsonSeedLoader.seed_data_dir( 'curves' ) == SEED_DATA_DIR / 'curves'

def Test_LoadJsonRecords_TestValidRecords_ExpectFieldRows(
      tmp_path: Path ) -> None:
   path = tmp_path / 'records.json'
   path.write_text(
      json.dumps( [
         { 'name': 'Lion', 'exhibit': 'Africa' },
         { 'name': 'Giraffe', 'exhibit': 'Africa' },
      ] ),
      encoding='utf-8' )

   assert JsonSeedLoader.load_json_records(
      path,
      fields=[ 'name', 'exhibit' ] ) == [
      [ 'Lion', 'Africa' ],
      [ 'Giraffe', 'Africa' ],
   ]

def Test_LoadJsonRecords_TestMissingField_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'records.json'
   path.write_text(
      json.dumps( [ { 'name': 'Lion' } ] ),
      encoding='utf-8' )

   with pytest.raises( ValueError, match="Missing 'exhibit'" ):
      JsonSeedLoader.load_json_records( path, fields=[ 'name', 'exhibit' ] )

def Test_LoadJsonRecords_TestNonArray_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'records.json'
   path.write_text( json.dumps( { 'name': 'Lion' } ), encoding='utf-8' )

   with pytest.raises( ValueError, match='Expected a JSON array' ):
      JsonSeedLoader.load_json_records( path, fields=[ 'name' ] )

def Test_LoadJsonRecords_TestNonObjectRecord_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'records.json'
   path.write_text( json.dumps( [ 'Lion' ] ), encoding='utf-8' )

   with pytest.raises( ValueError, match='to be an object' ):
      JsonSeedLoader.load_json_records( path, fields=[ 'name' ] )

def Test_LoadJsonRows_TestValidRows_ExpectCopiedLists(
      tmp_path: Path ) -> None:
   path = tmp_path / 'rows.json'
   path.write_text(
      json.dumps( [ [ 'Lion', 'Africa' ], [ 'Giraffe', 'Africa' ] ] ),
      encoding='utf-8' )

   assert JsonSeedLoader.load_json_rows( path ) == [
      [ 'Lion', 'Africa' ],
      [ 'Giraffe', 'Africa' ],
   ]

def Test_LoadJsonRows_TestNonArray_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'rows.json'
   path.write_text( json.dumps( { 'row': 1 } ), encoding='utf-8' )

   with pytest.raises( ValueError, match='Expected a JSON array' ):
      JsonSeedLoader.load_json_rows( path )

def Test_LoadDayCurveFile_TestValidPayload_ExpectEntityPlusDayRows(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( {
         'species': 'Lion',
         'exhibit': 'Africa',
         'days': [
            { 'day': 1, 'value': 0.5 },
            { 'day': 2, 'value': 0.8 },
         ],
      } ),
      encoding='utf-8' )

   assert JsonSeedLoader.load_day_curve_file(
      path,
      entity_fields=[ 'species', 'exhibit' ],
      day_fields=[ 'day', 'value' ] ) == [
      [ 'Lion', 'Africa', 1, 0.5 ],
      [ 'Lion', 'Africa', 2, 0.8 ],
   ]

def Test_LoadDayCurveFile_TestNonObjectPayload_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text( json.dumps( [ 1, 2 ] ), encoding='utf-8' )

   with pytest.raises( ValueError, match='Expected a JSON object' ):
      JsonSeedLoader.load_day_curve_file( path, day_fields=[ 'day' ] )

def Test_LoadDayCurveFile_TestMissingEntityField_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( { 'species': '', 'days': [] } ),
      encoding='utf-8' )

   with pytest.raises( ValueError, match='non-empty species string' ):
      JsonSeedLoader.load_day_curve_file(
         path,
         entity_fields=[ 'species' ],
         day_fields=[ 'day' ] )

def Test_LoadDayCurveFile_TestMissingDays_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text( json.dumps( { 'species': 'Lion' } ), encoding='utf-8' )

   with pytest.raises( ValueError, match='Expected a days array' ):
      JsonSeedLoader.load_day_curve_file(
         path,
         entity_fields=[ 'species' ],
         day_fields=[ 'day' ] )

def Test_LoadDayCurveFile_TestNonObjectDay_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( {
         'species': 'Lion',
         'days': [ 'bad' ],
      } ),
      encoding='utf-8' )

   with pytest.raises( ValueError, match='to be an object' ):
      JsonSeedLoader.load_day_curve_file(
         path,
         entity_fields=[ 'species' ],
         day_fields=[ 'day' ] )

def Test_LoadDayCurveFile_TestMissingDayField_ExpectValueError(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( {
         'species': 'Lion',
         'days': [ { 'day': 1 } ],
      } ),
      encoding='utf-8' )

   with pytest.raises( ValueError, match="Missing 'value'" ):
      JsonSeedLoader.load_day_curve_file(
         path,
         entity_fields=[ 'species' ],
         day_fields=[ 'day', 'value' ] )

def Test_LoadDayCurveDirectory_TestMultipleFiles_ExpectSortedCombinedRows(
      tmp_path: Path ) -> None:
   first = tmp_path / 'a.json'
   second = tmp_path / 'b.json'
   first.write_text(
      json.dumps( {
         'name': 'A',
         'days': [ { 'day': 1, 'value': 1 } ],
      } ),
      encoding='utf-8' )
   second.write_text(
      json.dumps( {
         'name': 'B',
         'days': [ { 'day': 2, 'value': 2 } ],
      } ),
      encoding='utf-8' )

   assert JsonSeedLoader.load_day_curve_directory(
      tmp_path,
      entity_fields=[ 'name' ],
      day_fields=[ 'day', 'value' ] ) == [
      [ 'A', 1, 1 ],
      [ 'B', 2, 2 ],
   ]

def Test_InsertRows_TestEmptyRows_ExpectNoExecutemany() -> None:
   stub, cursor = _cursor()

   JsonSeedLoader.insert_rows(
      cursor,
      table='Animal',
      columns=[ 'SPECIES' ],
      rows=[] )

   assert stub.executemany_calls == []

def Test_InsertRows_TestMismatchedRowLength_ExpectValueError() -> None:
   _stub, cursor = _cursor()

   with pytest.raises( ValueError, match='must have 2 values' ):
      JsonSeedLoader.insert_rows(
         cursor,
         table='Animal',
         columns=[ 'SPECIES', 'EXHIBIT' ],
         rows=[ [ 'Lion' ] ] )

def Test_InsertRows_TestValidRows_ExpectExecutemany() -> None:
   stub, cursor = _cursor()

   JsonSeedLoader.insert_rows(
      cursor,
      table='Animal',
      columns=[ 'SPECIES', 'EXHIBIT' ],
      rows=[ [ 'Lion', 'Africa' ] ] )

   assert len( stub.executemany_calls ) == 1
   sql, rows = stub.executemany_calls[ 0 ]
   assert 'INSERT INTO Animal' in sql
   assert rows == [ [ 'Lion', 'Africa' ] ]

def Test_InsertJsonRows_TestPath_ExpectInserted(
      tmp_path: Path ) -> None:
   path = tmp_path / 'rows.json'
   path.write_text( json.dumps( [ [ 'Lion', 'Africa' ] ] ), encoding='utf-8' )
   stub, cursor = _cursor()

   JsonSeedLoader.insert_json_rows(
      cursor,
      table='Animal',
      columns=[ 'SPECIES', 'EXHIBIT' ],
      path=path )

   assert stub.executemany_calls[ 0 ][ 1 ] == [ [ 'Lion', 'Africa' ] ]

def Test_InsertJsonRecords_TestPath_ExpectInserted(
      tmp_path: Path ) -> None:
   path = tmp_path / 'records.json'
   path.write_text(
      json.dumps( [ { 'species': 'Lion', 'exhibit': 'Africa' } ] ),
      encoding='utf-8' )
   stub, cursor = _cursor()

   JsonSeedLoader.insert_json_records(
      cursor,
      table='Animal',
      columns=[ 'SPECIES', 'EXHIBIT' ],
      fields=[ 'species', 'exhibit' ],
      path=path )

   assert stub.executemany_calls[ 0 ][ 1 ] == [ [ 'Lion', 'Africa' ] ]

def Test_InsertDayCurveFile_TestPath_ExpectInserted(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( {
         'species': 'Lion',
         'days': [ { 'day': 1, 'value': 0.5 } ],
      } ),
      encoding='utf-8' )
   stub, cursor = _cursor()

   JsonSeedLoader.insert_day_curve_file(
      cursor,
      table='AnimalCurve',
      columns=[ 'SPECIES', 'DAY', 'VALUE' ],
      path=path,
      entity_fields=[ 'species' ],
      day_fields=[ 'day', 'value' ] )

   assert stub.executemany_calls[ 0 ][ 1 ] == [ [ 'Lion', 1, 0.5 ] ]

def Test_InsertDayCurveDirectory_TestDirectory_ExpectInserted(
      tmp_path: Path ) -> None:
   path = tmp_path / 'curve.json'
   path.write_text(
      json.dumps( {
         'species': 'Lion',
         'days': [ { 'day': 1, 'value': 0.5 } ],
      } ),
      encoding='utf-8' )
   stub, cursor = _cursor()

   JsonSeedLoader.insert_day_curve_directory(
      cursor,
      table='AnimalCurve',
      columns=[ 'SPECIES', 'DAY', 'VALUE' ],
      directory=tmp_path,
      entity_fields=[ 'species' ],
      day_fields=[ 'day', 'value' ] )

   assert stub.executemany_calls[ 0 ][ 1 ] == [ [ 'Lion', 1, 0.5 ] ]
