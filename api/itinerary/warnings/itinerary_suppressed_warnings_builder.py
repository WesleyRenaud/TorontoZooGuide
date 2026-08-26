from __future__ import annotations

from dataclasses import replace

from ..data_access.itinerary_status_provider import ItineraryStatusProvider
from ..results.itinerary_save_result import ItinerarySaveResult
from ..results.itinerary_time_set_result import ItineraryTimeSetResult
from ...shared.enums import ItineraryErrorType
from ...types import Connection


class ItinerarySuppressedWarningsBuilder():
   @classmethod
   def append_suppressed_warning(
         cls,
         suppressed_warnings: list[ ItineraryErrorType ],
         error_type: ItineraryErrorType ) -> None:
      if error_type not in suppressed_warnings:
         suppressed_warnings.append( error_type )


   @classmethod
   def record_if_error_suppressed(
         cls,
         conn: Connection,
         suppressed_warnings: list[ ItineraryErrorType ],
         error_type: ItineraryErrorType ) -> bool:
      if not ItineraryStatusProvider.is_itinerary_error_suppressed( conn, error_type ):
         return False

      cls.append_suppressed_warning( suppressed_warnings, error_type )
      return True


   @classmethod
   def with_suppressed_warnings(
         cls,
         result: ItinerarySaveResult,
         suppressed_warnings: list[ ItineraryErrorType ] ) -> ItinerarySaveResult:
      if not suppressed_warnings:
         return result

      combined = [
         *dict.fromkeys( ( *result.suppressed_warnings, *suppressed_warnings ) ),
      ]

      return replace( result, suppressed_warnings=combined )


   @classmethod
   def with_time_set_suppressed_warnings(
         cls,
         result: ItineraryTimeSetResult,
         suppressed_warnings: list[ ItineraryErrorType ] ) -> ItineraryTimeSetResult:
      if not suppressed_warnings:
         return result

      combined = [
         *dict.fromkeys( ( *result.suppressed_warnings, *suppressed_warnings ) ),
      ]

      return replace( result, suppressed_warnings=combined )
