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

   assert station.name == record.name
   assert station.description == record.description
   assert station.x_coord == record.x_coord
   assert station.y_coord == record.y_coord
