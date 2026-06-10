from __future__ import annotations

from .controllers.drinking_fountain_controller import DrinkingFountainController
from ..json_handler import PostRouteHandler


DRINKING_FOUNTAIN_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-drinking-fountains': DrinkingFountainController.get_drinking_fountains,
   '/set-drinking-fountains-closed': DrinkingFountainController.set_drinking_fountains_closed,
   '/set-drinking-fountains-open': DrinkingFountainController.set_drinking_fountains_open,
}
