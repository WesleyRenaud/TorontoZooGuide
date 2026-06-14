from __future__ import annotations

from dataclasses import dataclass

from .itinerary_result_reason import ItineraryResultReason
from ..logic.itinerary_adjustment import ItineraryAdjustment
from ...models import Itinerary
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItinerarySaveResult:
   itinerary: Itinerary
   reasons: tuple[ ItineraryResultReason, ... ] = ()
   adjustments: tuple[ ItineraryAdjustment, ... ] = ()
   status: ItineraryErrorType = ItineraryErrorType.SUCCESS
   suppressed_warnings: tuple[ ItineraryErrorType, ... ] = ()


   @property
   def success( self ) -> bool:
      return self.status == ItineraryErrorType.SUCCESS
