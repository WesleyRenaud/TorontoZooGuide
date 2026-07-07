from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_bulk_schedule_animals_schedules_in_master_route_order(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()
   assert result.itinerary.arrival_time == '9:30 AM'

   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah' )
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )

   assert lion.start_time == '9:30 AM'
   assert lion.end_time == '9:38 AM'
   assert cheetah.start_time == '9:38 AM'
   assert cheetah.end_time == '9:43 AM'


def test_bulk_schedule_animals_sets_arrival_time_to_zoo_open_when_unset(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   itinerary_before = ItineraryCoordinator.get_itinerary()
   assert itinerary_before.arrival_time is None

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'


def test_bulk_schedule_animals_rebuild_reschedules_already_scheduled_animals(
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

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.reasons == ()

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   assert lion.start_time is not None
   assert lion.end_time is not None
   assert penguin.start_time is not None
   assert penguin.end_time is not None
   assert lion.start_time != '09:00'
   assert result.itinerary.arrival_time == '9:00 AM'


def test_bulk_schedule_animals_rebuild_reschedules_when_all_animals_are_already_scheduled(
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

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()
   assert {
      animal.species
      for animal in result.itinerary.animals
      if has_itinerary_schedule_times( animal.start_time, animal.end_time )
   } == { 'African Lion', 'African Penguin' }
