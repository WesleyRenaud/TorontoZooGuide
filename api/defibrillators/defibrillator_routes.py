from __future__ import annotations

from .controllers.defibrillator_controller import DefibrillatorController
from ..json_request_handler import PostRouteHandler


class DefibrillatorRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-defibrillators': DefibrillatorController.get_defibrillators,
}

