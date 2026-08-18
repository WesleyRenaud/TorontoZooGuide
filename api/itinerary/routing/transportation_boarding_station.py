from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg


def boarding_station_for_transportation_legs(
      legs: list[ ItineraryTransportationLeg ],
   ) -> str | None:
   if not legs:
      return None

   return legs[ 0 ].from_station
