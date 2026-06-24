from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CAROUSEL, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.reschedule_itinerary_item_schedules import reschedule_itinerary_items_after_fixed_time_activity_add
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def test_reschedule_after_fixed_time_activity_only_reschedules_previously_scheduled_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
   ).success

   result = reschedule_itinerary_items_after_fixed_time_activity_add(
      db.conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      saved_itinerary_before_clear=fetch_saved_itinerary( db.conn ),
   )

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   assert has_itinerary_schedule_times( lion.start_time, lion.end_time )
   assert lion.start_time != '10:00'
   assert not has_itinerary_schedule_times( penguin.start_time, penguin.end_time )


def test_bulk_schedule_schedules_unscheduled_animals_when_requested(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='09:00',
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   assert has_itinerary_schedule_times( lion.start_time, lion.end_time )
   assert has_itinerary_schedule_times( penguin.start_time, penguin.end_time )


def test_bulk_schedule_schedules_unscheduled_animals_clears_guest_scheduled_attractions_and_events(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item( 'lunch', '' ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.itinerary.events == []

   carousel = next(
      attraction for attraction in result.itinerary.attractions
      if attraction.name == CAROUSEL )

   assert not has_itinerary_schedule_times(
      carousel.start_time,
      carousel.end_time )

   lion = result.itinerary.animals[ 0 ]
   assert has_itinerary_schedule_times( lion.start_time, lion.end_time )
