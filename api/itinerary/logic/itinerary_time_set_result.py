from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryTimeSetResult:
   error_type: ItineraryErrorType = ItineraryErrorType.SUCCESS


   @property
   def success( self ) -> bool:
      return self.error_type == ItineraryErrorType.SUCCESS
