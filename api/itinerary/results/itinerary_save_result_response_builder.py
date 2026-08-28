from __future__ import annotations

from .itinerary_path_builder import ItineraryPathBuilder
from .itinerary_save_result import ItinerarySaveResult
from ...shared.itinerary_config_builder import ItineraryConfigBuilder
from ...types import Types


class ItinerarySaveResultResponseBuilder():
   @classmethod
   def to_dict(
         cls,
         result: ItinerarySaveResult,
         *,
         conn: Types.Connection | None = None,
         include_itinerary: bool = True,
         include_config: bool = False,
         extra: dict[ str, object ] | None = None,
   ) -> dict[ str, object ]:
      payload: dict[ str, object ] = {
         'status': result.status.value,
         'reasons': [
            reason.to_dict() for reason in result.reasons
         ],
         'adjustments': [
            adjustment.to_dict() for adjustment in result.adjustments
         ],
         'suppressed_warnings': [
            warning.value for warning in result.suppressed_warnings
         ],
      }

      if include_itinerary:
         payload[ 'itinerary' ] = result.itinerary.to_dict()
         payload[ 'itinerary_path' ] = ItineraryPathBuilder.build( conn )

      if include_config:
         payload[ 'itinerary_config' ] = ItineraryConfigBuilder.to_dict( conn )

      if extra:
         payload.update( extra )

      return payload
