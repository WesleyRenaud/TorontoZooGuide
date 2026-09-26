from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
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
   error_type = ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   suppressed_warnings: list[ ItineraryErrorType ] = [ error_type ]

   ItinerarySuppressedWarningsBuilder.append_suppressed_warning(
      suppressed_warnings,
      error_type )

   assert suppressed_warnings == [ error_type ]


def Test_RecordIfErrorSuppressed_TestNotSuppressedType_ExpectFalse(
      stub_suppressed_status_provider: None ) -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []
   error_type = ItineraryErrorType.ITEM_NOT_ON_ITINERARY

   recorded = ItinerarySuppressedWarningsBuilder.record_if_error_suppressed(
      STUB_REQUEST_CONNECTION,
      suppressed_warnings,
      error_type )

   assert recorded is False
   assert suppressed_warnings == []


def Test_RecordIfErrorSuppressed_TestSuppressedType_ExpectTracked(
      stub_suppressed_status_provider: None ) -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []
   error_type = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   recorded = ItinerarySuppressedWarningsBuilder.record_if_error_suppressed(
      STUB_REQUEST_CONNECTION,
      suppressed_warnings,
      error_type )

   assert recorded is True
   assert suppressed_warnings == [ error_type ]


def Test_WithSuppressedWarnings_TestEmpty_ExpectOriginalResult() -> None:
   date = '2026-06-15'
   result = ItinerarySaveResult( itinerary=Itinerary( date=date ) )
   empty_warnings: list[ ItineraryErrorType ] = []

   merged = ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
      result,
      empty_warnings )

   assert merged is result


def Test_WithSuppressedWarnings_TestMerge_ExpectUniqueWarningTypes() -> None:
   date = '2026-06-15'
   existing = ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   added = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   result = ItinerarySaveResult(
      itinerary=Itinerary( date=date ),
      suppressed_warnings=( existing, ) )
   additional = [ added, existing ]

   merged = ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
      result,
      additional )

   assert merged.suppressed_warnings == [ existing, added ]


def Test_WithTimeSetSuppressedWarnings_TestEmpty_ExpectOriginalResult() -> None:
   result = ItineraryTimeSetResult()
   empty_warnings: list[ ItineraryErrorType ] = []

   merged = ItinerarySuppressedWarningsBuilder.with_time_set_suppressed_warnings(
      result,
      empty_warnings )

   assert merged is result


def Test_WithTimeSetSuppressedWarnings_TestMerge_ExpectUniqueWarningTypes() -> None:
   existing = ItineraryErrorType.ITEM_NOT_ON_ITINERARY
   added = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE
   result = ItineraryTimeSetResult(
      suppressed_warnings=( existing, ) )
   additional = [ added, existing ]

   merged = ItinerarySuppressedWarningsBuilder.with_time_set_suppressed_warnings(
      result,
      additional )

   assert merged.suppressed_warnings == [ existing, added ]
