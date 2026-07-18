from __future__ import annotations

from dataclasses import dataclass, field

from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryTimeSetResult:
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: list[ ItineraryErrorType ] = field( default_factory=list )
   itinerary: Itinerary | None = None


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
