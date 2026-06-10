from __future__ import annotations

from .controllers.defibrillator_controller import DefibrillatorController
from ..json_handler import PostRouteHandler


DEFIBRILLATOR_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-defibrillators': DefibrillatorController.get_defibrillators,
}
