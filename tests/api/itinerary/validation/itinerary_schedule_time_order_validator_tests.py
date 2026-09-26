from __future__ import annotations

from api.itinerary.validation.itinerary_schedule_time_order_validator import ItineraryScheduleTimeOrderValidator


def Test_DepartureFollowsArrival_TestArrivalUnset_ExpectTrue() -> None:
   arrival = '10:00'
   departure = None

   follows = ItineraryScheduleTimeOrderValidator.departure_follows_arrival(
      arrival,
      departure )

   assert follows is True


def Test_DepartureFollowsArrival_TestDepartureUnset_ExpectTrue() -> None:
   arrival = None
   departure = '17:00'

   follows = ItineraryScheduleTimeOrderValidator.departure_follows_arrival(
      arrival,
      departure )

   assert follows is True


def Test_DepartureFollowsArrival_TestDepartureAfterArrival_ExpectTrue() -> None:
   arrival = '10:00'
   departure = '17:00'

   follows = ItineraryScheduleTimeOrderValidator.departure_follows_arrival(
      arrival,
      departure )

   assert follows is True


def Test_DepartureFollowsArrival_TestDepartureBeforeArrival_ExpectFalse() -> None:
   arrival = '17:00'
   departure = '10:00'

   follows = ItineraryScheduleTimeOrderValidator.departure_follows_arrival(
      arrival,
      departure )

   assert follows is False


def Test_DepartureFollowsArrival_TestSameTime_ExpectFalse() -> None:
   arrival = '10:00'
   departure = arrival

   follows = ItineraryScheduleTimeOrderValidator.departure_follows_arrival(
      arrival,
      departure )

   assert follows is False
