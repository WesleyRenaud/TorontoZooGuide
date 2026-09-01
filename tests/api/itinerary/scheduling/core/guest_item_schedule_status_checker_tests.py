from __future__ import annotations

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from api.models import Animal
from api.models import Attraction
from api.models import Itinerary
from api.models import ItineraryTransportation


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

UNSCHEDULED_CAROUSEL = Attraction(
   name='Conservation Carousel',
   free_with_admission=True,
)

SCHEDULED_CAROUSEL = Attraction(
   name='Conservation Carousel',
   free_with_admission=True,
   start_time='11:00 AM',
   end_time='11:20 AM',
)

UNSCHEDULED_ZOOMOBILE = ItineraryTransportation(
   name='Zoomobile',
   added_as_attraction=True,
)

BULK_EVALUATED_ZOOMOBILE = ItineraryTransportation(
   name='Zoomobile',
   added_as_attraction=False,
   bulk_transit_evaluated=True,
)

SCHEDULED_ZOOMOBILE = ItineraryTransportation(
   name='Zoomobile',
   added_as_attraction=True,
   start_time='11:30 AM',
   end_time='12:45 PM',
)

SCHEDULED_PENGUIN = Animal(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   start_time='10:30 AM',
   end_time='10:35 AM',
)


def _itinerary(
      *,
      animals: list[ Animal ],
      attractions: list[ Attraction ] | None = None,
      transportations: list[ ItineraryTransportation ] | None = None ) -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[],
      animals=animals,
      attractions=attractions or [],
      transportations=transportations or [],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def Test_HasUnscheduledGuestItems_TestUnscheduledAnimalsAndAttractions_ExpectTrue() -> None:
   itinerary = _itinerary(
      animals=[ SCHEDULED_LION, UNSCHEDULED_CHEETAH ],
      attractions=[ UNSCHEDULED_CAROUSEL ] )

   assert GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )


def Test_HasUnscheduledGuestItems_TestUnscheduledTransportation_ExpectTrue() -> None:
   itinerary = _itinerary(
      animals=[ SCHEDULED_LION ],
      transportations=[ UNSCHEDULED_ZOOMOBILE ] )

   assert GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )


def Test_HasUnscheduledGuestItems_TestBulkEvaluatedTransit_ExpectFalse() -> None:
   itinerary = _itinerary(
      animals=[ SCHEDULED_LION ],
      transportations=[ BULK_EVALUATED_ZOOMOBILE ] )

   assert not GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )


def Test_HasUnscheduledGuestItems_TestFullyScheduledGuestItems_ExpectFalse() -> None:
   itinerary = _itinerary(
      animals=[ SCHEDULED_LION ],
      attractions=[ SCHEDULED_CAROUSEL ],
      transportations=[ SCHEDULED_ZOOMOBILE ] )

   assert not GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )


def Test_HasUnscheduledGuestItems_TestLionAndPenguinFullyScheduled_ExpectFalse() -> None:
   itinerary = _itinerary(
      animals=[
         SCHEDULED_LION,
         SCHEDULED_PENGUIN,
      ] )

   assert not GuestItemScheduleStatusChecker.has_unscheduled_guest_items( itinerary )
   assert {
      animal.species
      for animal in itinerary.animals
      if GuestItemScheduleStatusChecker.has_schedule_times(
         animal.start_time,
         animal.end_time )
   } == { 'African Lion', 'African Penguin' }
