from __future__ import annotations

from api.models.transportation_station import TransportationStation


def Test_ToDict_TestStationFields_ExpectFrontendShape() -> None:
   assert TransportationStation(
      name='Station',
      description='Stop',
      x_coord=1.0,
      y_coord=2.0,
   ).to_dict()[ 'name' ] == 'Station'
