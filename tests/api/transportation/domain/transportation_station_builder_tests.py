from __future__ import annotations

from api.transportation.data_access.transportation_station_record import TransportationStationRecord
from api.transportation.domain.transportation_station_builder import TransportationStationBuilder


STATION_COORD = 1.5


def Test_BuildTransportationStation_TestRecord_ExpectMappedModel() -> None:
   record = TransportationStationRecord(
      name='Africa Station',
      description='Africa Zoomobile stop',
      x_coord=STATION_COORD,
      y_coord=STATION_COORD )

   station = TransportationStationBuilder.build_transportation_station( record )

   assert station.name == 'Africa Station'
   assert station.description == 'Africa Zoomobile stop'
   assert station.x_coord == STATION_COORD
   assert station.y_coord == STATION_COORD
