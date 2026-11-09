from __future__ import annotations

from .http_request_handler import HttpRequestHandler
from .server_address import ServerAddress
from .threaded_http_server import ThreadedHttpServer

class ServerRunner():
   DEFAULT_PORT = 8000

   @classmethod
   def run( cls, port: int = DEFAULT_PORT ) -> None:
      httpd = ThreadedHttpServer( ServerAddress( 'localhost', port ), HttpRequestHandler )
      print( 'Server listening on port: ', port )
      httpd.serve_forever()
