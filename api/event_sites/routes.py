from __future__ import annotations

from .controllers.event_site_controller import EventSiteController
from ..json_handler import PostRouteHandler


EVENT_SITE_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-event-sites': EventSiteController.get_event_sites,
}
