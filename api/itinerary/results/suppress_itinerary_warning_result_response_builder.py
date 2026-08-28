from __future__ import annotations

from ..operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from ...shared.itinerary_config_builder import ItineraryConfigBuilder
from ...types import Types


class SuppressItineraryWarningResultResponseBuilder():
   @classmethod
   def to_dict(
         cls,
         result: SuppressItineraryWarningResult,
         *,
         conn: Types.Connection | None = None,
   ) -> dict[ str, object ]:
      payload: dict[ str, object ] = {
         'status': result.status.value,
         'reasons': [],
         'suppressed_warnings': [],
         'itinerary_config': ItineraryConfigBuilder.to_dict( conn ),
      }

      return payload
