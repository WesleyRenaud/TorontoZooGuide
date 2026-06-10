from __future__ import annotations

from .controllers.emergency_intercom_controller import EmergencyIntercomController
from ..json_handler import PostRouteHandler


EMERGENCY_INTERCOM_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-emergency-intercoms': EmergencyIntercomController.get_emergency_intercoms,
}
