from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_bulk_schedule_animals_with_no_itinerary_returns_nothing_to_schedule(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.bulk_schedule_animals()

   assert not result.success
   assert result.status == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED


def test_unschedule_all_itinerary_items_with_no_itinerary_returns_nothing_to_unschedule(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.unschedule_all_itinerary_items()

   assert not result.success
   assert result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED


def test_bulk_schedule_animals_with_no_unscheduled_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert not result.success
   assert result.status == ItineraryErrorType.BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED
   assert result.reasons == []
   assert result.itinerary.animals == []
