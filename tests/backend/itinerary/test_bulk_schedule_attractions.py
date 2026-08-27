from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CAROUSEL, entrance_travel_seconds_to_animal, LION_ITINERARY_ENTRY, schedule_time_after_seconds

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.routing.walk_travel_time import travel_time_seconds_between_nodes
from api.itinerary.scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from api.itinerary.scheduling.bulk.loop_schedule_unit_builder import LoopScheduleUnitBuilder
from api.itinerary.scheduling.bulk.master_route_loop_stop_grouper import MasterRouteLoopStopGrouper
from api.itinerary.scheduling.bulk.master_route_stop_sorter import MasterRouteStopSorter
from api.itinerary.scheduling.items.schedule_item_travel_time import walk_node_id_for_attraction
from api.itinerary.warnings.bulk_schedule_itinerary_warning_builder import BulkScheduleItineraryWarningBuilder
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
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
      travel_time_seconds_between_nodes(
         load_walk_graph(),
         load_walk_graph()[ 'entrance_node_id' ],
         walk_node_id_for_attraction( SPLASH_ISLAND ),
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


def test_build_loop_schedule_units_orders_woven_attraction_between_animals() -> None:
   stops = [
      ItineraryAnimalRecord(
         species='Amur Tiger',
         exhibit='Eurasia Wilds',
         old_likelihood=None,
         new_likelihood=100 ),
      ItineraryAttractionRecord(
         attraction=KANGAROO_WALK_THRU,
         old_likelihood=None,
         new_likelihood=100 ),
      ItineraryAnimalRecord(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         old_likelihood=None,
         new_likelihood=100 ),
   ]
   loop_units = LoopScheduleUnitBuilder.build(
      MasterRouteLoopStopGrouper.group( stops ) )

   australasia = next(
      unit
      for unit in loop_units
      if unit.loop_id == 'australasia' )
   ordered_names = [
      stop.attraction
      if isinstance( stop, ItineraryAttractionRecord )
      else stop.species
      for stop in australasia.stops
   ]

   assert ordered_names == [
      'Western Grey Kangaroo',
      KANGAROO_WALK_THRU,
      'Amur Tiger',
   ]


def test_master_route_stop_sorter_orders_unmapped_attractions_by_name() -> None:
   unmapped_b = ItineraryAttractionRecord(
      attraction='ZZZ Unmapped Attraction B',
      old_likelihood=None,
      new_likelihood=100 )
   unmapped_a = ItineraryAttractionRecord(
      attraction='AAA Unmapped Attraction A',
      old_likelihood=None,
      new_likelihood=100 )
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100 )

   ordered = MasterRouteStopSorter.sort( [ unmapped_b, lion, unmapped_a ] )

   assert ordered[ 0 ].species == 'African Lion'
   assert [
      stop.attraction
      for stop in ordered[ 1: ]
   ] == [
      'AAA Unmapped Attraction A',
      'ZZZ Unmapped Attraction B',
   ]


def test_build_bulk_schedule_not_enough_time_issue_includes_attractions() -> None:
   issue = BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
         ItineraryAttractionRecord(
            attraction=CAROUSEL,
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME
   assert [
      ( item.name, item.item_type, item.location )
      for item in issue.items
   ] == [
      ( 'African Lion', ItinerarySaveIssueItemType.ANIMAL, 'Africa Savanna' ),
      ( CAROUSEL, ItinerarySaveIssueItemType.ATTRACTION, '' ),
   ]


def test_walk_node_id_for_unknown_attraction_is_none() -> None:
   assert LoopScheduleUnitBuilder.walk_node_id_for_stop(
      ItineraryAttractionRecord(
         attraction='Not A Real Attraction',
         old_likelihood=None,
         new_likelihood=100 ) ) is None


def test_attractions_for_bulk_schedule_handles_missing_and_scheduled_only(
      db: DbControllers ) -> None:
   assert BulkScheduleStopSelector.attractions(
      None,
      only_previously_scheduled=False ) == []
   assert BulkScheduleStopSelector.stops(
      None,
      only_previously_scheduled=False ) == []

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   assert [
      attraction.attraction
      for attraction in BulkScheduleStopSelector.attractions(
         saved,
         only_previously_scheduled=False )
   ] == [ CAROUSEL ]
   assert BulkScheduleStopSelector.attractions(
      saved,
      only_previously_scheduled=True ) == []
