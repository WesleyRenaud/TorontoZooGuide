from __future__ import annotations

from api.transportation.data_access.transportation_route_record import TransportationRouteRecord
from api.transportation.domain.transportation_route_builder import TransportationRouteBuilder


def Test_GroupTransportationRoutes_TestMultipleTransportations_ExpectGroupedRoutes() -> None:
   route_records = [
      TransportationRouteRecord( transportation='Zoomobile', route='summer' ),
      TransportationRouteRecord( transportation='Zoomobile', route='winter' ),
      TransportationRouteRecord( transportation='Gondola', route='summer' ),
   ]

   grouped_routes = TransportationRouteBuilder.group_transportation_routes( route_records )

   assert grouped_routes == [
      {
         'name': 'Zoomobile',
         'routes': [ 'summer', 'winter' ],
      },
      {
         'name': 'Gondola',
         'routes': [ 'summer' ],
      },
   ]
