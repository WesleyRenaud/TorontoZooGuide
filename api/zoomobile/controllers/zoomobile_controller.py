from __future__ import annotations

from datetime import date

from ..data_access.zoomobile_route_schedule import save_current_zoomobile_route_schedule
from ..data_access.zoomobile_station import fetch_active_zoomobile_route
from ..data_access.zoomobile_station import fetch_zoomobile_day_route
from ..data_access.zoomobile_station import fetch_zoomobile_station_names
from ..data_access.zoomobile_station import fetch_zoomobile_station_records
from ..data_access.zoomobile_station import fetch_zoomobile_station_status_records
from ..data_access.zoomobile_station_status import save_zoomobile_station_closed_status
from ..data_access.zoomobile_station_status import save_zoomobile_station_open_status
from ..logic.zoomobile_route import build_zoomobile_route_response
from ..logic.zoomobile_route import is_valid_zoomobile_route
from ..logic.zoomobile_route import resolve_requested_zoomobile_route
from ..logic.zoomobile_route import resolve_zoomobile_route_context
from ..logic.zoomobile_route_schedule import build_current_zoomobile_route_schedule
from ..logic.zoomobile_station import build_zoomobile_stations
from ..logic.zoomobile_station import resolve_zoomobile_station_context
from ..logic.zoomobile_station_status import build_zoomobile_station_closed_status
from ..logic.zoomobile_stations_matching_query import build_zoomobile_stations_matching_query
from ...models import ZoomobileRoute
from ...models import ZoomobileStation
from ...request_connection import get_connection
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class ZoomobileController():
   @classmethod
   def get_zoomobile_station_names( cls ) -> list[ str ]:
      return fetch_zoomobile_station_names( get_connection() )


   @classmethod
   def get_zoomobile_stations(
         cls,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         zoomobile_stations_to_include: list[ str ] | None = None ) -> list[ ZoomobileStation ]:

      return build_zoomobile_stations(
         station_records=fetch_zoomobile_station_records( get_connection() ),
         status_records=fetch_zoomobile_station_status_records( get_connection() ),
         context=resolve_zoomobile_station_context(
            route=route,
            day=day,
            month=month,
            year=year,
            zoomobile_stations_to_include=zoomobile_stations_to_include ) )


   @classmethod
   def get_zoomobile_stations_matching_query(
         cls,
         query: str,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ ZoomobileStation ]:

      route_context = resolve_zoomobile_route_context(
         day=day,
         month=month,
         year=year )
      resolved_route, _ = resolve_requested_zoomobile_route(
         route,
         fetch_active_zoomobile_route(
            get_connection(),
            target_date=route_context.target_date ),
         fetch_zoomobile_day_route(
            get_connection(),
            month=route_context.normalized_month,
            day=route_context.normalized_day ) )
      zoomobile_stations = cls.get_zoomobile_stations(
         route=resolved_route,
         day=day,
         month=month,
         year=year )

      return build_zoomobile_stations_matching_query(
         zoomobile_stations,
         query )


   @classmethod
   def get_zoomobile_route(
         cls,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         zoomobile_stations_to_include: list[ str ] | None = None ) -> ZoomobileRoute:

      route_context = resolve_zoomobile_route_context(
         day=day,
         month=month,
         year=year )
      resolved_route, route_source = resolve_requested_zoomobile_route(
         route,
         fetch_active_zoomobile_route(
            get_connection(),
            target_date=route_context.target_date ),
         fetch_zoomobile_day_route(
            get_connection(),
            month=route_context.normalized_month,
            day=route_context.normalized_day ) )

      return build_zoomobile_route_response(
         route=resolved_route,
         route_source=route_source,
         zoomobile_stations=cls.get_zoomobile_stations(
            route=resolved_route,
            day=route_context.normalized_day,
            month=route_context.normalized_month,
            year=route_context.target_date.year,
            zoomobile_stations_to_include=zoomobile_stations_to_include ) )


   @classmethod
   def get_active_zoomobile_route( cls, target_date: date ) -> str | None:
      route = fetch_active_zoomobile_route(
         get_connection(),
         target_date=target_date )

      if not is_valid_zoomobile_route( route ):
         return None

      return route


   @classmethod
   def get_zoomobile_day_route( cls, month: MonthInput, day: VisitDay ) -> str | None:
      route = fetch_zoomobile_day_route(
         get_connection(),
         month=month,
         day=day )

      if not is_valid_zoomobile_route( route ):
         return None

      return route


   @classmethod
   def set_zoomobile_station_as_closed(
         cls,
         zoomobile_station: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      status = build_zoomobile_station_closed_status(
         zoomobile_station=zoomobile_station,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_zoomobile_station_closed_status(
         get_connection(),
         status=status )


   @classmethod
   def set_zoomobile_station_as_open( cls, zoomobile_station: str ) -> bool:
      return save_zoomobile_station_open_status(
         get_connection(),
         zoomobile_station=zoomobile_station )


   @classmethod
   def set_current_zoomobile_route(
         cls,
         route: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      schedule = build_current_zoomobile_route_schedule(
         route=route,
         start_date=start_date,
         end_date=end_date )

      return save_current_zoomobile_route_schedule(
         get_connection(),
         schedule=schedule )
