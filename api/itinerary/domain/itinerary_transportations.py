from __future__ import annotations

from datetime import date

from ...itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation import ItineraryTransportation
from ...request_connection import get_connection
from ...transportation.data_access.transportation_station import fetch_main_transportation_station_record
from ..transportation.route_duration_minutes import transportation_route_duration_minutes


def build_itinerary_transportations(
      saved_transportations: list[ ItineraryTransportationRecord ],
      *,
      target_date: date,
) -> list[ ItineraryTransportation ]:
   transportations: list[ ItineraryTransportation ] = []
   conn = get_connection()

   for saved in saved_transportations:
      main_station_record = fetch_main_transportation_station_record(
         conn,
         saved.transportation )
      transportations.append(
         ItineraryTransportation(
            name=saved.transportation,
            old_likelihood=saved.old_likelihood,
            likelihood=saved.new_likelihood,
            start_time=saved.start_time,
            end_time=saved.end_time,
            x_coord=main_station_record.x_coord,
            y_coord=main_station_record.y_coord,
            main_station=main_station_record.name,
            legs=saved.legs,
            added_as_attraction=saved.added_as_attraction,
            route_duration_minutes=transportation_route_duration_minutes(
               conn,
               transportation=saved.transportation,
               target_date=target_date,
            ),
         ),
      )

   return transportations
