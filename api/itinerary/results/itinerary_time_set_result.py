from __future__ import annotations

from dataclasses import dataclass

from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryTimeSetResult:
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: tuple[ ItineraryErrorType, ... ] = ()
   itinerary: Itinerary | None = None


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
