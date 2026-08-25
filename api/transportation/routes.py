from __future__ import annotations

from .controllers.transportation_controller import TransportationController
from ..json_handler import PostRouteHandler


TRANSPORTATION_ROUTES: dict[ str, PostRouteHandler ] = {
   '/get-transportations': TransportationController.get_transportations,
   '/get-transportation-routes': TransportationController.get_transportation_routes,
   '/get-transportation-route': TransportationController.get_transportation_route,
   '/get-transportation-station-names': TransportationController.get_transportation_station_names,
   '/set-transportation-station-closed': TransportationController.set_transportation_station_closed,
   '/set-transportation-station-open': TransportationController.set_transportation_station_open,
   '/set-current-transportation-route': TransportationController.set_current_transportation_route,
}
