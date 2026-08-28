from __future__ import annotations

import mimetypes
import os

from ..html_string_renderer import HtmlStringRenderer
from .static_file_handler import StaticFileHandler

class StaticFileSender():
   @classmethod
   def send(
         cls,
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
            handler.wfile.write( HtmlStringRenderer.render( fp.read() ).encode( 'utf-8' ) )
         return

      with open( filepath, "rb" ) as fp:
         while True:
            chunk = fp.read( 8192 )
            if not chunk:
               break
            handler.wfile.write( chunk )
