from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import unquote
from urllib.parse import urlparse

from .json_handler import JsonHandlerMixin
from .request_connection import with_db_connection
from .routes import GET_ROUTES
from .routes import POST_ROUTES
from .static.file_server import StaticFileHandlerMixin
from .static.routes import STATIC_PREFIX_ROUTES


DEFAULT_PORT = 8000


class MyHandler( JsonHandlerMixin, StaticFileHandlerMixin, BaseHTTPRequestHandler ):
   def do_GET( self ) -> None:
      parsed = urlparse( self.path )
      path = unquote( parsed.path )

      route = GET_ROUTES.get( path )

      if route is not None:
         route( self )
         return

      for prefix, prefix_route in STATIC_PREFIX_ROUTES.items():
         if path.startswith( prefix ):
            prefix_route( self )
            return

      self.send_error( 404, "Not Found" )


   @with_db_connection
   def do_POST( self ) -> None:
      route = POST_ROUTES.get( self.path )

      if route is not None:
         route( self )
         return

      self.send_error( 404, "Not Found" )


def run_server( port: int = DEFAULT_PORT ) -> None:
   httpd = HTTPServer( ( 'localhost', port ), MyHandler )
   print( 'Server listening on port: ', port )
   httpd.serve_forever()
