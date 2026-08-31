from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.warnings.short_visit_warning_builder import ShortVisitWarningBuilder
from api.shared.enums import ItineraryErrorType


@pytest.fixture
def stub_no_suppressed_status( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )


@pytest.fixture
def stub_short_visit_suppressed( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, error_type: (
         error_type == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ) )


def Test_IsRequired_TestConfirming_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   assert not ShortVisitWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:30',
      '10:00',
      confirming_short_visit=True )


def Test_IsRequired_TestShortVisit_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   assert ShortVisitWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:30',
      '10:00',
      confirming_short_visit=False )


def Test_IsRequired_TestLongEnoughVisit_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   assert not ShortVisitWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:30',
      '17:00',
      confirming_short_visit=False )


def Test_IsRequired_TestSuppressed_ExpectFalseAndTracked(
      stub_short_visit_suppressed: None ) -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   assert not ShortVisitWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:30',
      '10:00',
      confirming_short_visit=False,
      suppressed_warnings=suppressed_warnings )
   assert suppressed_warnings == [
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   ]
