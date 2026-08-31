from __future__ import annotations

from api.itinerary.validation.itinerary_visit_duration_validator import ItineraryVisitDurationValidator


def Test_IsShorterThanMinimum_TestVisitWindows_ExpectMinimumThreshold() -> None:
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:00' )
   assert not ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:30' )
