from __future__ import annotations

import pytest

from api.itinerary.validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from api.shared.calendar_dates import DateValues
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


def Test_EarliestArrivalTime_TestEarlyAdmissionOffered_ExpectEarlyAdmission() -> None:
   assert ItineraryArrivalTimeValidator.earliest_arrival_time(
      EARLY_ADMISSION_ZOO_HOURS ) == '09:00'
   assert ItineraryArrivalTimeValidator.earliest_arrival_time(
      ZOO_HOURS ) == '09:30'


def Test_EarliestAllowedArrivalMinutes_TestFixedZooStartTimes_ExpectEarliestStart() -> None:
   assert ItineraryArrivalTimeValidator.earliest_allowed_arrival_minutes(
      ZOO_HOURS,
      [ '09:00 AM' ] ) == DateValues.time_value_in_minutes( '09:00 AM' )


def Test_EarliestAllowedArrivalMinutes_TestInvalidFixedStart_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   original_time_value_in_minutes = DateValues.time_value_in_minutes

   def time_value_in_minutes( value: str ) -> int | None:
      if value == 'not-a-time':
         return None

      return original_time_value_in_minutes( value )

   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_arrival_time_validator.DateValues.time_value_in_minutes',
      time_value_in_minutes )

   assert ItineraryArrivalTimeValidator.earliest_allowed_arrival_minutes(
      ZOO_HOURS,
      [ 'not-a-time' ] ) == DateValues.time_value_in_minutes( '09:30' )


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


def Test_ValidateForZooHours_TestAfterLastAdmission_ExpectOutOfBounds() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '18:15',
      ZOO_HOURS,
      departure_time='19:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEarlyAdmissionArrival_ExpectSuccess() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '09:00',
      EARLY_ADMISSION_ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestBeforeEarlyAdmission_ExpectOutOfBounds() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '08:45',
      EARLY_ADMISSION_ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestArrivalAfterDeparture_ExpectOrderInvalid() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '17:15',
      ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestFixedZooStartBeforeOpen_ExpectSuccess() -> None:
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '08:45',
      ZOO_HOURS,
      departure_time='17:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      '08:45',
      ZOO_HOURS,
      departure_time='17:00',
      fixed_zoo_start_times=( '08:45', ) ) == ItineraryErrorType.SUCCESS
