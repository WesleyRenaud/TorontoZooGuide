from __future__ import annotations

from dataclasses import dataclass, field

from ..domain.itinerary_adjustment import ItineraryAdjustment
from .itinerary_result_reason import ItineraryResultReason
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItinerarySaveResult:
   itinerary: Itinerary
   reasons: list[ ItineraryResultReason ] = field( default_factory=list )
   adjustments: list[ ItineraryAdjustment ] = field( default_factory=list )
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: list[ ItineraryErrorType ] = field( default_factory=list )


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
