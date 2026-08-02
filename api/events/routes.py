from __future__ import annotations

from .controllers.event_controller import EventController
from ..json_handler import PostRouteHandler


EVENT_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-events': EventController.get_events,
   '/create-event': EventController.create_event,
}
