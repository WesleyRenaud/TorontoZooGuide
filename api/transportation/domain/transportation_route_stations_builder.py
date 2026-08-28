from __future__ import annotations

from datetime import date

from ..data_access.transportation_station_record import TransportationStationRecord
from ..data_access.transportation_station_status_record import TransportationStationStatusRecord
from ...models import TransportationStation
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from .transportation_station_builder import TransportationStationBuilder
from .transportation_station_context import TransportationStationContext
from ...types import Types


class TransportationRouteStationsBuilder():
   @classmethod
   def resolve_transportation_station_context(
         cls,
         route: str,
         stations_on_route: list[ str ],
         year: Types.VisitYear,
         month: Types.MonthInput,
         day: Types.VisitDay,
         transportation_stations_to_include: list[ str ] | None = None ) -> TransportationStationContext:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )
      return TransportationStationContext(
         route=route,
         stations_on_route=stations_on_route,
         target_date=target_date,
         transportation_stations_to_include=transportation_stations_to_include or [] )


   @classmethod
   def group_transportation_station_status_records_by_station(
         cls,
         status_records: list[ TransportationStationStatusRecord ],
   ) -> dict[ str, list[ TransportationStationStatusRecord ] ]:
      status_records_by_station: dict[ str, list[ TransportationStationStatusRecord ] ] = {}
      for status_record in status_records:
         if status_record.station not in status_records_by_station:
            status_records_by_station[ status_record.station ] = []
         status_records_by_station[ status_record.station ].append( status_record )
      return status_records_by_station


   @classmethod
   def is_transportation_station_on_route(
         cls,
         station_record: TransportationStationRecord,
         context: TransportationStationContext ) -> bool:
      return (
         station_record.name in context.stations_on_route
         or station_record.name in context.transportation_stations_to_include
      )


   @classmethod
   def is_transportation_station_closed(
         cls,
         status_records: list[ TransportationStationStatusRecord ],
         target_date: date ) -> bool:
      for status_record in status_records:
         is_active = DateValues.is_date_in_range(
            target_date=target_date,
            start_date_value=status_record.closed_start,
            end_date_value=status_record.closed_end )
         if is_active and status_record.is_closed:
            return True
      return False


   @classmethod
   def build_route_transportation_stations(
         cls,
         station_records: list[ TransportationStationRecord ],
         status_records: list[ TransportationStationStatusRecord ],
         context: TransportationStationContext ) -> list[ TransportationStation ]:
      status_records_by_station = cls.group_transportation_station_status_records_by_station(
         status_records )
      transportation_stations = []

      for station_record in station_records:
         if not cls.is_transportation_station_on_route(
               station_record=station_record,
               context=context ):
            continue
         if cls.is_transportation_station_closed(
               status_records=status_records_by_station.get( station_record.name, [] ),
               target_date=context.target_date ):
            continue
         transportation_stations.append(
            TransportationStationBuilder.build_transportation_station( station_record ) )

      return transportation_stations
