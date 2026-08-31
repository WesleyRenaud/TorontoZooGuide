from __future__ import annotations

from api.itinerary.validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from api.shared.enums import ItineraryErrorType
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-15',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_ValidateForZooHours_TestBeforeOpen_ExpectOutOfBounds() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '09:00',
      ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEqualsDeparture_ExpectOrderInvalid() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '17:00',
      ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestWithinHours_ExpectSuccess() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '10:00',
      ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestNoDeparture_ExpectSuccess() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '10:00',
      ZOO_HOURS,
      departure_time=None ) == ItineraryErrorType.SUCCESS
