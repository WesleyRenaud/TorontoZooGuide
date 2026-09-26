from __future__ import annotations

from api.transportation.data_access.transportation_route_record import TransportationRouteRecord
from api.transportation.domain.transportation_route_builder import TransportationRouteBuilder


def Test_GroupTransportationRoutes_TestMultipleTransportations_ExpectGroupedRoutes() -> None:
   zoomobile_summer = TransportationRouteRecord( transportation='Zoomobile', route='summer' )
   zoomobile_winter = TransportationRouteRecord( transportation='Zoomobile', route='winter' )
   gondola_summer = TransportationRouteRecord( transportation='Gondola', route='summer' )
   route_records = [ zoomobile_summer, zoomobile_winter, gondola_summer ]

   grouped_routes = TransportationRouteBuilder.group_transportation_routes( route_records )

   assert grouped_routes == [
      {
         'name': zoomobile_summer.transportation,
         'routes': [ zoomobile_summer.route, zoomobile_winter.route ],
      },
      {
         'name': gondola_summer.transportation,
         'routes': [ gondola_summer.route ],
      },
   ]
