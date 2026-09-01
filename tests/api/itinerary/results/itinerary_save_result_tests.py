from __future__ import annotations

from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType


def Test_Success_TestSuccessStatus_ExpectTrue() -> None:
   result = ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )

   assert result.success is True


def Test_Success_TestFailureStatus_ExpectFalse() -> None:
   result = ItinerarySaveResult(
      status=ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      itinerary=Itinerary( date='2026-06-15' ),
   )

   assert result.success is False
