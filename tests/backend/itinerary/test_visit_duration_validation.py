from api.itinerary.validation.itinerary_visit_duration_validation_builder import ItineraryVisitDurationValidationBuilder


def test_itinerary_visit_is_shorter_than_minimum() -> None:
   assert ItineraryVisitDurationValidationBuilder.is_shorter_than_minimum( '09:30', '11:00' )
   assert not ItineraryVisitDurationValidationBuilder.is_shorter_than_minimum( '09:30', '11:30' )
