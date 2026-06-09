from __future__ import annotations

from .controllers.pavilion_controller import PavilionController
from ..json_handler import PostRouteHandler


PAVILION_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-pavilions': PavilionController.get_pavilions,
}
