from __future__ import annotations

import json
from typing import Any

from .json_request_handler import JsonRequestHandler


class JsonHandlerMixin():
   def _read_json_body( self: JsonRequestHandler ) -> dict[ str, Any ]:
      content_length = int( self.headers[ 'Content-Length' ] )
      post_data = self.rfile.read( content_length )
      return json.loads( post_data.decode( 'utf-8' ) )


   def _write_json(
         self: JsonRequestHandler,
         payload: Any,
         status: int = 200 ) -> None:
      self.send_response( status )
      self.send_header( 'Content-type', 'application/json' )
      self.end_headers()
      self.wfile.write( json.dumps( payload ).encode( 'utf-8' ) )
