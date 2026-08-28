from __future__ import annotations

from .itinerary_path_builder import ItineraryPathBuilder
from .itinerary_time_set_result import ItineraryTimeSetResult
from ...shared.itinerary_config_builder import ItineraryConfigBuilder
from ...types import Types


class ItineraryTimeSetResultResponseBuilder():
   @classmethod
   def to_dict(
         cls,
         result: ItineraryTimeSetResult,
         *,
         conn: Types.Connection | None = None,
         extra: dict[ str, object ] | None = None,
   ) -> dict[ str, object ]:
      payload: dict[ str, object ] = {
         'status': result.status.value,
         'reasons': [],
         'suppressed_warnings': [
            warning.value for warning in result.suppressed_warnings
         ],
      }

      payload[ 'itinerary_config' ] = ItineraryConfigBuilder.to_dict( conn )
      payload[ 'itinerary_path' ] = ItineraryPathBuilder.build( conn )

      if result.itinerary is not None:
         payload[ 'itinerary' ] = result.itinerary.to_dict()

      if extra:
         payload.update( extra )

      return payload
