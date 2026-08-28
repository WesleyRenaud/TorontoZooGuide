from __future__ import annotations

from datetime import date

from ..data_access.transportation_active_route_provider import TransportationActiveRouteProvider
from ..data_access.transportation_provider import TransportationProvider
from ..data_access.transportation_route_provider import TransportationRouteProvider
from ..data_access.transportation_route_schedule_provider import TransportationRouteScheduleProvider
from ..data_access.transportation_station_provider import TransportationStationProvider
from ..data_access.transportation_station_status_provider import TransportationStationStatusProvider
from ..domain.active_transportation_route_builder import ActiveTransportationRouteBuilder
from ..domain.transportation_builder import TransportationBuilder
from ..domain.transportation_route_builder import TransportationRouteBuilder
from ..domain.transportation_route_stations_builder import TransportationRouteStationsBuilder
from ...models import TransportationStation
from ...models.active_transportation_route import ActiveTransportationRoute
from ...models.transportation import Transportation
from ...request_connection import get_connection
from ..scheduling.transportation_current_route_schedule_builder import TransportationCurrentRouteScheduleBuilder
from ..search.transportation_stations_matching_query_builder import TransportationStationsMatchingQueryBuilder
from ..search.transportations_matching_query_builder import TransportationsMatchingQueryBuilder
from ...shared.enums.transportation_name import TransportationName
from ...shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver
from ..status.transportation_station_status_builder import TransportationStationStatusBuilder
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class TransportationCoordinator():
   @classmethod
   def get_transportations(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> list[ Transportation ]:
      context = OpeningScheduleVisitContextResolver.resolve(
         day=day,
         month=month,
         year=year )

      return TransportationBuilder.build_transportations(
         TransportationProvider.fetch_transportation_records(
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
      return TransportationsMatchingQueryBuilder.build(
         cls.get_transportations(
            day=day,
            month=month,
            year=year ),
         query )


   @classmethod
   def get_transportation_routes( cls ) -> list[ dict[ str, object ] ]:
      return TransportationRouteBuilder.group_transportation_routes(
         TransportationRouteProvider.fetch_transportation_routes_by_name(
            get_connection() ) )


   @classmethod
   def get_transportation_station_names(
         cls,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ str ]:
      return TransportationStationProvider.fetch_transportation_station_names(
         get_connection(),
         transportation )


   @classmethod
   def get_transportation_route_ids(
         cls,
         transportation: str = TransportationName.ZOOMOBILE ) -> list[ str ]:
      return TransportationActiveRouteProvider.fetch_transportation_route_ids(
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

      return TransportationRouteStationsBuilder.build_route_transportation_stations(
         station_records=TransportationStationProvider.fetch_transportation_station_records(
            get_connection(),
            transportation ),
         status_records=TransportationStationStatusProvider.fetch_transportation_station_status_records(
            get_connection(),
            transportation ),
         context=TransportationRouteStationsBuilder.resolve_transportation_station_context(
            route=route,
            stations_on_route=TransportationActiveRouteProvider.fetch_transportation_route_station_names(
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

      route_context = ActiveTransportationRouteBuilder.resolve_transportation_route_context(
         day=day,
         month=month,
         year=year )
      valid_routes = cls.get_transportation_route_ids( transportation )
      resolved_route, _ = ActiveTransportationRouteBuilder.resolve_requested_transportation_route(
         route,
         TransportationActiveRouteProvider.fetch_active_transportation_route(
            get_connection(),
            transportation,
            target_date=route_context.target_date ),
         TransportationActiveRouteProvider.fetch_transportation_day_route(
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

      return TransportationStationsMatchingQueryBuilder.build(
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

      route_context = ActiveTransportationRouteBuilder.resolve_transportation_route_context(
         day=day,
         month=month,
         year=year )
      valid_routes = cls.get_transportation_route_ids( transportation )
      resolved_route, route_source = ActiveTransportationRouteBuilder.resolve_requested_transportation_route(
         route,
         TransportationActiveRouteProvider.fetch_active_transportation_route(
            get_connection(),
            transportation,
            target_date=route_context.target_date ),
         TransportationActiveRouteProvider.fetch_transportation_day_route(
            get_connection(),
            transportation,
            month=route_context.normalized_month,
            day=route_context.normalized_day ),
         valid_routes )

      return ActiveTransportationRouteBuilder.build_active_transportation_route_response(
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
      route = TransportationActiveRouteProvider.fetch_active_transportation_route(
         get_connection(),
         transportation,
         target_date=target_date )

      if not ActiveTransportationRouteBuilder.is_valid_transportation_route(
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
      route = TransportationActiveRouteProvider.fetch_transportation_day_route(
         get_connection(),
         transportation,
         month=month,
         day=day )

      if not ActiveTransportationRouteBuilder.is_valid_transportation_route(
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
      status = TransportationStationStatusBuilder.build_transportation_station_closed_status(
         transportation_station=transportation_station,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return TransportationStationStatusProvider.save_transportation_station_closed_status(
         get_connection(),
         transportation,
         status=status )


   @classmethod
   def set_transportation_station_as_open(
         cls,
         transportation_station: str,
         transportation: str = TransportationName.ZOOMOBILE ) -> bool:
      return TransportationStationStatusProvider.save_transportation_station_open_status(
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
      if not ActiveTransportationRouteBuilder.is_valid_transportation_route(
            route,
            cls.get_transportation_route_ids( transportation ) ):
         return False

      schedule = TransportationCurrentRouteScheduleBuilder.build_current_transportation_route_schedule(
         route=route,
         start_date=start_date,
         end_date=end_date )

      return TransportationRouteScheduleProvider.save_current_transportation_route_schedule(
         get_connection(),
         transportation,
         schedule=schedule )
