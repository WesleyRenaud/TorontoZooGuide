from __future__ import annotations

from dataclasses import dataclass

from ...itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation import ItineraryTransportation
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...request_connection import get_connection
from ...types import Coordinate


@dataclass( frozen=True )
class MainTransportationStation:
   name: str | None = None
   x_coord: Coordinate | None = None
   y_coord: Coordinate | None = None


def fetch_main_station_coords(
      transportation: str ) -> MainTransportationStation:
   conn = get_connection()

   if conn is None:
      return MainTransportationStation()

   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT NAME, X_COORD, Y_COORD
               FROM TransportationStation
               WHERE TRANSPORTATION = ?
                 AND IS_MAIN_STATION = 1;
         """,
         ( transportation, ),
      ).fetchone()

      if row is None:
         return MainTransportationStation()

      return MainTransportationStation(
         name=row[ 'NAME' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )

   finally:
      cur.close()


def build_itinerary_transportations(
      saved_transportations: list[ ItineraryTransportationRecord ],
) -> list[ ItineraryTransportation ]:
   transportations: list[ ItineraryTransportation ] = []

   for saved in saved_transportations:
      main_station = fetch_main_station_coords( saved.transportation )
      transportations.append(
         ItineraryTransportation(
            name=saved.transportation,
            old_likelihood=saved.old_likelihood,
            likelihood=saved.new_likelihood,
            start_time=saved.start_time,
            end_time=saved.end_time,
            x_coord=main_station.x_coord,
            y_coord=main_station.y_coord,
            main_station=main_station.name,
            legs=[
               ItineraryTransportationLeg(
                  from_station=leg.from_station,
                  to_station=leg.to_station,
                  start_time=leg.start_time,
                  end_time=leg.end_time )
               for leg in saved.legs
            ],
            added_as_attraction=saved.added_as_attraction ) )

   return transportations
