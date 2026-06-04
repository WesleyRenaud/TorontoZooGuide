from __future__ import annotations

from .itinerary_save_result import ItinerarySaveResult
from .itinerary_time_set_result import ItineraryTimeSetResult
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
   }

   payload[ 'itinerary_config' ] = itinerary_config_to_dict( conn )

   if extra:
      payload.update( extra )

   return payload
