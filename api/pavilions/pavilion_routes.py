from __future__ import annotations

from .controllers.pavilion_controller import PavilionController
from ..json_request_handler import PostRouteHandler


class PavilionRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-pavilions': PavilionController.get_pavilions,
}

