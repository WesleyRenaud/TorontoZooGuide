from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.models import Transportation
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from conftest import DbControllers


TRANSPORTATION = 'Zoomobile'


def _hours_payload(
      *,
      start_date: str,
      end_date: str | None,
      weekday_start: str = '10:00 AM',
      weekday_end: str = '4:00 PM',
      weekend_start: str = '11:00 AM',
      weekend_end: str = '5:00 PM' ) -> dict:
   return {
      'attraction': TRANSPORTATION,
      'start_date': start_date,
      'end_date': end_date,
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def _transportation_for_visit(
      *,
      day: int,
      month: str,
      year: int ) -> Transportation:
   transportations = TransportationCoordinator.get_transportations(
      day=day,
      month=month,
      year=year )

   return next(
      transportation
      for transportation in transportations
      if transportation.name == TRANSPORTATION
   )


def test_get_transportations_resolves_weekday_hours_from_joined_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   # Monday
   transportation = _transportation_for_visit( day=15, month='June', year=2026 )

   assert transportation.open_time == '10:00 AM'
   assert transportation.close_time == '4:00 PM'
   assert transportation.free_with_admission is False


def test_get_transportations_resolves_weekend_hours_from_joined_schedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   # Saturday
   transportation = _transportation_for_visit( day=20, month='June', year=2026 )

   assert transportation.open_time == '11:00 AM'
   assert transportation.close_time == '5:00 PM'


def test_get_transportations_matching_query_filters_by_name(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   matching = TransportationCoordinator.get_transportations_matching_query(
      query='zoom',
      day=15,
      month='June',
      year=2026 )
   missing = TransportationCoordinator.get_transportations_matching_query(
      query='carousel',
      day=15,
      month='June',
      year=2026 )

   assert [ transportation.name for transportation in matching ] == [ TRANSPORTATION ]
   assert missing == []
