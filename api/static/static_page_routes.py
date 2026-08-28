from __future__ import annotations

from typing import ClassVar

from ..static_request_handler import GetRouteHandler
from ..static_request_handler import StaticRequestHandler


class StaticPageRoutes():
   @staticmethod
   def serve_page(
         handler: StaticRequestHandler,
         filepath: str ) -> None:
      handler._send_file( filepath, "text/html" )


   @staticmethod
   def serve_project_path( handler: StaticRequestHandler ) -> None:
      handler._send_file( '.' + handler.path )


   PAGE_ROUTES: ClassVar[ dict[ str, GetRouteHandler ] ] = {
      '/map.html': lambda handler: StaticPageRoutes.serve_page( handler, './pages/map.html' ),
      '/animals.html': lambda handler: StaticPageRoutes.serve_page( handler, './pages/animals.html' ),
      '/itinerary.html': lambda handler: StaticPageRoutes.serve_page( handler, './pages/itinerary.html' ),
      '/console-operations.html': lambda handler: StaticPageRoutes.serve_page( handler, './pages/console-operations.html' ),
   }

   PREFIX_ROUTES: ClassVar[ dict[ str, GetRouteHandler ] ] = {
      '/styles/': serve_project_path,
      '/scripts/': serve_project_path,
      '/images/': serve_project_path,
   }
