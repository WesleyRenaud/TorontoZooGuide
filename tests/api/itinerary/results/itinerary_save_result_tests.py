from __future__ import annotations

from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType


def Test_Success_TestSuccessStatus_ExpectTrue() -> None:
   date = '2026-06-15'
   result = ItinerarySaveResult( itinerary=Itinerary( date=date ) )

   success = result.success

   assert success is True


def Test_Success_TestFailureStatus_ExpectFalse() -> None:
   date = '2026-06-15'
   result = ItinerarySaveResult(
      status=ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      itinerary=Itinerary( date=date ) )

   success = result.success

   assert success is False
