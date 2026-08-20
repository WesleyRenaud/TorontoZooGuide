from __future__ import annotations

from datetime import date

from ...models import TransportationStation
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...transportation.data_access.transportation_station_record import TransportationStationRecord
from ...transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from ...transportation.domain.transportation_station import build_transportation_station
from ...types import MonthInput, VisitDay, VisitYear
from .zoomobile_station_context import ZoomobileStationContext


def resolve_zoomobile_station_context(
      route: str,
      stations_on_route: list[ str ],
      year: VisitYear,
      month: MonthInput,
      day: VisitDay,
      zoomobile_stations_to_include: list[ str ] | None = None ) -> ZoomobileStationContext:

   target_date = CalendarDates.visit_target_date(
      month=month,
      day=day,
      year=year )

   return ZoomobileStationContext(
      route=route,
      stations_on_route=stations_on_route,
      target_date=target_date,
      zoomobile_stations_to_include=zoomobile_stations_to_include or [] )


def group_zoomobile_station_status_records_by_station(
      status_records: list[ TransportationStationStatusRecord ],
) -> dict[ str, list[ TransportationStationStatusRecord ] ]:
   status_records_by_station: dict[ str, list[ TransportationStationStatusRecord ] ] = {}

   for status_record in status_records:
      if status_record.station not in status_records_by_station:
         status_records_by_station[ status_record.station ] = []

      status_records_by_station[ status_record.station ].append( status_record )

   return status_records_by_station


def is_zoomobile_station_on_route(
      station_record: TransportationStationRecord,
      context: ZoomobileStationContext ) -> bool:
   return (
      station_record.name in context.stations_on_route
      or station_record.name in context.zoomobile_stations_to_include
   )


def is_zoomobile_station_closed(
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


def build_zoomobile_station(
      station_record: TransportationStationRecord ) -> TransportationStation:
   return build_transportation_station( station_record )


def build_zoomobile_stations(
      station_records: list[ TransportationStationRecord ],
      status_records: list[ TransportationStationStatusRecord ],
      context: ZoomobileStationContext ) -> list[ TransportationStation ]:

   status_records_by_station = group_zoomobile_station_status_records_by_station(
      status_records )
   zoomobile_stations = []

   for station_record in station_records:
      if not is_zoomobile_station_on_route(
            station_record=station_record,
            context=context ):
         continue

      if is_zoomobile_station_closed(
            status_records=status_records_by_station.get( station_record.name, [] ),
            target_date=context.target_date ):
         continue

      zoomobile_stations.append(
         build_zoomobile_station( station_record ) )

   return zoomobile_stations
