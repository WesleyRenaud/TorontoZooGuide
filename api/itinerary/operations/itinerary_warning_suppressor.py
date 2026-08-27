from __future__ import annotations

from ..data_access.itinerary_status_provider import ItineraryStatusProvider
from ...shared.enums import ItineraryErrorType
from .suppress_itinerary_warning_result import SuppressItineraryWarningResult
from ...types import Connection


class ItineraryWarningSuppressor():
   @classmethod
   def suppress(
         cls,
         conn: Connection,
         warning_type: str ) -> SuppressItineraryWarningResult:
      if not warning_type:
         return SuppressItineraryWarningResult(
            status=ItineraryErrorType.SAVE_FAILED )

      try:
         error_type = ItineraryErrorType( warning_type )
      except ValueError:
         return SuppressItineraryWarningResult(
            status=ItineraryErrorType.SAVE_FAILED )

      if not ItineraryStatusProvider.is_itinerary_status_suppressable( conn, error_type ):
         return SuppressItineraryWarningResult(
            status=ItineraryErrorType.SAVE_FAILED )

      ItineraryStatusProvider.suppress_itinerary_status( conn, error_type )

      return SuppressItineraryWarningResult()
