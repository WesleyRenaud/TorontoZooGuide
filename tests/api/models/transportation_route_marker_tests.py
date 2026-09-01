from __future__ import annotations

from api.models.transportation_route_marker import TransportationRouteMarker


def Test_ToDict_TestRouteType_ExpectFrontendShape() -> None:
   assert TransportationRouteMarker( route_type='summer', x_coord=1, y_coord=2 ).to_dict()[ 'route_type' ] == 'summer'
