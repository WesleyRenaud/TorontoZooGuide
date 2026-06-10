from __future__ import annotations

from .controllers.search_controller import SearchController
from ..json_handler import PostRouteHandler


SEARCH_ROUTES: dict[ str, PostRouteHandler ] = {
   '/search': SearchController.search,
}
