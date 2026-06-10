from __future__ import annotations

from ..json_handler import GetRouteHandler


GET_ROUTES: dict[ str, GetRouteHandler ] = {}


def register_get_routes( routes: dict[ str, GetRouteHandler ] ) -> None:
   GET_ROUTES.update( routes )
