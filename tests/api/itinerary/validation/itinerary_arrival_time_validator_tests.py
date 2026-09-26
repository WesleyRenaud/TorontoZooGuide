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
   zoo_hours = EARLY_ADMISSION_ZOO_HOURS

   earliest = ItineraryArrivalTimeValidator.earliest_arrival_time( zoo_hours )

   assert earliest == zoo_hours.early_admission_time


def Test_EarliestArrivalTime_TestStandardHours_ExpectOpenTime() -> None:
   zoo_hours = ZOO_HOURS

   earliest = ItineraryArrivalTimeValidator.earliest_arrival_time( zoo_hours )

   assert earliest == zoo_hours.open_time


def Test_EarliestAllowedArrivalMinutes_TestFixedZooStartTimes_ExpectEarliestStart() -> None:
   zoo_hours = ZOO_HOURS
   fixed_start = '09:00 AM'

   earliest_minutes = ItineraryArrivalTimeValidator.earliest_allowed_arrival_minutes(
      zoo_hours,
      [ fixed_start ] )

   assert earliest_minutes == DateValues.time_value_in_minutes( fixed_start )


def Test_EarliestAllowedArrivalMinutes_TestInvalidFixedStart_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoo_hours = ZOO_HOURS
   invalid_start_time = 'not-a-time'
   original_time_value_in_minutes = DateValues.time_value_in_minutes

   def time_value_in_minutes( value: str ) -> int | None:
      if value == invalid_start_time:
         return None

      return original_time_value_in_minutes( value )

   monkeypatch.setattr(
      'api.itinerary.validation.itinerary_arrival_time_validator.DateValues.time_value_in_minutes',
      time_value_in_minutes )

   earliest_minutes = ItineraryArrivalTimeValidator.earliest_allowed_arrival_minutes(
      zoo_hours,
      [ invalid_start_time ] )

   assert earliest_minutes == original_time_value_in_minutes( zoo_hours.open_time )


def Test_ValidateForZooHours_TestBeforeOpen_ExpectOutOfBounds() -> None:
   minutes_before_open = DateValues.time_value_in_minutes( '00:30' )
   arrival_time = DateValues.schedule_time_key_from_minutes(
      DateValues.time_value_in_minutes( ZOO_HOURS.open_time ) - minutes_before_open )
   departure_time = '17:00'

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEqualsDeparture_ExpectOrderInvalid() -> None:
   departure_time = '17:00'
   arrival_time = departure_time

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestWithinHours_ExpectSuccess() -> None:
   arrival_time = '10:00'
   departure_time = '17:00'

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestNoDeparture_ExpectSuccess() -> None:
   arrival_time = '10:00'
   departure_time = None

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestAfterLastAdmission_ExpectOutOfBounds() -> None:
   minutes_after_last_admission = DateValues.time_value_in_minutes( '00:15' )
   arrival_time = DateValues.add_minutes_to_time(
      ZOO_HOURS.last_admission_time,
      minutes_after_last_admission )
   departure_time = ZOO_HOURS.close_time

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEarlyAdmissionArrival_ExpectSuccess() -> None:
   arrival_time = EARLY_ADMISSION_ZOO_HOURS.early_admission_time
   departure_time = '17:00'

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      EARLY_ADMISSION_ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestBeforeEarlyAdmission_ExpectOutOfBounds() -> None:
   minutes_before_early_admission = DateValues.time_value_in_minutes( '00:15' )
   arrival_time = DateValues.schedule_time_key_from_minutes(
      DateValues.time_value_in_minutes( EARLY_ADMISSION_ZOO_HOURS.early_admission_time )
      - minutes_before_early_admission )
   departure_time = '17:00'

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      EARLY_ADMISSION_ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestArrivalAfterDeparture_ExpectOrderInvalid() -> None:
   departure_time = '17:00'
   minutes_after_departure = DateValues.time_value_in_minutes( '00:15' )
   arrival_time = DateValues.add_minutes_to_time(
      departure_time,
      minutes_after_departure )

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestBeforeOpenWithoutFixedStart_ExpectOutOfBounds() -> None:
   arrival_time = '08:45'
   departure_time = '17:00'

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestFixedZooStartBeforeOpen_ExpectSuccess() -> None:
   arrival_time = '08:45'
   departure_time = '17:00'
   fixed_zoo_start_times = ( arrival_time, )

   error_type = ItineraryArrivalTimeValidator.validate_for_zoo_hours(
      arrival_time,
      ZOO_HOURS,
      departure_time=departure_time,
      fixed_zoo_start_times=fixed_zoo_start_times )

   assert error_type == ItineraryErrorType.SUCCESS
