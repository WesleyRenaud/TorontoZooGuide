from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote
from urllib.parse import urlparse

from .json_handler_mixin import JsonHandlerMixin
from .request_connection_provider import RequestConnectionProvider
from .routes.get_route_registry import GetRouteRegistry
from .routes.post_route_registry import PostRouteRegistry
from .static.static_file_handler_mixin import StaticFileHandlerMixin
from .static.static_page_routes import StaticPageRoutes


class HttpRequestHandler( JsonHandlerMixin, StaticFileHandlerMixin, BaseHTTPRequestHandler ):
   def do_GET( self ) -> None:
      parsed = urlparse( self.path )
      path = unquote( parsed.path )

      route = GetRouteRegistry.ROUTES.get( path )

      if route is not None:
         route( self )
         return

      for prefix, prefix_route in StaticPageRoutes.PREFIX_ROUTES.items():
         if path.startswith( prefix ):
            prefix_route( self )
            return

      self.send_error( 404, "Not Found" )


   @RequestConnectionProvider.with_db_connection
   def do_POST( self ) -> None:
      route = PostRouteRegistry.ROUTES.get( self.path )

      if route is not None:
         route( self )
         return

      self.send_error( 404, "Not Found" )
