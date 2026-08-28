from __future__ import annotations

from ..shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from ..shared.enums.map_item_type import MapItemType
from ..types import Types


class ItineraryTransportationStation:
   def __init__(
         self,
         name: str,
         *,
         transportation: str,
         role: ItineraryTransportationStationRole,
         description: str,
         x_coord: Types.Coordinate,
         y_coord: Types.Coordinate ) -> None:
      self.name = name
      self.transportation = transportation
      self.role = role
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'transportation': self.transportation,
         'role': self.role.value,
         'type': MapItemType.TRANSPORTATION_STATION.value,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
      }
