from __future__ import annotations

from api.itinerary.validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
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

JUNE_22_ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-22',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='17:00',
   close_time='18:00',
)


def Test_ValidateForZooHours_TestBeforeOpen_ExpectOutOfBounds() -> None:
   minutes_before_open = DateValues.time_value_in_minutes( '00:30' )
   departure_time = DateValues.schedule_time_key_from_minutes(
      DateValues.time_value_in_minutes( ZOO_HOURS.open_time ) - minutes_before_open )
   arrival_time = ZOO_HOURS.open_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestEqualsArrival_ExpectOrderInvalid() -> None:
   arrival_time = ZOO_HOURS.open_time
   departure_time = arrival_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.TIME_ORDER_INVALID


def Test_ValidateForZooHours_TestWithinHours_ExpectSuccess() -> None:
   departure_time = ZOO_HOURS.last_admission_time
   arrival_time = ZOO_HOURS.open_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestNoArrival_ExpectSuccess() -> None:
   departure_time = ZOO_HOURS.last_admission_time
   arrival_time = None

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestEarlyAdmissionWindow_ExpectSuccess() -> None:
   minutes_after_early_admission = DateValues.time_value_in_minutes( '00:08' )
   departure_time = DateValues.add_minutes_to_time(
      EARLY_ADMISSION_ZOO_HOURS.early_admission_time,
      minutes_after_early_admission )
   arrival_time = EARLY_ADMISSION_ZOO_HOURS.early_admission_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      EARLY_ADMISSION_ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.SUCCESS


def Test_ValidateForZooHours_TestBeforeEarlyAdmission_ExpectOutOfBounds() -> None:
   minutes_before_early_admission = DateValues.time_value_in_minutes( '00:01' )
   departure_time = DateValues.schedule_time_key_from_minutes(
      DateValues.time_value_in_minutes( EARLY_ADMISSION_ZOO_HOURS.early_admission_time )
      - minutes_before_early_admission )
   arrival_time = EARLY_ADMISSION_ZOO_HOURS.early_admission_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      EARLY_ADMISSION_ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestAfterClose_ExpectOutOfBounds() -> None:
   minutes_after_close = DateValues.time_value_in_minutes( '00:15' )
   departure_time = DateValues.add_minutes_to_time(
      ZOO_HOURS.close_time,
      minutes_after_close )
   arrival_time = ZOO_HOURS.open_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def Test_ValidateForZooHours_TestAfterShorterDayClose_ExpectOutOfBounds() -> None:
   departure_time = ZOO_HOURS.close_time
   arrival_time = JUNE_22_ZOO_HOURS.open_time

   error_type = ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      departure_time,
      JUNE_22_ZOO_HOURS,
      arrival_time=arrival_time )

   assert error_type == ItineraryErrorType.TIME_OUT_OF_BOUNDS
