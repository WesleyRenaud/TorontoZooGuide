from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.itinerary.attraction_item_key import AttractionScheduleItemKey
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from conftest import DbControllers


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'


def _australasia_exhibits() -> list[ str ]:
   selected: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name == 'Australasia':
         selected.extend( region.exhibits )

   assert selected
   return selected


def test_unschedule_covering_attraction_clears_visit_times_when_attraction_left_unscheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   exhibits = _australasia_exhibits()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=itinerary_animals_for_exhibits(
         exhibits,
         visit_date='2026-06-20' ),
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=exhibits,
   ).success

   scheduled = ItineraryCoordinator.bulk_schedule_animals()

   assert scheduled.success
   assert scheduled.itinerary.arrival_time is not None
   assert scheduled.itinerary.departure_time is not None

   result = ItineraryCoordinator.unschedule_itinerary_item(
      AttractionScheduleItemKey( name=KANGAROO_WALK_THRU ) )

   assert result.success

   walk_thru = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   kangaroo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Western Grey Kangaroo' )

   assert walk_thru.start_time is None
   assert walk_thru.end_time is None
   assert kangaroo.covered_by_talk is False
   assert kangaroo.start_time is not None
   assert kangaroo.end_time is not None
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None
