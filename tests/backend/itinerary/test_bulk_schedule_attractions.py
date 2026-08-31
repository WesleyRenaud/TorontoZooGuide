from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CAROUSEL, entrance_travel_seconds_to_animal, LION_ITINERARY_ENTRY, schedule_time_after_seconds

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
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
SPLASH_ISLAND = 'Splash Island'


def test_bulk_schedule_packs_attraction_only_loop(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == schedule_time_after_seconds(
      '9:30 AM',
      WalkTravelTimeCalculator.seconds_between_nodes(
         WalkGraphProvider.fetch(),
         WalkGraphProvider.fetch()[ 'entrance_node_id' ],
         ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( SPLASH_ISLAND ),
      ),
   )
   assert splash.end_time is not None


def test_bulk_schedule_covers_kangaroo_when_walk_thru_is_selected(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ KANGAROO, AMUR_TIGER ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   kangaroo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Western Grey Kangaroo' )
   walk_thru = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   tiger = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Amur Tiger' )

   assert kangaroo.covered_by_talk is True
   assert kangaroo.start_time == walk_thru.start_time
   assert kangaroo.end_time == walk_thru.end_time
   assert walk_thru.start_time is not None
   assert tiger.start_time is not None
   assert walk_thru.start_time < tiger.start_time


def test_bulk_schedule_repacks_attractions_after_clear(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   first = ItineraryCoordinator.bulk_schedule_itinerary()
   assert first.success
   carousel_before = next(
      attraction
      for attraction in first.itinerary.attractions
      if attraction.name == CAROUSEL )
   assert carousel_before.start_time is not None

   second = ItineraryCoordinator.bulk_schedule_itinerary()
   assert second.success
   carousel_after = next(
      attraction
      for attraction in second.itinerary.attractions
      if attraction.name == CAROUSEL )
   assert carousel_after.start_time is not None
