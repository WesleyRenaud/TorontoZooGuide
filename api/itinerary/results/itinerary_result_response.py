from __future__ import annotations

from .itinerary_save_result import ItinerarySaveResult
from .itinerary_time_set_result import ItineraryTimeSetResult
from ..logic.suppress_itinerary_warning import SuppressItineraryWarningResult
from ...shared.constants import itinerary_config_to_dict
from ...types import Connection


def itinerary_result_to_dict(
      result: ItinerarySaveResult,
      *,
      conn: Connection | None = None,
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

   if include_config:
      payload[ 'itinerary_config' ] = itinerary_config_to_dict( conn )

   if extra:
      payload.update( extra )

   return payload


def itinerary_time_set_result_to_dict(
      result: ItineraryTimeSetResult,
      *,
      conn: Connection | None = None,
      extra: dict[ str, object ] | None = None,
) -> dict[ str, object ]:
   payload: dict[ str, object ] = {
      'status': result.status.value,
      'reasons': [],
      'suppressed_warnings': [
         warning.value for warning in result.suppressed_warnings
      ],
   }

   payload[ 'itinerary_config' ] = itinerary_config_to_dict( conn )

   if result.itinerary is not None:
      payload[ 'itinerary' ] = result.itinerary.to_dict()

   if extra:
      payload.update( extra )

   return payload


def suppress_itinerary_warning_result_to_dict(
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
