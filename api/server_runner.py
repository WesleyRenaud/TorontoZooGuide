from __future__ import annotations

from http.server import ThreadingHTTPServer

from .http_request_handler import HttpRequestHandler

class ServerRunner():
   DEFAULT_PORT = 8000

   @classmethod
   def run( cls, port: int = DEFAULT_PORT ) -> None:
      httpd = ThreadingHTTPServer( ( 'localhost', port ), HttpRequestHandler )
      print( 'Server listening on port: ', port )
      httpd.serve_forever()
