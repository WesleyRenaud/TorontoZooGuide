from __future__ import annotations

from dataclasses import dataclass, field

from .itinerary_result_reason import ItineraryResultReason
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryTimeSetResult:
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: list[ ItineraryErrorType ] = field( default_factory=list )
   itinerary: Itinerary | None = None
   reasons: list[ ItineraryResultReason ] = field( default_factory=list )


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
