from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.data_access.attraction_animal import fetch_attraction_animal_links
from api.itinerary.attraction_item_key import AttractionScheduleItemKey
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.resolve_itinerary_stops import resolve_itinerary_stops
from api.shared.calendar_dates import DateValues
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


def test_attraction_animal_seed_links_kangaroo_walk_thru(
      db: DbControllers ) -> None:
   links = fetch_attraction_animal_links( db.conn, KANGAROO_WALK_THRU )

   assert [
      (
         link.species,
         link.exhibit,
         link.enclosure_name,
      )
      for link in links
   ] == [
      (
         'Western Grey Kangaroo',
         'Australasia Outdoor',
         None,
      ),
   ]


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

   result = ItineraryCoordinator.bulk_schedule_animals()

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
      for stop in resolve_itinerary_stops( result.itinerary )
      if (
         stop.schedule_item_kind == ScheduleItemKind.ANIMAL
         and 'Western Grey Kangaroo' in stop.item_key )
   ]
   attraction_stops = [
      stop
      for stop in resolve_itinerary_stops( result.itinerary )
      if (
         stop.schedule_item_kind == ScheduleItemKind.ATTRACTION
         and stop.item_key == KANGAROO_WALK_THRU )
   ]

   assert animal_stops == []
   assert attraction_stops


def test_unschedule_covering_attraction_restores_kangaroo_default_duration(
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

   scheduled = ItineraryCoordinator.bulk_schedule_animals()

   assert scheduled.success

   walk_thru_before = next(
      attraction
      for attraction in scheduled.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   tiger_before = next(
      animal
      for animal in scheduled.itinerary.animals
      if animal.species == 'Amur Tiger' )
   walk_thru_start_seconds = DateValues.time_value_in_seconds(
      walk_thru_before.start_time )
   tiger_start_before = DateValues.time_value_in_seconds(
      tiger_before.start_time )

   assert walk_thru_start_seconds is not None
   assert tiger_start_before is not None

   result = ItineraryCoordinator.unschedule_itinerary_item(
      AttractionScheduleItemKey( name=KANGAROO_WALK_THRU ) )

   assert result.success

   kangaroo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Western Grey Kangaroo' )
   tiger_after = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Amur Tiger' )
   walk_thru_after = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )

   assert kangaroo.covered_by_talk is False
   assert kangaroo.start_time == walk_thru_before.start_time
   assert kangaroo.end_time == DateValues.schedule_time_key_from_seconds(
      walk_thru_start_seconds + ( 5 * 60 ) )
   assert walk_thru_after.start_time is None
   assert walk_thru_after.end_time is None

   tiger_start_after = DateValues.time_value_in_seconds( tiger_after.start_time )

   assert tiger_start_after is not None
   assert tiger_start_after < tiger_start_before
