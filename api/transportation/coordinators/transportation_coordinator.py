from __future__ import annotations

from datetime import date

from ..data_access.active_route import fetch_active_transportation_route
from ..data_access.active_route import fetch_transportation_day_route
from ..data_access.active_route import fetch_transportation_route_ids
from ..data_access.active_route import fetch_transportation_route_station_names
from ..data_access.route_schedule import save_current_transportation_route_schedule
from ..data_access.station_status import save_transportation_station_closed_status
from ..data_access.station_status import save_transportation_station_open_status
from ..data_access.transportation import fetch_transportation_records
from ..data_access.transportation_route import fetch_transportation_routes_by_name
from ..data_access.transportation_station import fetch_transportation_station_names
from ..data_access.transportation_station import fetch_transportation_station_records
from ..data_access.transportation_station import fetch_transportation_station_status_records
from ..domain.active_transportation_route import build_active_transportation_route_response
from ..domain.active_transportation_route import is_valid_transportation_route
from ..domain.active_transportation_route import resolve_requested_transportation_route
from ..domain.active_transportation_route import resolve_transportation_route_context
from ..domain.route_stations import build_route_transportation_stations
from ..domain.route_stations import resolve_transportation_station_context
from ..domain.transportation import build_transportations
from ..domain.transportation_route import group_transportation_routes
from ...models import TransportationStation
from ...models.active_transportation_route import ActiveTransportationRoute
from ...models.transportation import Transportation
from ...request_connection import get_connection
from ..scheduling.route_schedule import build_current_transportation_route_schedule
from ..search.transportation_stations_matching_query import build_transportation_stations_matching_query
from ..search.transportations_matching_query import build_transportations_matching_query
from ...shared.enums.transportation_name import TransportationName
from ...shared.opening_schedule_visit_context import resolve_opening_schedule_visit_context
from ..status.station_status import build_transportation_station_closed_status
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class TransportationCoordinator():
   @classmethod
   def get_transportations(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ Transportation ]:
      context = resolve_opening_schedule_visit_context(
         day=day,
         month=month,
         year=year )

      return build_transportations(
         fetch_transportation_records(
            get_connection(),
            visit_date=context.target_date ),
         context=context )


   @classmethod
   def get_transportations_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ Transportation ]:
      return build_transportations_matching_query(
         cls.get_transportations(
            day=day,
            month=month,
            year=year ),
         query )


   @classmethod
   def get_transportation_routes( cls ) -> list[ dict[ str, object ] ]:
      return group_transportation_routes(
         fetch_transportation_routes_by_name( get_connection() ) )


   @classmethod
   def get_transportation_station_names(
         cls,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ str ]:
      return fetch_transportation_station_names(
         get_connection(),
         transportation )


   @classmethod
   def get_transportation_route_ids(
         cls,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ str ]:
      return fetch_transportation_route_ids(
         get_connection(),
         transportation )


   @classmethod
   def get_transportation_stations(
         cls,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         transportation_stations_to_include: list[ str ] | None = None,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ TransportationStation ]:

      return build_route_transportation_stations(
         station_records=fetch_transportation_station_records(
            get_connection(),
            transportation ),
         status_records=fetch_transportation_station_status_records(
            get_connection(),
            transportation ),
         context=resolve_transportation_station_context(
            route=route,
            stations_on_route=fetch_transportation_route_station_names(
               get_connection(),
               transportation,
               route=route ),
            day=day,
            month=month,
            year=year,
            transportation_stations_to_include=transportation_stations_to_include ) )


   @classmethod
   def get_transportation_stations_matching_query(
         cls,
         query: str,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ TransportationStation ]:

      route_context = resolve_transportation_route_context(
         day=day,
         month=month,
         year=year )
      valid_routes = cls.get_transportation_route_ids( transportation )
      resolved_route, _ = resolve_requested_transportation_route(
         route,
         fetch_active_transportation_route(
            get_connection(),
            transportation,
            target_date=route_context.target_date ),
         fetch_transportation_day_route(
            get_connection(),
            transportation,
            month=route_context.normalized_month,
            day=route_context.normalized_day ),
         valid_routes )
      transportation_stations = cls.get_transportation_stations(
         route=resolved_route,
         day=day,
         month=month,
         year=year,
         transportation=transportation )

      return build_transportation_stations_matching_query(
         transportation_stations,
         query )


   @classmethod
   def get_transportation_route(
         cls,
         route: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         transportation_stations_to_include: list[ str ] | None = None,
         transportation: str = TransportationName.ZOOMOBILE ) -> ActiveTransportationRoute:

      route_context = resolve_transportation_route_context(
         day=day,
         month=month,
         year=year )
      valid_routes = cls.get_transportation_route_ids( transportation )
      resolved_route, route_source = resolve_requested_transportation_route(
         route,
         fetch_active_transportation_route(
            get_connection(),
            transportation,
            target_date=route_context.target_date ),
         fetch_transportation_day_route(
            get_connection(),
            transportation,
            month=route_context.normalized_month,
            day=route_context.normalized_day ),
         valid_routes )

      return build_active_transportation_route_response(
         route=resolved_route,
         route_source=route_source,
         transportation_stations=cls.get_transportation_stations(
            route=resolved_route,
            day=route_context.normalized_day,
            month=route_context.normalized_month,
            year=route_context.target_date.year,
            transportation_stations_to_include=transportation_stations_to_include,
            transportation=transportation ) )


   @classmethod
   def get_active_transportation_route(
         cls,
         target_date: date,
         transportation: str = TransportationName.ZOOMOBILE ) -> str | None:
      route = fetch_active_transportation_route(
         get_connection(),
         transportation,
         target_date=target_date )

      if not is_valid_transportation_route(
            route,
            cls.get_transportation_route_ids( transportation ) ):
         return None

      return route


   @classmethod
   def get_transportation_day_route(
         cls,
         month: MonthInput,
         day: VisitDay,
         transportation: str = TransportationName.ZOOMOBILE ) -> str | None:
      route = fetch_transportation_day_route(
         get_connection(),
         transportation,
         month=month,
         day=day )

      if not is_valid_transportation_route(
            route,
            cls.get_transportation_route_ids( transportation ) ):
         return None

      return route


   @classmethod
   def set_transportation_station_as_closed(
         cls,
         transportation_station: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str,
         transportation: str = TransportationName.ZOOMOBILE ) -> bool:
      status = build_transportation_station_closed_status(
         transportation_station=transportation_station,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_transportation_station_closed_status(
         get_connection(),
         transportation,
         status=status )


   @classmethod
   def set_transportation_station_as_open(
         cls,
         transportation_station: str,
         transportation: str = TransportationName.ZOOMOBILE ) -> bool:
      return save_transportation_station_open_status(
         get_connection(),
         transportation,
         transportation_station=transportation_station )


   @classmethod
   def set_current_transportation_route(
         cls,
         route: str,
         start_date: DateInput,
         end_date: DateInput,
         transportation: str = TransportationName.ZOOMOBILE ) -> bool:
      if not is_valid_transportation_route(
            route,
            cls.get_transportation_route_ids( transportation ) ):
         return False

      schedule = build_current_transportation_route_schedule(
         route=route,
         start_date=start_date,
         end_date=end_date )

      return save_current_transportation_route_schedule(
         get_connection(),
         transportation,
         schedule=schedule )
