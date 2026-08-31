from __future__ import annotations

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_walk_route_completion_checker import ItineraryWalkRouteCompletionChecker
from api.models import Animal


VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'

SCHEDULED_LION = Animal(
   species='African Lion',
   exhibit='Africa Savanna',
   start_time='10:00 AM',
   end_time='10:30 AM',
)

UNSCHEDULED_CHEETAH = Animal(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)


def Test_ShouldAppendReturnToEntranceLeg_TestPartialSchedule_ExpectFalse() -> None:
   partial_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[ SCHEDULED_LION, UNSCHEDULED_CHEETAH ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   assert not ItineraryWalkRouteCompletionChecker.should_append_return_to_entrance_leg(
      partial_itinerary )


def Test_ShouldAppendReturnToEntranceLeg_TestCompleteSchedule_ExpectTrue() -> None:
   complete_itinerary = ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=[ SCHEDULED_LION ],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )

   assert ItineraryWalkRouteCompletionChecker.should_append_return_to_entrance_leg(
      complete_itinerary )
