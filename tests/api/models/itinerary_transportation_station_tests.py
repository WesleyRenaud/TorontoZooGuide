from __future__ import annotations

from api.models.itinerary_transportation_station import ItineraryTransportationStation
from api.shared.enums.item_type import ItemType
from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole

def Test_ToDict_TestMainStation_ExpectSerializedFields() -> None:
   station = ItineraryTransportationStation(
      name='Main Zoomobile Station',
      transportation='Zoomobile',
      role=ItineraryTransportationStationRole.ONBOARDING,
      description='Main station',
      x_coord=1.0,
      y_coord=2.0 )

   result = station.to_dict()

   assert result[ 'name' ] == 'Main Zoomobile Station'
   assert result[ 'transportation' ] == 'Zoomobile'
   assert result[ 'role' ] == ItineraryTransportationStationRole.ONBOARDING.value
   assert result[ 'type' ] == ItemType.TRANSPORTATION_STATION.value
