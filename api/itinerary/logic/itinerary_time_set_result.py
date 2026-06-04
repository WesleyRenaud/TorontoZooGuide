from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryTimeSetResult:
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: tuple[ ItineraryErrorType, ... ] = ()


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
