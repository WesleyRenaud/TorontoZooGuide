from __future__ import annotations

from typing import Any

from http_support_constants import ZOOMOBILE_STATION_NAME

from api.models import ZoomobileStation
from api.models.zoomobile_route import ZoomobileRoute

class ZoomobileStubMixin:
   def get_zoomobile_route( self, **kwargs: Any ) -> ZoomobileRoute:
         self.calls.append( ( 'get_zoomobile_route', kwargs ) )
         return ZoomobileRoute(
            route='summer',
            route_source='manual',
            zoomobile_stations=( ZoomobileStation(
               name=ZOOMOBILE_STATION_NAME,
               description='Station',
               x_coord=1.0,
               y_coord=2.0,
            ), ),
         )


   def get_zoomobile_stations_matching_query( self, **kwargs: Any ) -> list[ ZoomobileStation ]:
         self.calls.append( ( 'get_zoomobile_stations_matching_query', kwargs ) )
         return [ ZoomobileStation(
            name=ZOOMOBILE_STATION_NAME,
            description='Station',
            x_coord=1.0,
            y_coord=2.0,
         ) ]


   def get_zoomobile_station_names( self ) -> list[ str ]:
         self.calls.append( ( 'get_zoomobile_station_names', {} ) )
         return [ ZOOMOBILE_STATION_NAME ]
