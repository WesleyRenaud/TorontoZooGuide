from __future__ import annotations

from .controllers.guest_service_controller import GuestServiceController
from ..json_request_handler import PostRouteHandler


class GuestServiceRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-guest-services': GuestServiceController.get_guest_services,
}

