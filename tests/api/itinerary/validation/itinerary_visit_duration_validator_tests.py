from __future__ import annotations

from api.itinerary.validation.itinerary_visit_duration_validator import ItineraryVisitDurationValidator
from api.shared.calendar_dates import DateValues
from api.shared.constants import Constants


def Test_IsShorterThanMinimum_TestBelowMinimum_ExpectTrue() -> None:
   arrival = '09:30'
   departure_minutes = (
      DateValues.time_value_in_minutes( arrival )
      + Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES
      - 1 )
   departure = DateValues.schedule_time_key_from_minutes( departure_minutes )

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is True


def Test_IsShorterThanMinimum_TestAboveMinimum_ExpectFalse() -> None:
   arrival = '09:30'
   departure_minutes = (
      DateValues.time_value_in_minutes( arrival )
      + Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES
      + DateValues.time_value_in_minutes( '00:30' ) )
   departure = DateValues.schedule_time_key_from_minutes( departure_minutes )

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestExactMinimum_ExpectNotShorter() -> None:
   arrival = '09:30'
   departure_minutes = (
      DateValues.time_value_in_minutes( arrival )
      + Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES )
   departure = DateValues.schedule_time_key_from_minutes( departure_minutes )

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestLateAfternoonHalfHour_ExpectTrue() -> None:
   arrival = '16:30'
   departure = '17:00'

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is True


def Test_IsShorterThanMinimum_TestLateAfternoonFortyFiveMinutes_ExpectTrue() -> None:
   arrival = '17:15'
   departure = '18:00'

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is True


def Test_IsShorterThanMinimum_TestMorningTwoHours_ExpectFalse() -> None:
   arrival = '09:30'
   departure = '11:30'

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestLateAfternoonOneHour_ExpectTrue() -> None:
   arrival = '17:00'
   departure = '18:00'

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is True


def Test_IsShorterThanMinimum_TestBothTimesMissing_ExpectFalse() -> None:
   arrival = None
   departure = None

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestArrivalMissing_ExpectFalse() -> None:
   arrival = None
   departure = '17:00'

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestDepartureMissing_ExpectFalse() -> None:
   arrival = '09:30'
   departure = None

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False


def Test_IsShorterThanMinimum_TestBlankTimes_ExpectFalse() -> None:
   arrival = ''
   departure = ''

   shorter = ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )

   assert shorter is False
