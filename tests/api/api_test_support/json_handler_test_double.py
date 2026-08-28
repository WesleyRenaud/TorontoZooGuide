from __future__ import annotations

from io import BytesIO
import json
from typing import Any


class JsonHandlerTestDouble():
   def __init__( self, body: dict[ str, Any ] | None = None ) -> None:
      encoded = json.dumps( body or {} ).encode( 'utf-8' )
      self.headers = { 'Content-Length': str( len( encoded ) ) }
      self.rfile = BytesIO( encoded )
      self.wfile = BytesIO()
      self.statuses: list[ int ] = []
      self.sent_headers: list[ tuple[ str, str ] ] = []


   def send_response( self, code: int, message: str | None = None ) -> None:
      self.statuses.append( code )


   def send_header( self, keyword: str, value: str ) -> None:
      self.sent_headers.append( ( keyword, value ) )


   def end_headers( self ) -> None:
      return None


   def _read_json_body( self ) -> dict[ str, Any ]:
      content_length = int( self.headers[ 'Content-Length' ] )
      post_data = self.rfile.read( content_length )
      return json.loads( post_data.decode( 'utf-8' ) )


   def _write_json( self, payload: Any, status: int = 200 ) -> None:
      self.send_response( status )
      self.send_header( 'Content-type', 'application/json' )
      self.end_headers()
      self.wfile.write( json.dumps( payload ).encode( 'utf-8' ) )


   def json_response( self ) -> Any:
      self.wfile.seek( 0 )
      return json.loads( self.wfile.read().decode( 'utf-8' ) )
