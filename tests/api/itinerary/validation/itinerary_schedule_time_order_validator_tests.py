from __future__ import annotations

from api.itinerary.validation.itinerary_schedule_time_order_validator import ItineraryScheduleTimeOrderValidator


def Test_DepartureFollowsArrival_TestOtherTimeUnset_ExpectTrue() -> None:
   assert ItineraryScheduleTimeOrderValidator.departure_follows_arrival( '10:00', None )
   assert ItineraryScheduleTimeOrderValidator.departure_follows_arrival( None, '17:00' )


def Test_DepartureFollowsArrival_TestDepartureAfterArrival_ExpectTrue() -> None:
   assert ItineraryScheduleTimeOrderValidator.departure_follows_arrival( '10:00', '17:00' )


def Test_DepartureFollowsArrival_TestDepartureNotAfterArrival_ExpectFalse() -> None:
   assert not ItineraryScheduleTimeOrderValidator.departure_follows_arrival( '17:00', '10:00' )
   assert not ItineraryScheduleTimeOrderValidator.departure_follows_arrival( '10:00', '10:00' )
