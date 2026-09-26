from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.warnings.short_visit_warning_builder import ShortVisitWarningBuilder
from api.shared.calendar_dates import DateValues
from api.shared.constants import Constants
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
   arrival_time = '09:30'
   departure_time = DateValues.add_minutes_to_time(
      arrival_time,
      Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES - 1 )
   confirming_short_visit = True

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit )

   assert required is False


def Test_IsRequired_TestShortVisit_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = '09:30'
   departure_time = DateValues.add_minutes_to_time(
      arrival_time,
      Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES - 1 )
   confirming_short_visit = False

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit )

   assert required is True


def Test_IsRequired_TestLongEnoughVisit_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = '09:30'
   departure_time = DateValues.add_minutes_to_time(
      arrival_time,
      Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES )
   confirming_short_visit = False

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit )

   assert required is False


def Test_IsRequired_TestSuppressed_ExpectFalseAndTracked(
      stub_short_visit_suppressed: None ) -> None:
   arrival_time = '09:30'
   departure_time = DateValues.add_minutes_to_time(
      arrival_time,
      Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES - 1 )
   confirming_short_visit = False
   suppressed_warnings: list[ ItineraryErrorType ] = []
   expected_warning = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit,
      suppressed_warnings=suppressed_warnings )

   assert required is False
   assert suppressed_warnings == [ expected_warning ]


def Test_IsRequired_TestMissingArrival_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = None
   departure_time = '5:00 PM'
   confirming_short_visit = False

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit )

   assert required is False


def Test_IsRequired_TestMissingArrivalAndDeparture_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = None
   departure_time = None
   confirming_short_visit = False

   required = ShortVisitWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      departure_time,
      confirming_short_visit=confirming_short_visit )

   assert required is False
