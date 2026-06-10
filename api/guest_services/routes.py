from __future__ import annotations

from .controllers.guest_service_controller import GuestServiceController
from ..json_handler import PostRouteHandler


GUEST_SERVICE_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-guest-services': GuestServiceController.get_guest_services,
}
