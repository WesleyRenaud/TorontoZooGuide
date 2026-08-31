from __future__ import annotations

from api.itinerary.validation.itinerary_visit_duration_validator import ItineraryVisitDurationValidator
from api.shared.calendar_dates import DateValues
from api.shared.constants import Constants


def Test_IsShorterThanMinimum_TestVisitWindows_ExpectMinimumThreshold() -> None:
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:00' )
   assert not ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:30' )


def Test_IsShorterThanMinimum_TestExactMinimum_ExpectNotShorter() -> None:
   arrival = '09:30'
   departure_minutes = (
      DateValues.time_value_in_minutes( arrival )
      + Constants.MIN_ITINERARY_VISIT_DURATION_MINUTES )
   departure = DateValues.schedule_time_key_from_minutes( departure_minutes )

   assert not ItineraryVisitDurationValidator.is_shorter_than_minimum(
      arrival,
      departure )


def Test_IsShorterThanMinimum_TestCoordinatorShortVisitExamples_ExpectThreshold() -> None:
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '16:30', '17:00' )
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '17:15', '18:00' )
   assert not ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:30' )
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '17:00', '18:00' )
