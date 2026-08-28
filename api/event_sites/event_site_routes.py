from __future__ import annotations

from .controllers.event_site_controller import EventSiteController
from ..json_request_handler import PostRouteHandler


class EventSiteRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-event-sites': EventSiteController.get_event_sites,
}

