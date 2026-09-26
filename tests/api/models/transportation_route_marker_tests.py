from __future__ import annotations

from api.models.transportation_route_marker import TransportationRouteMarker


def Test_ToDict_TestRouteType_ExpectFrontendShape() -> None:
   marker = TransportationRouteMarker( route_type='summer', x_coord=1, y_coord=2 )

   result = marker.to_dict()

   assert result[ 'route_type' ] == marker.route_type
