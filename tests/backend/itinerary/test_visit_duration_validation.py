from api.itinerary.validation.itinerary_visit_duration_validation import itinerary_visit_is_shorter_than_minimum


def test_itinerary_visit_is_shorter_than_minimum() -> None:
   assert itinerary_visit_is_shorter_than_minimum( '09:30', '11:00' )
   assert not itinerary_visit_is_shorter_than_minimum( '09:30', '11:30' )
