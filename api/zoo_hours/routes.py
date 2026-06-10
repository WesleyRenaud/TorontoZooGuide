from __future__ import annotations

from .controllers.zoo_hours_controller import ZooHoursController
from ..json_handler import PostRouteHandler


ZOO_HOURS_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-zoo-hours': ZooHoursController.get_zoo_hours,
}
