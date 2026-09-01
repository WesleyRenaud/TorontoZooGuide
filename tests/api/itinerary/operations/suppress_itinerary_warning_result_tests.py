from __future__ import annotations

from api.itinerary.operations.suppress_itinerary_warning_result import SuppressItineraryWarningResult
from api.shared.enums import ItineraryErrorType


def Test_Success_TestSuccessStatus_ExpectTrue() -> None:
   assert SuppressItineraryWarningResult().success is True


def Test_Success_TestFailureStatus_ExpectFalse() -> None:
   result = SuppressItineraryWarningResult(
      status=ItineraryErrorType.SAVE_FAILED,
   )

   assert result.success is False
