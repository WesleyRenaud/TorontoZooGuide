from __future__ import annotations

from email.utils import formatdate
from email.utils import parsedate_to_datetime
import mimetypes
import os

from ..html_string_renderer import HtmlStringRenderer
from .module_preload_builder import ModulePreloadBuilder
from .static_file_handler import StaticFileHandler

class StaticFileSender():
   HTML_CACHE_CONTROL = 'no-cache'
   STATIC_CACHE_CONTROL = 'public, max-age=86400'


   @classmethod
   def send(
         cls,
         handler: StaticFileHandler,
         filepath: str,
         content_type: str | None = None ) -> None:
      if not os.path.isfile( filepath ):
         handler.send_error( 404, "Not Found" )
         return

      if not content_type:
         content_type, _ = mimetypes.guess_type( filepath )

      content_type = content_type or 'application/octet-stream'
      mtime = os.path.getmtime( filepath )
      last_modified = formatdate( mtime, usegmt=True )
      cache_control = cls.cache_control( filepath, content_type )

      if content_type == 'text/html':
         cls._send_html( handler, filepath, content_type, cache_control, last_modified, mtime )
         return

      if cls._is_not_modified( handler, mtime ):
         handler.send_response( 304 )
         cls._send_cache_headers( handler, cache_control, last_modified )
         handler.end_headers()
         return

      cls._send_file_headers(
         handler,
         content_type,
         cache_control,
         last_modified,
         os.path.getsize( filepath ) )

      with open( filepath, 'rb' ) as fp:
         while True:
            chunk = fp.read( 8192 )
            if not chunk:
               break
            handler.wfile.write( chunk )


   @classmethod
   def _send_html(
         cls,
         handler: StaticFileHandler,
         filepath: str,
         content_type: str,
         cache_control: str,
         last_modified: str,
         mtime: float ) -> None:
      with open( filepath, encoding='utf-8' ) as fp:
         rendered = HtmlStringRenderer.render( fp.read() )

      injected = ModulePreloadBuilder.inject( rendered, filepath )

      if injected == rendered and cls._is_not_modified( handler, mtime ):
         handler.send_response( 304 )
         cls._send_cache_headers( handler, cache_control, last_modified )
         handler.end_headers()
         return

      body = injected.encode( 'utf-8' )
      cls._send_file_headers( handler, content_type, cache_control, last_modified, len( body ) )
      handler.wfile.write( body )


   @classmethod
   def cache_control( cls, filepath: str, content_type: str ) -> str:
      if content_type == 'text/html' or filepath.endswith( '.html' ):
         return cls.HTML_CACHE_CONTROL

      return cls.STATIC_CACHE_CONTROL


   @classmethod
   def _send_file_headers(
         cls,
         handler: StaticFileHandler,
         content_type: str,
         cache_control: str,
         last_modified: str,
         size: int ) -> None:
      handler.send_response( 200 )
      handler.send_header( 'Content-type', content_type )
      cls._send_cache_headers( handler, cache_control, last_modified )
      handler.send_header( 'Content-Length', str( size ) )
      handler.end_headers()


   @classmethod
   def _send_cache_headers(
         cls,
         handler: StaticFileHandler,
         cache_control: str,
         last_modified: str ) -> None:
      handler.send_header( 'Cache-Control', cache_control )
      handler.send_header( 'Last-Modified', last_modified )


   @classmethod
   def _is_not_modified( cls, handler: StaticFileHandler, mtime: float ) -> bool:
      headers = getattr( handler, 'headers', None )
      if headers is None:
         return False

      raw_since = headers.get( 'If-Modified-Since' )
      if not raw_since:
         return False

      try:
         since = parsedate_to_datetime( str( raw_since ) ).timestamp()
      except ( TypeError, ValueError, OverflowError ):
         return False

      return int( mtime ) <= int( since )
