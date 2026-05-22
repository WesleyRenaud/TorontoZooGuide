from datetime import date, datetime
from io import BytesIO
import json
import sqlite3

import pytest

from api.connection import close_connection
from api.connection import open_connection
from api.request_connection import clear_connection
from api.request_connection import set_connection
from api.seed.runner import main as seed_database


@pytest.fixture
def db_path( tmp_path ):
   path = tmp_path / 'animals.db'
   seed_database( db_path=str( path ) )
   return path


@pytest.fixture
def controllers( db_path ):
   conn = open_connection( db_path=str( db_path ) )
   set_connection( conn )

   class DbControllers:
      def __init__( self, connection ):
         self.conn = connection
         self._closed = False


      def close( self ):
         if self._closed:
            return

         close_connection( self.conn )
         clear_connection()
         self.conn = None
         self._closed = True

   fixture = DbControllers( conn )

   try:
      yield fixture
   finally:
      fixture.close()


@pytest.fixture
def db( controllers ):
   return controllers


@pytest.fixture
def cursor( controllers ):
   cur = controllers.conn.cursor()

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
   frozen_datetime_targets = ( 'api.zoo_util.datetime', )

   def freeze( value ):
      FrozenDateTime.frozen_now = datetime.combine( value, datetime.min.time() )

      for target in frozen_datetime_targets:
         monkeypatch.setattr( target, FrozenDateTime )

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
