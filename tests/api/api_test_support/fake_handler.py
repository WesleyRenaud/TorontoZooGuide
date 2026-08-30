from __future__ import annotations

from io import BytesIO
import json
from typing import Any


class FakeHandler():
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
      self.files: list[ tuple[ str, str | None ] ] = []


   def send_response( self, code: int ) -> None:
      self.statuses.append( code )


   def send_header( self, name: str, value: str ) -> None:
      self.sent_headers.append( ( name, value ) )


   def end_headers( self ) -> None:
      self.ended = True


   def send_error( self, code: int, message: str | None = None ) -> None:
      self.errors.append( ( code, message ) )
      self.statuses.append( code )
