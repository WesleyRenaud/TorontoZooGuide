from __future__ import annotations

from datetime import date

from ..data_access.fetch_main_transportation_station import fetch_main_station_coords
from ...itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation import ItineraryTransportation
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...request_connection import get_connection
from ..transportation.route_duration_minutes import transportation_route_duration_minutes


def build_itinerary_transportations(
      saved_transportations: list[ ItineraryTransportationRecord ],
      *,
      target_date: date,
) -> list[ ItineraryTransportation ]:
   transportations: list[ ItineraryTransportation ] = []
   conn = get_connection()

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
            added_as_attraction=saved.added_as_attraction,
            route_duration_minutes=transportation_route_duration_minutes(
               conn,
               transportation=saved.transportation,
               target_date=target_date,
            ),
         ),
      )

   return transportations
