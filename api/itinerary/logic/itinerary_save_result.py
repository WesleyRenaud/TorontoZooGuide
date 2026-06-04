from __future__ import annotations

from dataclasses import dataclass

from .itinerary_result_reason import ItineraryResultReason
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItinerarySaveResult:
   itinerary: Itinerary
   reasons: tuple[ ItineraryResultReason, ... ] = ()
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
