from __future__ import annotations

from itinerary.support import CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, LION_ITINERARY_ENTRY, LION_KEY, schedule_itinerary_item, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from api.shared.calendar_dates import DateValues
from conftest import DbControllers

CAROUSEL = 'Conservation Carousel'


def test_set_arrival_time_unschedules_items_before_arrival(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='11:00',
   ).success

   set_wild_encounter_schedule( encounter_time='09:45' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER, start_time='09:45' ) ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryCoordinator.set_arrival_time(
      '10:15',
      confirming_short_visit=True )
   itinerary = ItineraryCoordinator.get_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '10:45 AM', '10:53 AM' ),
      ( 'Cheetah', '10:38 AM', '10:43 AM' ),
   ]
   carousel = next(
      attraction
      for attraction in itinerary.attractions
      if attraction.name == CAROUSEL )
   assert GuestItemScheduleStatusChecker.has_schedule_times(
      carousel.start_time,
      carousel.end_time )
   assert not DateValues.time_value_is_before(
      carousel.start_time,
      '10:15 AM' )
   assert [
      ( encounter.name, encounter.start_time, encounter.end_time )
      for encounter in itinerary.wild_encounters
   ] == [
      ( WILD_ENCOUNTER, '9:45 AM', '10:30 AM' ),
   ]
