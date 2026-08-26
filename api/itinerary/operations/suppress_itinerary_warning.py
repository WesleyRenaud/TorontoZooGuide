from __future__ import annotations

from dataclasses import dataclass

from ..data_access.itinerary_status_provider import ItineraryStatusProvider
from ...shared.enums import ItineraryErrorType
from ...types import Connection


@dataclass( frozen=True )
class SuppressItineraryWarningResult:
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS


def suppress_itinerary_warning(
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
