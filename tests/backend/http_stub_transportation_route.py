from __future__ import annotations

from typing import Any

from http_support_constants import ZOOMOBILE_STATION_NAME

from api.models import TransportationStation
from api.models.active_transportation_route import ActiveTransportationRoute


class TransportationRouteStubMixin:
   def get_transportation_route( self, **kwargs: Any ) -> ActiveTransportationRoute:
         self.calls.append( ( 'get_transportation_route', kwargs ) )
         return ActiveTransportationRoute(
            route='summer',
            route_source='manual',
            transportation_stations=( TransportationStation(
               name=ZOOMOBILE_STATION_NAME,
               description='Station',
               x_coord=1.0,
               y_coord=2.0,
            ), ),
         )


   def get_transportation_stations_matching_query( self, **kwargs: Any ) -> list[ TransportationStation ]:
         self.calls.append( ( 'get_transportation_stations_matching_query', kwargs ) )
         return [ TransportationStation(
            name=ZOOMOBILE_STATION_NAME,
            description='Station',
            x_coord=1.0,
            y_coord=2.0,
         ) ]


   def get_transportation_station_names( self, **kwargs: Any ) -> list[ str ]:
         self.calls.append( ( 'get_transportation_station_names', kwargs or {} ) )
         return [ ZOOMOBILE_STATION_NAME ]
