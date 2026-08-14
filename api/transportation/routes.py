from __future__ import annotations

from .controllers.transportation_controller import TransportationController
from ..json_handler import PostRouteHandler


TRANSPORTATION_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-transportation-routes': TransportationController.get_transportation_routes,
}
