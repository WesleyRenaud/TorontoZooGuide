from __future__ import annotations

from datetime import date

from ...itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_transportation_marker_coords_builder import ItineraryTransportationMarkerCoordsBuilder
from ...models.itinerary_transportation import ItineraryTransportation
from ...request_connection import get_connection
from ...transportation.data_access.transportation_provider import TransportationProvider
from ...transportation.data_access.transportation_station_provider import TransportationStationProvider
from ..transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver


class ItineraryTransportationsBuilder():
   @classmethod
   def build(
         cls,
         saved_transportations: list[ ItineraryTransportationRecord ],
         target_date: date,
   ) -> list[ ItineraryTransportation ]:
      transportations: list[ ItineraryTransportation ] = []
      conn = get_connection()
      attraction_coords_by_name = {
         record.name: ( record.x_coord, record.y_coord )
         for record in TransportationProvider.fetch_transportation_records(
            conn,
            target_date )
      }

      for saved in saved_transportations:
         main_station_record = TransportationStationProvider.fetch_main_transportation_station_record(
            conn,
            saved.transportation )
         x_coord, y_coord = ItineraryTransportationMarkerCoordsBuilder.build(
            legs=saved.legs,
            attraction_coords=attraction_coords_by_name.get( saved.transportation ),
            main_station=main_station_record )

         transportations.append(
            ItineraryTransportation(
               name=saved.transportation,
               old_likelihood=saved.old_likelihood,
               likelihood=saved.new_likelihood,
               start_time=saved.start_time,
               end_time=saved.end_time,
               x_coord=x_coord,
               y_coord=y_coord,
               main_station=main_station_record.name,
               legs=saved.legs,
               route=saved.route,
               route_marker_sequences=saved.route_marker_sequences,
               added_as_attraction=saved.added_as_attraction,
               route_duration_minutes=TransportationRouteDurationResolver.minutes(
                  conn,
                  transportation=saved.transportation,
                  target_date=target_date,
               ),
               bulk_transit_evaluated=saved.bulk_transit_evaluated,
            ),
         )

      return transportations
