from __future__ import annotations

from io import BytesIO
import json
from typing import Any


class FakeHandler():
   path: str
   headers: dict[ str, str ] | None
   rfile: BytesIO
   wfile: BytesIO
   statuses: list[ int ]
   sent_headers: list[ tuple[ str, str ] ]
   ended: bool
   errors: list[ tuple[ int, str | None ] ]
   files: list[ tuple[ str, str | None ] ]


   def __init__(
         self,
         path: str = '/',
         body: dict[ str, Any ] | None = None,
         headers: dict[ str, str ] | None = None ) -> None:
      self.path = path
      self.headers = headers or {}
      self.rfile = BytesIO( json.dumps( body or {} ).encode( 'utf-8' ) )
      self.wfile = BytesIO()
      self.statuses = []
      self.sent_headers = []
      self.ended = False
      self.errors = []
      self.files = []


   def send_response( self, code: int ) -> None:
      self.statuses.append( code )


   def send_header( self, name: str, value: str ) -> None:
      self.sent_headers.append( ( name, value ) )


   def end_headers( self ) -> None:
      self.ended = True


   def send_error( self, code: int, message: str | None = None ) -> None:
      self.errors.append( ( code, message ) )
      self.statuses.append( code )
