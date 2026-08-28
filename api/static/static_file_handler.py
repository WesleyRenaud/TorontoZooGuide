from __future__ import annotations

from typing import Any, Protocol


class StaticFileHandler( Protocol ):
   def send_response( self, code: int, message: str | None = None ) -> None:
      ...


   def send_header( self, keyword: str, value: str ) -> None:
      ...


   def end_headers( self ) -> None:
      ...


   def send_error( self, code: int, message: str | None = None ) -> None:
      ...


   wfile: Any
