from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.warnings.early_admission_warning_builder import EarlyAdmissionWarningBuilder
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.types import Types
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


EARLY_ADMISSION_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)

STANDARD_HOURS = ZooHoursRecord(
   operating_date='2026-06-15',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


@pytest.fixture
def stub_no_suppressed_status( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )


@pytest.fixture
def stub_early_admission_suppressed( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, error_type: (
         error_type == ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP ) )


def Test_ArrivalIsDuringEarlyAdmission_TestInWindow_ExpectTrue() -> None:
   arrival_time = '09:15'

   during = EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      arrival_time,
      EARLY_ADMISSION_HOURS )

   assert during is True


def Test_ArrivalIsDuringEarlyAdmission_TestAtOpen_ExpectFalse() -> None:
   arrival_time = EARLY_ADMISSION_HOURS.open_time

   during = EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      arrival_time,
      EARLY_ADMISSION_HOURS )

   assert during is False


def Test_ArrivalIsDuringEarlyAdmission_TestNoEarlyAdmission_ExpectFalse() -> None:
   arrival_time = '09:15'

   during = EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      arrival_time,
      STANDARD_HOURS )

   assert during is False


def Test_IsRequired_TestConfirming_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = '09:15'
   confirming_early_admission = True

   required = EarlyAdmissionWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=confirming_early_admission )

   assert required is False


def Test_IsRequired_TestDuringEarlyAdmission_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   arrival_time = '09:15'
   confirming_early_admission = False

   required = EarlyAdmissionWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=confirming_early_admission )

   assert required is True


def Test_IsRequired_TestSuppressed_ExpectFalseAndTracked(
      stub_early_admission_suppressed: None ) -> None:
   arrival_time = '09:15'
   confirming_early_admission = False
   suppressed_warnings: list[ ItineraryErrorType ] = []
   expected_warning = ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP

   required = EarlyAdmissionWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      arrival_time,
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=confirming_early_admission,
      suppressed_warnings=suppressed_warnings )

   assert required is False
   assert suppressed_warnings == [ expected_warning ]


def Test_ArrivalIsDuringEarlyAdmission_TestInvalidOpenTime_ExpectFalse(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   original = DateValues.time_value_in_seconds
   invalid_open_time = 'bad-open'
   arrival_time = '09:15'
   hours = ZooHoursRecord(
      operating_date='2026-06-20',
      early_admission_time='09:00',
      open_time=invalid_open_time,
      last_admission_time='18:00',
      close_time='19:00' )

   def fake_time_in_seconds( value: Types.TimeInput ) -> int | None:
      if value == invalid_open_time:
         return None
      return original( value )

   monkeypatch.setattr(
      'api.itinerary.warnings.early_admission_warning_builder.DateValues.time_value_in_seconds',
      fake_time_in_seconds )

   during = EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      arrival_time,
      hours )

   assert during is False
