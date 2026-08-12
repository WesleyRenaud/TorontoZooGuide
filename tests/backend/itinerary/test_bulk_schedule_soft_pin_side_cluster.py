from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.shared.calendar_dates import DateValues
from conftest import DbControllers

VISIT = '2026-06-20'
KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'
INDO_EXHIBITS = [
   'Indo-Malaya Pavilion',
   'Indo-Malaya Outdoor',
   'Malayan Woods Pavilion',
]
AFRICA_EXHIBITS = [
   'Africa Savanna',
   'African Rainforest Pavilion',
]
TUNDRA_EXHIBITS = [
   'Tundra Trek',
]


def _hours(
      attraction: str,
      *,
      weekday_start: str,
      weekday_end: str ) -> dict:
   return {
      'attraction': attraction,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekday_start,
      'weekend_holiday_end_time': weekday_end,
   }


def _scheduled_start_seconds( item: Animal | Attraction ) -> int:
   start_time = getattr( item, 'start_time', None )
   assert start_time is not None
   start_seconds = DateValues.time_value_in_seconds( start_time )
   assert start_seconds is not None
   return start_seconds


def _latest_africa_start( animals: list[ Animal ] ) -> int:
   africa_starts = [
      _scheduled_start_seconds( animal )
      for animal in animals
      if animal.exhibit in AFRICA_EXHIBITS and animal.start_time is not None
   ]
   assert africa_starts
   return max( africa_starts )


def _latest_indo_start( animals: list[ Animal ] ) -> int:
   indo_starts = [
      _scheduled_start_seconds( animal )
      for animal in animals
      if animal.exhibit in INDO_EXHIBITS and animal.start_time is not None
   ]
   assert indo_starts
   return max( indo_starts )


def _earliest_tundra_start( animals: list[ Animal ] ) -> int:
   tundra_starts = [
      _scheduled_start_seconds( animal )
      for animal in animals
      if animal.exhibit in TUNDRA_EXHIBITS and animal.start_time is not None
   ]
   assert tundra_starts
   return min( tundra_starts )


def _set_itinerary_with_kangaroo_hours(
      *,
      kangaroo_end: str,
      departure_time: str ) -> None:
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours(
         KANGAROO_WALK_THRU,
         weekday_start='11:00 AM',
         weekday_end=kangaroo_end ) )

   indo = itinerary_animals_for_exhibits( INDO_EXHIBITS, visit_date=VISIT )
   africa = itinerary_animals_for_exhibits( AFRICA_EXHIBITS, visit_date=VISIT )
   tundra = itinerary_animals_for_exhibits( TUNDRA_EXHIBITS, visit_date=VISIT )

   assert ItineraryCoordinator.set_itinerary(
      date=VISIT,
      arrival_time='11:00 AM',
      departure_time=departure_time,
      animals=[ *indo, *africa, *tundra ],
      attractions=[ KANGAROO_WALK_THRU ],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[
         *INDO_EXHIBITS,
         *AFRICA_EXHIBITS,
         *TUNDRA_EXHIBITS,
      ],
      confirming_attraction_without_animal=True,
   ).success


def test_bulk_schedule_defers_kangaroo_after_south_and_tundra(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """When hours allow: Indo → Africa → Tundra → Kangaroo Walk-Thru."""
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_itinerary_with_kangaroo_hours(
      kangaroo_end='6:00 PM',
      departure_time='18:00' )

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   kangaroo = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   kangaroo_start = _scheduled_start_seconds( kangaroo )
   africa_start = _latest_africa_start( result.itinerary.animals )
   indo_start = _latest_indo_start( result.itinerary.animals )
   tundra_start = _earliest_tundra_start( result.itinerary.animals )

   assert indo_start < kangaroo_start
   assert africa_start < kangaroo_start
   assert tundra_start < kangaroo_start
   assert indo_start < tundra_start
   assert africa_start < tundra_start
   africa_before = [
      _scheduled_start_seconds( animal )
      for animal in result.itinerary.animals
      if animal.exhibit in AFRICA_EXHIBITS
      and animal.start_time is not None
      and _scheduled_start_seconds( animal ) < kangaroo_start
   ]
   africa_after = [
      _scheduled_start_seconds( animal )
      for animal in result.itinerary.animals
      if animal.exhibit in AFRICA_EXHIBITS
      and animal.start_time is not None
      and _scheduled_start_seconds( animal ) > kangaroo_start
   ]
   assert africa_before
   assert not africa_after


def test_bulk_schedule_front_loads_kangaroo_before_south_when_hours_tight(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   """When Kangaroo would miss close after south+tundra: Kangaroo → Tundra first."""
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_itinerary_with_kangaroo_hours(
      kangaroo_end='12:30 PM',
      departure_time='18:00' )

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   kangaroo = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == KANGAROO_WALK_THRU )
   kangaroo_start = _scheduled_start_seconds( kangaroo )
   kangaroo_end = DateValues.time_value_in_seconds( kangaroo.end_time )
   assert kangaroo_end is not None
   assert kangaroo_end <= DateValues.time_value_in_seconds( '12:30 PM' )

   tundra_start = _earliest_tundra_start( result.itinerary.animals )
   africa_starts = [
      _scheduled_start_seconds( animal )
      for animal in result.itinerary.animals
      if animal.exhibit in AFRICA_EXHIBITS and animal.start_time is not None
   ]
   assert africa_starts
   earliest_africa = min( africa_starts )

   assert kangaroo_start < earliest_africa
   assert tundra_start < earliest_africa
   assert kangaroo_start <= tundra_start
   africa_between = [
      start
      for start in africa_starts
      if kangaroo_start < start < tundra_start
   ]
   assert not africa_between
