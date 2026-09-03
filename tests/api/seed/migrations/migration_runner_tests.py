from __future__ import annotations

from pathlib import Path
import runpy
import sqlite3
import warnings

import pytest

from api.seed.migrations.migration_runner import MigrationRunner

@pytest.fixture
def migration_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )

   yield conn

   conn.close()

def Test_EnsureMigrationTable_TestFreshDatabase_ExpectSchemaMigrationTable(
      migration_conn: sqlite3.Connection ) -> None:
   cursor = migration_conn.cursor()
   MigrationRunner.ensure_migration_table( cursor )
   tables = {
      row[ 0 ]
      for row in cursor.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }

   assert 'SchemaMigration' in tables

def Test_RunOnCursor_TestAlreadyApplied_ExpectSkipped(
      migration_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch,
      tmp_path: Path ) -> None:
   cursor = migration_conn.cursor()
   MigrationRunner.ensure_migration_table( cursor )
   cursor.execute(
      'INSERT INTO SchemaMigration ( MIGRATION_NAME ) VALUES ( ? );',
      ( '001_already_applied.sql', ),
   )
   migration_file = tmp_path / '001_already_applied.sql'
   migration_file.write_text( 'CREATE TABLE ShouldNotExist ( id INTEGER );' )
   monkeypatch.setattr(
      MigrationRunner,
      'migration_files',
      classmethod( lambda cls: [ migration_file ] ) )

   MigrationRunner.run_on_cursor( cursor )

   tables = {
      row[ 0 ]
      for row in cursor.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }
   assert 'ShouldNotExist' not in tables

def Test_RunOnCursor_TestSkipBefore_ExpectRecordedWithoutExecuting(
      migration_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch,
      tmp_path: Path ) -> None:
   cursor = migration_conn.cursor()
   migration_file = tmp_path / '001_skip_me.sql'
   migration_file.write_text( 'CREATE TABLE ShouldNotExist ( id INTEGER );' )
   monkeypatch.setattr(
      MigrationRunner,
      'migration_files',
      classmethod( lambda cls: [ migration_file ] ) )

   MigrationRunner.run_on_cursor(
      cursor,
      skip_before='999_future.sql' )

   applied = MigrationRunner.applied_migrations( cursor )
   tables = {
      row[ 0 ]
      for row in cursor.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }
   assert '001_skip_me.sql' in applied
   assert 'ShouldNotExist' not in tables

def Test_ExecuteMigrationStatement_TestUnexpectedError_ExpectReraise(
      migration_conn: sqlite3.Connection ) -> None:
   cursor = migration_conn.cursor()

   with pytest.raises( sqlite3.OperationalError ):
      MigrationRunner._execute_migration_statement(
         cursor,
         'THIS IS NOT VALID SQL' )

def Test_Run_TestConnectCommitClose_ExpectApplied(
      monkeypatch: pytest.MonkeyPatch,
      tmp_path: Path ) -> None:
   db_path = tmp_path / 'migrations.db'
   migration_file = tmp_path / '001_create_widget.sql'
   migration_file.write_text( 'CREATE TABLE Widget ( id INTEGER PRIMARY KEY );' )
   monkeypatch.setattr(
      MigrationRunner,
      'migration_files',
      classmethod( lambda cls: [ migration_file ] ) )

   MigrationRunner.run( db_path=str( db_path ) )

   conn = sqlite3.connect( db_path )
   tables = {
      row[ 0 ]
      for row in conn.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }
   applied = {
      row[ 0 ]
      for row in conn.execute(
         'SELECT MIGRATION_NAME FROM SchemaMigration;'
      ).fetchall()
   }
   conn.close()

   assert 'Widget' in tables
   assert '001_create_widget.sql' in applied

def Test_ModuleMain_TestRunInvoked_ExpectMigrationRunnerCalled(
      monkeypatch: pytest.MonkeyPatch,
      tmp_path: Path ) -> None:
   real_connect = sqlite3.connect
   db_path = tmp_path / 'animals.db'

   def connect_override( path: str ) -> sqlite3.Connection:
      if path == 'animals.db':
         return real_connect( str( db_path ) )

      return real_connect( path )

   monkeypatch.setattr( sqlite3, 'connect', connect_override )

   with warnings.catch_warnings():
      warnings.simplefilter( 'ignore', RuntimeWarning )
      runpy.run_module(
         'api.seed.migrations.migration_runner',
         run_name='__main__' )

   conn = real_connect( db_path )
   tables = {
      row[ 0 ]
      for row in conn.execute(
         "SELECT name FROM sqlite_master WHERE type = 'table';"
      ).fetchall()
   }
   conn.close()

   assert 'SchemaMigration' in tables
