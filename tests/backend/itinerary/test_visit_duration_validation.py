from api.itinerary.validation.itinerary_visit_duration_validator import ItineraryVisitDurationValidator


def test_itinerary_visit_is_shorter_than_minimum() -> None:
   assert ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:00' )
   assert not ItineraryVisitDurationValidator.is_shorter_than_minimum( '09:30', '11:30' )
