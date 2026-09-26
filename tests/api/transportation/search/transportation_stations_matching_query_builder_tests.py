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
   africa_station = _station( 'Africa Station' )
   americas_station = _station( 'Americas Station' )
   stations = [ africa_station, americas_station ]
   query = 'africa'

   matches = TransportationStationsMatchingQueryBuilder.build( stations, query )

   assert [ station.name for station in matches ] == [ africa_station.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingStationOnly() -> None:
   africa_station = _station( 'Africa Station' )
   americas_station = _station( 'Americas Station' )
   stations = [ africa_station, americas_station ]
   query = 'americas'

   matches = TransportationStationsMatchingQueryBuilder.filter_matching_query(
      stations,
      query )

   assert [ station.name for station in matches ] == [ americas_station.name ]
