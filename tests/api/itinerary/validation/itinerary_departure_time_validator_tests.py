from __future__ import annotations

from api.itinerary.validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
from api.shared.enums import ItineraryErrorType
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-15',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)

EARLY_ADMISSION_ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_ValidateForZooHours_TestBeforeOpen_ExpectOutOfBounds() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:00',
      ZOO_HOURS,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEqualsArrival_ExpectOrderInvalid() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:30',
      ZOO_HOURS,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestWithinHours_ExpectSuccess() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '18:00',
      ZOO_HOURS,
      arrival_time='09:30' ) == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestNoArrival_ExpectSuccess() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '18:00',
      ZOO_HOURS,
      arrival_time=None ) == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestEarlyAdmissionWindow_ExpectSuccess() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:08',
      EARLY_ADMISSION_ZOO_HOURS,
      arrival_time='09:00' ) == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestBeforeEarlyAdmission_ExpectOutOfBounds() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '08:59',
      EARLY_ADMISSION_ZOO_HOURS,
      arrival_time='09:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestAfterClose_ExpectOutOfBounds() -> None:
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '19:15',
      ZOO_HOURS,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
