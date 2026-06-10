from __future__ import annotations

from .controllers.restroom_controller import RestroomController
from ..json_handler import PostRouteHandler


RESTROOM_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-restrooms': RestroomController.get_restrooms,
   '/get-restroom-names': RestroomController.get_restroom_names,
   '/set-restroom-closed': RestroomController.set_restroom_closed,
   '/set-restroom-open': RestroomController.set_restroom_open,
   '/set-restroom-alert': RestroomController.set_restroom_alert,
   '/remove-restroom-alert': RestroomController.remove_restroom_alert,
}
