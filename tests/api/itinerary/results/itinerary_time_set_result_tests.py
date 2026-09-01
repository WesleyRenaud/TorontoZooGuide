from __future__ import annotations

from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType


def Test_Success_TestSuccessStatus_ExpectTrue() -> None:
   result = ItineraryTimeSetResult(
      itinerary=Itinerary( date='2026-06-15', arrival_time='9:45 AM' ),
   )

   assert result.success is True


def Test_Success_TestFailureStatus_ExpectFalse() -> None:
   result = ItineraryTimeSetResult(
      status=ItineraryErrorType.TIME_OUT_OF_BOUNDS,
   )

   assert result.success is False
