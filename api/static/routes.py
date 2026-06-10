from __future__ import annotations

from ..json_handler import GetRouteHandler
from ..json_handler import StaticRequestHandler


def _serve_page(
      handler: StaticRequestHandler,
      filepath: str ) -> None:
   handler._send_file( filepath, "text/html" )


def _serve_project_path( handler: StaticRequestHandler ) -> None:
   handler._send_file( '.' + handler.path )


STATIC_PAGE_ROUTES: dict[ str, GetRouteHandler ] = {
   '/map.html': lambda handler: _serve_page( handler, './pages/map.html' ),
   '/animals.html': lambda handler: _serve_page( handler, './pages/animals.html' ),
   '/itinerary.html': lambda handler: _serve_page( handler, './pages/itinerary.html' ),
   '/console-operations.html': lambda handler: _serve_page( handler, './pages/console-operations.html' ),
}

STATIC_PREFIX_ROUTES: dict[ str, GetRouteHandler ] = {
   '/styles/': _serve_project_path,
   '/scripts/': _serve_project_path,
   '/images/': _serve_project_path,
}
