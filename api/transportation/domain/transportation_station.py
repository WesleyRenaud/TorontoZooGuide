from __future__ import annotations

from ..data_access.transportation_station_record import TransportationStationRecord
from ...models.transportation_station import TransportationStation


def build_transportation_station(
      record: TransportationStationRecord,
) -> TransportationStation:
   return TransportationStation(
      name=record.name,
      description=record.description,
      x_coord=record.x_coord,
      y_coord=record.y_coord )
