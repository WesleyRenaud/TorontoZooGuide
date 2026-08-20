from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...types import Row


def map_itinerary_transportation_leg( row: Row ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=row[ 'FROM_STATION' ],
      to_station=row[ 'TO_STATION' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      transportation=row[ 'TRANSPORTATION' ] )


def map_itinerary_transportation_legs(
      rows: list[ Row ],
) -> list[ ItineraryTransportationLeg ]:
   return [
      map_itinerary_transportation_leg( row )
      for row in rows
   ]
