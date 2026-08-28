from __future__ import annotations

from ..operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from ...shared.constants import itinerary_config_to_dict
from ...types import Connection


class SuppressItineraryWarningResultResponseBuilder():
   @classmethod
   def to_dict(
         cls,
         result: SuppressItineraryWarningResult,
         *,
         conn: Connection | None = None,
   ) -> dict[ str, object ]:
      payload: dict[ str, object ] = {
         'status': result.status.value,
         'reasons': [],
         'suppressed_warnings': [],
         'itinerary_config': itinerary_config_to_dict( conn ),
      }

      return payload
