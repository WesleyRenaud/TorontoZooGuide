from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mimetypes
import os
import re
import subprocess
import sys
from typing import Any
from urllib.parse import unquote, urlparse

from . import connection
from .request_connection import clear_connection
from .request_connection import set_connection
from .routes import POST_ROUTES


DEFAULT_PORT = 8000
STRING_EXPORT_SCRIPT = './tools/exportStringValues.mjs'
HTML_STRING_TOKEN_RE = re.compile( r'\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}' )


def _flatten_string_values(
      values: dict[ str, Any ],
      prefix: str = '' ) -> dict[ str, str ]:
   flattened = {}

   for key, value in values.items():
      path = '{}.{}'.format( prefix, key ) if prefix else key

      if isinstance( value, dict ):
         flattened.update( _flatten_string_values( value, path ) )
      else:
         flattened[ path ] = str( value )

   return flattened


def get_html_string_values() -> dict[ str, str ]:
   result = subprocess.run(
      [ 'node', STRING_EXPORT_SCRIPT ],
      check=True,
      capture_output=True,
      text=True
   )

   return _flatten_string_values( json.loads( result.stdout ) )


def render_html_strings( content: str ) -> str:
   string_values = get_html_string_values()

   def replace_token( match: re.Match[ str ] ) -> str:
      key = match.group( 1 )
      value = string_values.get( key )

      if value is None:
         return match.group( 0 )

      return html.escape( value, quote=True )

   return HTML_STRING_TOKEN_RE.sub( replace_token, content )


def with_controllers(
      handler: Callable[ ..., Any ] ) -> Callable[ ..., Any ]:
   @wraps( handler )
   def wrapped( self: MyHandler, *args: Any, **kwargs: Any ) -> Any:
      conn = connection.open_connection()

      try:
         set_connection( conn )
         return handler( self, *args, **kwargs )
      finally:
         connection.close_connection( conn )
         clear_connection()

   return wrapped


class MyHandler( BaseHTTPRequestHandler ):
   def _read_json_body( self ) -> dict[ str, Any ]:
      content_length = int( self.headers[ 'Content-Length' ] )
      post_data = self.rfile.read( content_length )
      return json.loads( post_data.decode( 'utf-8' ) )


   def _write_json( self, payload: Any, status: int = 200 ) -> None:
      self.send_response( status )
      self.send_header( 'Content-type', 'application/json' )
      self.end_headers()
      self.wfile.write( json.dumps( payload ).encode( 'utf-8' ) )


   def _send_file(
         self,
         filepath: str,
         content_type: str | None = None ) -> None:
      if not os.path.isfile( filepath ):
         self.send_error( 404, "Not Found" )
         return

      self.send_response( 200 )
      if not content_type:
         content_type, _ = mimetypes.guess_type( filepath )
      self.send_header( "Content-type", content_type or "application/octet-stream" )
      self.end_headers()

      if content_type == "text/html":
         with open( filepath, encoding='utf-8' ) as fp:
            self.wfile.write( render_html_strings( fp.read() ).encode( 'utf-8' ) )
         return

      with open( filepath, "rb" ) as fp:
         while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


   def do_GET( self ) -> None:
      parsed = urlparse( self.path )
      path = unquote( parsed.path )  # handles %20 etc

      # Pages
      if path == "/map.html":
         return self._send_file( "./pages/map.html", "text/html" )
      if path == "/animals.html":
         return self._send_file( "./pages/animals.html", "text/html" )
      if path == "/itinerary.html":
         return self._send_file( "./pages/itinerary.html", "text/html" )
      if path == "/console-operations.html":
         return self._send_file( "./pages/console-operations.html", "text/html" )

      # Static folders (serve anything inside)
      if path.startswith( "/styles/" ):
         return self._send_file( "." + path )
      if path.startswith( "/scripts/" ):
         return self._send_file( "." + path )   # serves ALL modules
      if path.startswith( "/images/" ):
         return self._send_file( "." + path )

      # Otherwise
      self.send_error( 404, "Not Found" )


   @with_controllers
   def do_POST( self ) -> None:
      route = POST_ROUTES.get( self.path )

      if route is not None:
         route( self )


if __name__ == '__main__':
   port = int( sys.argv[ 1 ] ) if len( sys.argv ) > 1 else DEFAULT_PORT
   httpd = HTTPServer( ( 'localhost', port ), MyHandler )
   print( 'Server listening on port: ', port )
   httpd.serve_forever()
