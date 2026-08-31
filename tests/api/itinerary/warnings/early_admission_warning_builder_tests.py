from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.warnings.early_admission_warning_builder import EarlyAdmissionWarningBuilder
from api.shared.enums import ItineraryErrorType
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
   assert EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      '09:15',
      EARLY_ADMISSION_HOURS )


def Test_ArrivalIsDuringEarlyAdmission_TestAtOpen_ExpectFalse() -> None:
   assert not EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      '09:30',
      EARLY_ADMISSION_HOURS )


def Test_ArrivalIsDuringEarlyAdmission_TestNoEarlyAdmission_ExpectFalse() -> None:
   assert not EarlyAdmissionWarningBuilder.arrival_is_during_early_admission(
      '09:15',
      STANDARD_HOURS )


def Test_IsRequired_TestConfirming_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   assert not EarlyAdmissionWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:15',
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=True )


def Test_IsRequired_TestDuringEarlyAdmission_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   assert EarlyAdmissionWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:15',
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=False )


def Test_IsRequired_TestSuppressed_ExpectFalseAndTracked(
      stub_early_admission_suppressed: None ) -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   assert not EarlyAdmissionWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      '09:15',
      EARLY_ADMISSION_HOURS,
      confirming_early_admission=False,
      suppressed_warnings=suppressed_warnings )
   assert suppressed_warnings == [
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP,
   ]
