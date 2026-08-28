from __future__ import annotations

from .controllers.drinking_fountain_controller import DrinkingFountainController
from ..json_request_handler import PostRouteHandler


class DrinkingFountainRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-drinking-fountains': DrinkingFountainController.get_drinking_fountains,
   '/set-drinking-fountains-closed': DrinkingFountainController.set_drinking_fountains_closed,
   '/set-drinking-fountains-open': DrinkingFountainController.set_drinking_fountains_open,
}

