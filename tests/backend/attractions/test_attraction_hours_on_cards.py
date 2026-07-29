from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.models import Attraction
from conftest import DbControllers


ATTRACTION = 'Conservation Carousel'


def _hours_payload(
      *,
      start_date: str,
      end_date: str | None,
      weekday_start: str = '10:00 AM',
      weekday_end: str = '4:00 PM',
      weekend_start: str = '11:00 AM',
      weekend_end: str = '5:00 PM' ) -> dict:
   return {
      'attraction': ATTRACTION,
      'start_date': start_date,
      'end_date': end_date,
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def _attraction_for_visit(
      *,
      day: int,
      month: str,
      year: int ) -> Attraction:
   attractions = AttractionCoordinator.get_attractions(
      day=day,
      month=month,
      year=year,
      include_closed_attractions=True )

   return next(
      attraction
      for attraction in attractions
      if attraction.name == ATTRACTION
   )


def test_get_attractions_resolves_weekday_hours_from_joined_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   # Monday
   attraction = _attraction_for_visit( day=15, month='June', year=2026 )

   assert attraction.open_time == '10:00 AM'
   assert attraction.close_time == '4:00 PM'


def test_get_attractions_resolves_weekend_hours_from_joined_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   # Saturday
   attraction = _attraction_for_visit( day=20, month='June', year=2026 )

   assert attraction.open_time == '11:00 AM'
   assert attraction.close_time == '5:00 PM'


def test_get_attractions_resolves_holiday_hours_from_joined_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-07-31',
         weekend_start='12:00 PM',
         weekend_end='6:00 PM' ) )

   # Canada Day (Wednesday holiday)
   attraction = _attraction_for_visit( day=1, month='July', year=2026 )

   assert attraction.open_time == '12:00 PM'
   assert attraction.close_time == '6:00 PM'


def test_get_attractions_uses_open_ended_hours_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='',
         end_date='',
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='11:00 AM',
         weekend_end='4:00 PM' ) )

   attraction = _attraction_for_visit( day=17, month='August', year=2026 )

   assert attraction.open_time == '10:00 AM'
   assert attraction.close_time == '4:00 PM'


def test_get_attractions_leaves_hours_null_without_matching_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   attraction = _attraction_for_visit( day=15, month='August', year=2026 )

   assert attraction.open_time is None
   assert attraction.close_time is None
