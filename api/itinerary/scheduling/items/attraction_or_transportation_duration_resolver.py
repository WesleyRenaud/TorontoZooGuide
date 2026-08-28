from __future__ import annotations

from ...data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider
from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...transportation.transportation_default_duration_resolver import TransportationDefaultDurationResolver
from ....types import Types


class AttractionOrTransportationDurationResolver():
   @classmethod
   def default_seconds(
         cls,
         conn: Types.Connection,
         attraction_name: str ) -> int | None:
      if AttractionAlsoTransportationProvider.attraction_is_also_transportation( conn, attraction_name ):
         return TransportationDefaultDurationResolver.resolve(
            conn,
            attraction_name )

      return ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds( conn, attraction_name )
