from __future__ import annotations

from ..data_access.itinerary_provider import ItineraryProvider
from ..data_access.transportation_day_loop_provider import TransportationDayLoopProvider
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...request_connection import get_connection
from ...shared.calendar_dates import DateValues
from .transit_ride_endpoint import TransitRideEndpoint
from ..transportation.resolve_transportation_day_loop import fetch_transportation_day_loop
from .transportation_boarding_station_resolver import TransportationBoardingStationResolver
from .transportation_station_walk_node_resolver import TransportationStationWalkNodeResolver


class TransportationWalkNodeResolver():
   @classmethod
   def resolve(
         cls,
         transportation_name: str,
         *,
         legs: list[ ItineraryTransportationLeg ] | None = None,
         endpoint: TransitRideEndpoint = TransitRideEndpoint.ONBOARDING,
         ) -> str | None:
      station_name = cls._station_name_for_endpoint(
         transportation_name,
         legs=legs,
         endpoint=endpoint )

      if station_name is None:
         return None

      return TransportationStationWalkNodeResolver.resolve(
         transportation_name,
         station_name )


   @classmethod
   def _station_name_for_endpoint(
         cls,
         transportation_name: str,
         *,
         legs: list[ ItineraryTransportationLeg ] | None,
         endpoint: TransitRideEndpoint,
         ) -> str | None:
      if legs:
         return TransportationBoardingStationResolver.station_for_legs(
            legs,
            endpoint )

      return cls._default_boarding_station_name( transportation_name )


   @classmethod
   def _default_boarding_station_name( cls, transportation_name: str ) -> str | None:
      conn = get_connection()

      if conn is None:
         return None

      date_record = ItineraryProvider.fetch_itinerary_date_record( conn )

      if date_record is not None:
         visit_date = DateValues.parse_date_value( date_record.itinerary_date )

         if visit_date is not None:
            day_loop = fetch_transportation_day_loop(
               conn,
               transportation=transportation_name,
               target_date=visit_date )

            if day_loop is not None and day_loop.legs:
               return day_loop.legs[ 0 ].from_station

      return TransportationDayLoopProvider.fetch_main_transportation_station(
         conn,
         transportation_name )
