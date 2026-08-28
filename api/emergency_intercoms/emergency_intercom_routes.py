from __future__ import annotations

from .controllers.emergency_intercom_controller import EmergencyIntercomController
from ..json_request_handler import PostRouteHandler


class EmergencyIntercomRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-emergency-intercoms': EmergencyIntercomController.get_emergency_intercoms,
}

