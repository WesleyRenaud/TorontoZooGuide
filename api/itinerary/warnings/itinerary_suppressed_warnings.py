from __future__ import annotations

from dataclasses import replace

from ..data_access.itinerary_status_provider import ItineraryStatusProvider
from ..results.itinerary_save_result import ItinerarySaveResult
from ..results.itinerary_time_set_result import ItineraryTimeSetResult
from ...shared.enums import ItineraryErrorType
from ...types import Connection


def append_suppressed_warning(
      suppressed_warnings: list[ ItineraryErrorType ],
      error_type: ItineraryErrorType ) -> None:
   if error_type not in suppressed_warnings:
      suppressed_warnings.append( error_type )


def record_if_error_suppressed(
      conn: Connection,
      suppressed_warnings: list[ ItineraryErrorType ],
      error_type: ItineraryErrorType ) -> bool:
   if not ItineraryStatusProvider.is_itinerary_error_suppressed( conn, error_type ):
      return False

   append_suppressed_warning( suppressed_warnings, error_type )
   return True


def with_suppressed_warnings(
      result: ItinerarySaveResult,
      suppressed_warnings: list[ ItineraryErrorType ] ) -> ItinerarySaveResult:
   if not suppressed_warnings:
      return result

   combined = [
      *dict.fromkeys( ( *result.suppressed_warnings, *suppressed_warnings ) ),
   ]

   return replace( result, suppressed_warnings=combined )


def with_time_set_suppressed_warnings(
      result: ItineraryTimeSetResult,
      suppressed_warnings: list[ ItineraryErrorType ] ) -> ItineraryTimeSetResult:
   if not suppressed_warnings:
      return result

   combined = [
      *dict.fromkeys( ( *result.suppressed_warnings, *suppressed_warnings ) ),
   ]

   return replace( result, suppressed_warnings=combined )
