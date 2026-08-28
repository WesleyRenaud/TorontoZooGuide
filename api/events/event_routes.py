from __future__ import annotations

from .controllers.event_controller import EventController
from ..json_request_handler import PostRouteHandler


class EventRoutes():
   ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-events': EventController.get_events,
   '/create-event': EventController.create_event,
}

