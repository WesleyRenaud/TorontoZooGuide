from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.validation.itinerary_validation import validate_itinerary_attractions
from conftest import DbControllers


def test_validate_attractions_removes_closed_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AttractionCoordinator.set_attraction_as_closed(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel', 'Greenhouse' ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
      old_visit_date='2026-06-15' )

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Greenhouse'
   ] == [ ( 'Greenhouse', 100 ) ]

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Conservation Carousel'
   ] == [ ( 'Conservation Carousel', 0 ) ]


def test_validate_attractions_removes_closure_override_entries(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AttractionCoordinator.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=False,
      message='Open for June.'
   )
   AttractionCoordinator.set_attraction_closure_override(
      attraction='Conservation Carousel',
      start_date='2026-06-15',
      end_date='2026-06-15',
      message='Unavailable.'
   )

   result = validate_itinerary_attractions(
      AttractionCoordinator,
      attractions=[ 'Conservation Carousel' ],
      new_visit_date=date( 2026, 6, 15 ),
      arrival_time='09:30',
      departure_time='17:00',
      old_visit_date='2026-06-15' )

   assert [
      ( d.name, d.new_likelihood )
      for d in result
   ] == [ ( 'Conservation Carousel', 0 ) ]
