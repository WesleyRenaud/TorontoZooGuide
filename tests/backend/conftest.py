from datetime import date, datetime
from io import BytesIO
import json
import sqlite3

import pytest

import database
from seed.runner import main as seed_database


@pytest.fixture
def db_path( tmp_path ):
   path = tmp_path / 'animals.db'
   seed_database( db_path=str( path ) )
   return path


@pytest.fixture
def db( db_path ):
   test_database = database.Database( db_path=str( db_path ) )

   try:
      yield test_database
   finally:
      test_database.close()


@pytest.fixture
def cursor( db ):
   cur = db.conn.cursor()

   try:
      yield cur
   finally:
      cur.close()


def make_row( values ):
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   columns = ', '.join( f'? AS { key }' for key in values.keys() )
   row = conn.execute( f'SELECT { columns }', tuple( values.values() ) ).fetchone()
   conn.close()
   return row


class FrozenDateTime( datetime ):
   frozen_now = datetime( 2026, 6, 15, 9, 0, 0 )

   @classmethod
   def now( cls ):
      return cls.frozen_now


@pytest.fixture
def freeze_database_today( monkeypatch ):
   def freeze( value ):
      FrozenDateTime.frozen_now = datetime.combine( value, datetime.min.time() )
      monkeypatch.setattr( database, 'datetime', FrozenDateTime )

   return freeze


class FakeHandler:
   def __init__( self, path='/', body=None, headers=None ):
      self.path = path
      self.headers = headers or {}
      self.rfile = BytesIO( json.dumps( body or {} ).encode( 'utf-8' ) )
      self.wfile = BytesIO()
      self.statuses = []
      self.sent_headers = []
      self.ended = False
      self.errors = []


   def send_response( self, code ):
      self.statuses.append( code )


   def send_header( self, name, value ):
      self.sent_headers.append( ( name, value ) )


   def end_headers( self ):
      self.ended = True


   def send_error( self, code, message=None ):
      self.errors.append( ( code, message ) )
      self.statuses.append( code )


   def json_response( self ):
      self.wfile.seek( 0 )
      return json.loads( self.wfile.read().decode( 'utf-8' ) )


def json_headers_for( body ):
   return {
      'Content-Length': str( len( json.dumps( body ).encode( 'utf-8' ) ) )
   }
