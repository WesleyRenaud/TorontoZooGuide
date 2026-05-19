from ... import zoo
from ...shared.enums.zoomobile_route import ZoomobileRouteId
from .zoomobile_station_context import ZoomobileStationContext


def resolve_zoomobile_station_context(
      route,
      year,
      month,
      day,
      zoomobile_stations_to_include=None ):

   target_date = zoo.ZooUtil.visit_target_date(
      month=month,
      day=day,
      year=year )

   return ZoomobileStationContext(
      route=route,
      target_date=target_date,
      zoomobile_stations_to_include=zoomobile_stations_to_include or [] )


def group_zoomobile_station_status_records_by_station( status_records ):
   status_records_by_station = {}

   for status_record in status_records:
      if status_record.zoomobile_station not in status_records_by_station:
         status_records_by_station[ status_record.zoomobile_station ] = []

      status_records_by_station[ status_record.zoomobile_station ].append( status_record )

   return status_records_by_station


def is_zoomobile_station_on_route( station_record, context ):
   return (
      context.route == ZoomobileRouteId.SUMMER
      or station_record.on_winter_route
      or station_record.name in context.zoomobile_stations_to_include
   )


def is_zoomobile_station_closed( status_records, target_date ):
   for status_record in status_records:
      is_active = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=status_record.closed_start,
         end_date_value=status_record.closed_end )

      if is_active and status_record.is_closed:
         return True

   return False


def build_zoomobile_station( station_record ):
   return zoo.ZoomobileStation(
      name=station_record.name,
      description=station_record.description,
      x_coord=station_record.x_coord,
      y_coord=station_record.y_coord )


def build_zoomobile_stations(
      station_records,
      status_records,
      context ):

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
