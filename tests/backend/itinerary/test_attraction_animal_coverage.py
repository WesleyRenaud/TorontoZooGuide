from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.itinerary_stop_resolver import ItineraryStopResolver
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers


KANGAROO = {
   'species': 'Western Grey Kangaroo',
   'exhibit': 'Australasia Outdoor',
}
AMUR_TIGER = {
   'species': 'Amur Tiger',
   'exhibit': 'Eurasia Wilds',
}
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'


def test_bulk_schedule_covers_kangaroo_animal_when_walk_thru_is_packed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ KANGAROO, AMUR_TIGER ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   kangaroo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Western Grey Kangaroo' )
   walk_thru = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )

   assert kangaroo.covered_by_talk is True
   assert kangaroo.start_time == walk_thru.start_time
   assert kangaroo.end_time == walk_thru.end_time

   animal_stops = [
      stop
      for stop in ItineraryStopResolver.resolve( result.itinerary )
      if (
         stop.schedule_item_kind == ScheduleItemKind.ANIMAL
         and 'Western Grey Kangaroo' in stop.item_key )
   ]
   attraction_stops = [
      stop
      for stop in ItineraryStopResolver.resolve( result.itinerary )
      if (
         stop.schedule_item_kind == ScheduleItemKind.ATTRACTION
         and stop.item_key == KANGAROO_WALK_THRU )
   ]

   assert animal_stops == []
   assert attraction_stops
