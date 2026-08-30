from __future__ import annotations

from api.models.transportation_station import TransportationStation
from api.transportation.search.transportation_stations_matching_query_builder import TransportationStationsMatchingQueryBuilder


STATION_COORD = 0.0


def _station( name: str ) -> TransportationStation:
   return TransportationStation(
      name=name,
      description=f'{ name } stop',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )


def Test_Build_TestMatchingQuery_ExpectMatchingStationOnly() -> None:
   stations = [
      _station( 'Africa Station' ),
      _station( 'Americas Station' ),
   ]

   matches = TransportationStationsMatchingQueryBuilder.build( stations, 'africa' )

   assert [ station.name for station in matches ] == [ 'Africa Station' ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingStationOnly() -> None:
   stations = [
      _station( 'Africa Station' ),
      _station( 'Americas Station' ),
   ]

   matches = TransportationStationsMatchingQueryBuilder.filter_matching_query(
      stations,
      'americas' )

   assert [ station.name for station in matches ] == [ 'Americas Station' ]
