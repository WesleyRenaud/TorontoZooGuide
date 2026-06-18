from __future__ import annotations

pytest_plugins = [ 'http_support' ]

from collections.abc import Callable, Generator, Mapping
from datetime import date, datetime, tzinfo
from io import BytesIO
import json
from pathlib import Path
import sqlite3
from typing import Any

import pytest

from api import connection
from api.connection import close_connection
from api.connection import open_connection
from api.request_connection import clear_connection
from api.request_connection import set_connection
from api.seed.runner import main as seed_database
from api.types import Connection, Cursor, Row


class DbControllers:
   def __init__( self, connection: Connection ) -> None:
      self.conn: Connection | None = connection
      self._closed = False


   def close( self ) -> None:
      if self._closed:
         return

      if self.conn is not None:
         close_connection( self.conn )
      clear_connection()
      self.conn = None
      self._closed = True


@pytest.fixture
def db_path( tmp_path: Path ) -> Path:
   path = tmp_path / 'animals.db'
   seed_database( db_path=str( path ) )
   return path


@pytest.fixture
def controllers( db_path: Path ) -> Generator[ DbControllers, None, None ]:
   conn = open_connection( db_path=str( db_path ) )
   set_connection( conn )

   fixture = DbControllers( conn )

   try:
      yield fixture
   finally:
      fixture.close()


@pytest.fixture
def db( controllers: DbControllers ) -> DbControllers:
   return controllers


@pytest.fixture
def integration_db( db_path: Path, monkeypatch: pytest.MonkeyPatch ) -> Path:
   test_db_path = str( db_path )

   def open_test_connection( db_path_arg: str = 'animals.db' ) -> Connection:
      conn = sqlite3.connect( test_db_path )
      conn.row_factory = sqlite3.Row
      return conn

   monkeypatch.setattr( connection, 'open_connection', open_test_connection )
   return db_path


@pytest.fixture
def cursor( controllers: DbControllers ) -> Generator[ Cursor, None, None ]:
   assert controllers.conn is not None
   cur = controllers.conn.cursor()

   try:
      yield cur
   finally:
      cur.close()


def make_row( values: Mapping[ str, object ] ) -> Row:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   columns = ', '.join( f'? AS { key }' for key in values.keys() )
   row = conn.execute( f'SELECT { columns }', tuple( values.values() ) ).fetchone()
   conn.close()
   return row


class FrozenDateTime( datetime ):
   frozen_now: datetime = datetime( 2026, 6, 15, 9, 0, 0 )

   @classmethod
   def now( cls, tz: tzinfo | None = None ) -> datetime:
      return cls.frozen_now


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   frozen_datetime_targets = ( 'api.shared.calendar_dates.datetime', )

   def freeze( value: date ) -> None:
      FrozenDateTime.frozen_now = datetime.combine( value, datetime.min.time() )

      for target in frozen_datetime_targets:
         monkeypatch.setattr( target, FrozenDateTime )

   return freeze


class FakeHandler:
   def __init__(
         self,
         path: str = '/',
         body: dict[ str, Any ] | None = None,
         headers: dict[ str, str ] | None = None ) -> None:
      self.path = path
      self.headers = headers or {}
      self.rfile = BytesIO( json.dumps( body or {} ).encode( 'utf-8' ) )
      self.wfile = BytesIO()
      self.statuses: list[ int ] = []
      self.sent_headers: list[ tuple[ str, str ] ] = []
      self.ended = False
      self.errors: list[ tuple[ int, str | None ] ] = []


   def send_response( self, code: int ) -> None:
      self.statuses.append( code )


   def send_header( self, name: str, value: str ) -> None:
      self.sent_headers.append( ( name, value ) )


   def end_headers( self ) -> None:
      self.ended = True


   def send_error( self, code: int, message: str | None = None ) -> None:
      self.errors.append( ( code, message ) )
      self.statuses.append( code )


   def json_response( self ) -> Any:
      self.wfile.seek( 0 )
      return json.loads( self.wfile.read().decode( 'utf-8' ) )


def json_headers_for( body: dict[ str, Any ] ) -> dict[ str, str ]:
   return {
      'Content-Length': str( len( json.dumps( body ).encode( 'utf-8' ) ) )
   }
