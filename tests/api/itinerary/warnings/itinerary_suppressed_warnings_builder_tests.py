from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.warnings.itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType


@pytest.fixture
def stub_suppressed_status_provider( monkeypatch: pytest.MonkeyPatch ) -> None:
   suppressed = { ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE }

   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, error_type: error_type in suppressed )


def Test_AppendSuppressedWarning_TestDuplicate_ExpectSingleEntry() -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   ItinerarySuppressedWarningsBuilder.append_suppressed_warning(
      suppressed_warnings,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   ItinerarySuppressedWarningsBuilder.append_suppressed_warning(
      suppressed_warnings,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

   assert suppressed_warnings == [ ItineraryErrorType.ITEM_NOT_ON_ITINERARY ]


def Test_RecordIfErrorSuppressed_TestOnlySuppressedTypes_ExpectTracked(
      stub_suppressed_status_provider: None ) -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   assert not ItinerarySuppressedWarningsBuilder.record_if_error_suppressed(
      object(),  # type: ignore[arg-type]
      suppressed_warnings,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

   assert ItinerarySuppressedWarningsBuilder.record_if_error_suppressed(
      object(),  # type: ignore[arg-type]
      suppressed_warnings,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   assert suppressed_warnings == [ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ]


def Test_WithSuppressedWarnings_TestEmpty_ExpectOriginalResult() -> None:
   result = ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )

   assert ItinerarySuppressedWarningsBuilder.with_suppressed_warnings( result, () ) is result


def Test_WithSuppressedWarnings_TestMerge_ExpectUniqueWarningTypes() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date='2026-06-15' ),
      suppressed_warnings=( ItineraryErrorType.ITEM_NOT_ON_ITINERARY, ) )

   merged = ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
      result,
      (
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ) )

   assert merged.suppressed_warnings == [
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   ]


def Test_WithTimeSetSuppressedWarnings_TestEmpty_ExpectOriginalResult() -> None:
   result = ItineraryTimeSetResult()

   assert ItinerarySuppressedWarningsBuilder.with_time_set_suppressed_warnings(
      result,
      () ) is result


def Test_WithTimeSetSuppressedWarnings_TestMerge_ExpectUniqueWarningTypes() -> None:
   result = ItineraryTimeSetResult(
      suppressed_warnings=( ItineraryErrorType.ITEM_NOT_ON_ITINERARY, ) )

   merged = ItinerarySuppressedWarningsBuilder.with_time_set_suppressed_warnings(
      result,
      (
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ) )

   assert merged.suppressed_warnings == [
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   ]
