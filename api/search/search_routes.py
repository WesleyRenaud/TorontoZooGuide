from __future__ import annotations

from .controllers.search_controller import SearchController
from ..json_request_handler import PostRouteHandler


class SearchRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/search': SearchController.search,
}

