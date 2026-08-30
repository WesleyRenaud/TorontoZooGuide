from __future__ import annotations

from datetime import date

from api.transportation.data_access.transportation_station_record import TransportationStationRecord
from api.transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from api.transportation.domain.transportation_route_stations_builder import TransportationRouteStationsBuilder
from api.transportation.domain.transportation_station_context import TransportationStationContext


STATION_COORD = 0.0
VISIT_DATE = date( 2026, 6, 15 )
ROUTE_NAME = 'summer'


def _station_record( name: str ) -> TransportationStationRecord:
   return TransportationStationRecord(
      name=name,
      description=f'{ name } stop',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )


def _context(
      *,
      stations_on_route: list[ str ],
      transportation_stations_to_include: list[ str ] | None = None ) -> TransportationStationContext:
   return TransportationStationContext(
      route=ROUTE_NAME,
      stations_on_route=stations_on_route,
      target_date=VISIT_DATE,
      transportation_stations_to_include=transportation_stations_to_include or [] )


def Test_ResolveTransportationStationContext_TestVisitDate_ExpectNormalizedContext() -> None:
   context = TransportationRouteStationsBuilder.resolve_transportation_station_context(
      route=ROUTE_NAME,
      stations_on_route=[ 'Africa Station' ],
      year=2026,
      month=6,
      day=15,
      transportation_stations_to_include=[ 'Americas Station' ] )

   assert context.route == ROUTE_NAME
   assert context.target_date == VISIT_DATE
   assert context.stations_on_route == [ 'Africa Station' ]
   assert context.transportation_stations_to_include == [ 'Americas Station' ]


def Test_IsTransportationStationOnRoute_TestIncludedOffRouteStation_ExpectTrue() -> None:
   station_record = _station_record( 'Americas Station' )
   context = _context(
      stations_on_route=[ 'Africa Station' ],
      transportation_stations_to_include=[ 'Americas Station' ] )

   assert TransportationRouteStationsBuilder.is_transportation_station_on_route(
      station_record,
      context )


def Test_IsTransportationStationClosed_TestActiveClosure_ExpectTrue() -> None:
   status_records = [
      TransportationStationStatusRecord(
         station='Africa Station',
         closed_start='2026-06-01',
         closed_end='2026-06-30',
         is_closed=True,
         closed_message='Closed for maintenance.' ),
   ]

   assert TransportationRouteStationsBuilder.is_transportation_station_closed(
      status_records,
      VISIT_DATE )


def Test_BuildRouteTransportationStations_TestClosedOnRouteStation_ExpectExcluded() -> None:
   station_records = [
      _station_record( 'Africa Station' ),
      _station_record( 'Americas Station' ),
   ]
   status_records = [
      TransportationStationStatusRecord(
         station='Africa Station',
         closed_start='2026-06-01',
         closed_end='2026-06-30',
         is_closed=True,
         closed_message='Closed for maintenance.' ),
   ]
   context = _context( stations_on_route=[ 'Africa Station', 'Americas Station' ] )

   stations = TransportationRouteStationsBuilder.build_route_transportation_stations(
      station_records,
      status_records,
      context )

   assert [ station.name for station in stations ] == [ 'Americas Station' ]


def Test_BuildRouteTransportationStations_TestWinterRouteStationList_ExpectOffRouteStationExcluded() -> None:
   station_records = [
      _station_record( 'Africa Zoomobile Station' ),
      _station_record( 'Main Zoomobile Station' ),
   ]
   context = _context( stations_on_route=[ 'Main Zoomobile Station' ] )

   stations = TransportationRouteStationsBuilder.build_route_transportation_stations(
      station_records,
      [],
      context )

   assert [ station.name for station in stations ] == [ 'Main Zoomobile Station' ]
