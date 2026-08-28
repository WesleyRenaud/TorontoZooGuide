from __future__ import annotations

from .controllers.zoo_hours_controller import ZooHoursController
from ..json_request_handler import PostRouteHandler


class ZooHoursRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-zoo-hours': ZooHoursController.get_zoo_hours,
}

