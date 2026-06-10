from __future__ import annotations

from .controllers.zoomobile_controller import ZoomobileController
from ..json_handler import PostRouteHandler


ZOOMOBILE_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-zoomobile-route': ZoomobileController.get_zoomobile_route,
   '/get-zoomobile-station-names': ZoomobileController.get_zoomobile_station_names,
   '/set-zoomobile-station-closed': ZoomobileController.set_zoomobile_station_closed,
   '/set-zoomobile-station-open': ZoomobileController.set_zoomobile_station_open,
   '/set-current-zoomobile-route': ZoomobileController.set_current_zoomobile_route,
}
