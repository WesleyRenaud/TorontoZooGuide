from __future__ import annotations

from ..json_handler import PostRouteHandler


POST_ROUTES: dict[ str, PostRouteHandler ] = {}


def register_post_routes( routes: dict[ str, PostRouteHandler ] ) -> None:
   POST_ROUTES.update( routes )
