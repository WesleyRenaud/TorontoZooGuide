from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...transportation.data_access.transportation_station_record import TransportationStationRecord
from ...types import Coordinate


def itinerary_transportation_marker_coords(
      legs: list[ ItineraryTransportationLeg ],
      attraction_coords: tuple[ Coordinate, Coordinate ] | None,
      main_station: TransportationStationRecord,
) -> tuple[ Coordinate, Coordinate ]:
   if legs or attraction_coords is None:
      return main_station.x_coord, main_station.y_coord

   return attraction_coords
