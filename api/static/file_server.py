from __future__ import annotations

import mimetypes
import os
from typing import Any, Protocol

from ..html_strings import render_html_strings


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


def send_file(
      handler: StaticFileHandler,
      filepath: str,
      content_type: str | None = None ) -> None:
   if not os.path.isfile( filepath ):
      handler.send_error( 404, "Not Found" )
      return

   handler.send_response( 200 )
   if not content_type:
      content_type, _ = mimetypes.guess_type( filepath )
   handler.send_header( "Content-type", content_type or "application/octet-stream" )
   handler.end_headers()

   if content_type == "text/html":
      with open( filepath, encoding='utf-8' ) as fp:
         handler.wfile.write( render_html_strings( fp.read() ).encode( 'utf-8' ) )
      return

   with open( filepath, "rb" ) as fp:
      while True:
         chunk = fp.read( 8192 )
         if not chunk:
            break
         handler.wfile.write( chunk )


class StaticFileHandlerMixin:
   def _send_file(
         self: StaticFileHandler,
         filepath: str,
         content_type: str | None = None ) -> None:
      send_file( self, filepath, content_type )
