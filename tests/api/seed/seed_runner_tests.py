from __future__ import annotations

import runpy
import sqlite3

import pytest

from api.seed.seed_runner import SeedRunner

def Test_ApplySchema_TestMonkeypatchedConnect_ExpectSchemaMigrateCommit(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   calls: list[ str ] = []
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   class _Conn:
      def cursor( self ) -> sqlite3.Cursor:
         calls.append( 'cursor' )
         return cursor


      def commit( self ) -> None:
         calls.append( 'commit' )


      def close( self ) -> None:
         calls.append( 'close' )

   monkeypatch.setattr(
      'api.seed.seed_runner.sqlite3.connect',
      lambda db_path: _Conn() )
   monkeypatch.setattr(
      'api.seed.seed_runner.SchemaCreator.create',
      lambda cur: calls.append( 'schema' ) )
   monkeypatch.setattr(
      'api.seed.seed_runner.MigrationRunner.run_on_cursor',
      lambda cur, *, skip_before: calls.append( f'migrate:{ skip_before }' ) )

   SeedRunner.apply_schema( db_path=':memory:' )

   assert calls == [
      'cursor',
      'schema',
      'migrate:011_runtime_schema_column_additions.sql',
      'commit',
      'close',
   ]
   conn.close()

def Test_ApplySeedData_TestMonkeypatchedConnect_ExpectSeedCommit(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   calls: list[ str ] = []
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   class _Conn:
      def cursor( self ) -> sqlite3.Cursor:
         calls.append( 'cursor' )
         return cursor


      def commit( self ) -> None:
         calls.append( 'commit' )


      def close( self ) -> None:
         calls.append( 'close' )

   monkeypatch.setattr(
      'api.seed.seed_runner.sqlite3.connect',
      lambda db_path: _Conn() )
   monkeypatch.setattr(
      'api.seed.seed_runner.StaticDataSeeder.seed',
      lambda cur: calls.append( 'seed' ) )

   SeedRunner.apply_seed_data( db_path=':memory:' )

   assert calls == [ 'cursor', 'seed', 'commit', 'close' ]
   conn.close()

def Test_Main_TestMonkeypatchedConnect_ExpectSchemaMigrateSeedCommit(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   class _Conn:
      def cursor( self ) -> sqlite3.Cursor:
         calls.append( 'cursor' )
         return cursor


      def commit( self ) -> None:
         calls.append( 'commit' )


      def close( self ) -> None:
         calls.append( 'close' )

   monkeypatch.setattr(
      'api.seed.seed_runner.sqlite3.connect',
      lambda db_path: _Conn() )
   monkeypatch.setattr(
      'api.seed.seed_runner.SchemaCreator.create',
      lambda cur: calls.append( 'schema' ) )
   monkeypatch.setattr(
      'api.seed.seed_runner.MigrationRunner.run_on_cursor',
      lambda cur, *, skip_before: calls.append( f'migrate:{ skip_before }' ) )
   monkeypatch.setattr(
      'api.seed.seed_runner.StaticDataSeeder.seed',
      lambda cur: calls.append( 'seed' ) )

   SeedRunner.main( db_path=':memory:' )

   assert calls == [
      'cursor',
      'schema',
      'migrate:011_runtime_schema_column_additions.sql',
      'seed',
      'commit',
      'close',
   ]
   assert 'Database schema and seed data applied successfully.' in capsys.readouterr().out
   conn.close()

def Test_ModuleMain_TestMonkeypatchedConnect_ExpectSchemaMigrateSeedCommit(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []
   conn = sqlite3.connect( ':memory:' )
   cursor = conn.cursor()

   class _Conn:
      def cursor( self ) -> sqlite3.Cursor:
         calls.append( 'cursor' )
         return cursor


      def commit( self ) -> None:
         calls.append( 'commit' )


      def close( self ) -> None:
         calls.append( 'close' )

   monkeypatch.setattr(
      'api.seed.seed_runner.sqlite3.connect',
      lambda db_path: _Conn() )
   monkeypatch.setattr(
      'api.seed.seed_runner.SchemaCreator.create',
      lambda cur: calls.append( 'schema' ) )
   monkeypatch.setattr(
      'api.seed.seed_runner.MigrationRunner.run_on_cursor',
      lambda cur, *, skip_before: calls.append( f'migrate:{ skip_before }' ) )
   monkeypatch.setattr(
      'api.seed.seed_runner.StaticDataSeeder.seed',
      lambda cur: calls.append( 'seed' ) )

   runpy.run_module( 'api.seed.seed_runner', run_name='__main__' )

   assert calls == [
      'cursor',
      'schema',
      'migrate:011_runtime_schema_column_additions.sql',
      'seed',
      'commit',
      'close',
   ]
   assert 'Database schema and seed data applied successfully.' in capsys.readouterr().out
   conn.close()
