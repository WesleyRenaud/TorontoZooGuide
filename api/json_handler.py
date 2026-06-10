from __future__ import annotations

from collections.abc import Callable
import json
from typing import Any, Protocol


class JsonRequestHandler( Protocol ):
   headers: dict[ str, str ]
   rfile: Any
   wfile: Any


   def send_response( self, code: int, message: str | None = None ) -> None:
      ...


   def send_header( self, keyword: str, value: str ) -> None:
      ...


   def end_headers( self ) -> None:
      ...


   def _read_json_body( self ) -> dict[ str, Any ]:
      ...


   def _write_json( self, payload: Any, status: int = 200 ) -> None:
      ...


class StaticRequestHandler( Protocol ):
   path: str


   def _send_file(
         self,
         filepath: str,
         content_type: str | None = None ) -> None:
      ...


   def send_error( self, code: int, message: str | None = None ) -> None:
      ...


PostRouteHandler = Callable[ [ JsonRequestHandler ], None ]
GetRouteHandler = Callable[ [ StaticRequestHandler ], None ]


class JsonHandlerMixin:
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
