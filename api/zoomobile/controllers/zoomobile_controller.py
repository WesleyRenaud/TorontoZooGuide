from ..data_access.zoomobile_station import fetch_active_zoomobile_route
from ..data_access.zoomobile_station import fetch_zoomobile_day_route
from ..data_access.zoomobile_station import fetch_zoomobile_station_records
from ..data_access.zoomobile_station import fetch_zoomobile_station_status_records
from ..logic.zoomobile_route import build_zoomobile_route_response
from ..logic.zoomobile_route import is_valid_zoomobile_route
from ..logic.zoomobile_route import resolve_zoomobile_route
from ..logic.zoomobile_route import resolve_zoomobile_route_context
from ..logic.zoomobile_station import build_zoomobile_stations
from ..logic.zoomobile_station import resolve_zoomobile_station_context


class ZoomobileController():
   def __init__( self, conn ):
      self._conn = conn


   def get_zoomobile_stations(
         self,
         route,
         month,
         day,
         zoomobile_stations_to_include=None ):

      return build_zoomobile_stations(
         station_records=fetch_zoomobile_station_records( self._conn ),
         status_records=fetch_zoomobile_station_status_records( self._conn ),
         context=resolve_zoomobile_station_context(
            route=route,
            month=month,
            day=day,
            zoomobile_stations_to_include=zoomobile_stations_to_include ) )


   def get_zoomobile_route(
         self,
         route,
         month,
         day,
         zoomobile_stations_to_include=None ):

      route_context = resolve_zoomobile_route_context(
         month=month,
         day=day )
      resolved_route, route_source = resolve_zoomobile_route(
         requested_route=route,
         active_route=fetch_active_zoomobile_route(
            self._conn,
            target_date=route_context.target_date ),
         day_route=fetch_zoomobile_day_route(
            self._conn,
            month=route_context.normalized_month,
            day=route_context.normalized_day ) )

      return build_zoomobile_route_response(
         route=resolved_route,
         route_source=route_source,
         zoomobile_stations=self.get_zoomobile_stations(
            route=resolved_route,
            month=route_context.normalized_month,
            day=route_context.normalized_day,
            zoomobile_stations_to_include=zoomobile_stations_to_include ) )


   def get_active_zoomobile_route( self, target_date ):
      route = fetch_active_zoomobile_route(
         self._conn,
         target_date=target_date )

      if not is_valid_zoomobile_route( route ):
         return None

      return route


   def get_zoomobile_day_route( self, month, day ):
      route = fetch_zoomobile_day_route(
         self._conn,
         month=month,
         day=day )

      if not is_valid_zoomobile_route( route ):
         return None

      return route
