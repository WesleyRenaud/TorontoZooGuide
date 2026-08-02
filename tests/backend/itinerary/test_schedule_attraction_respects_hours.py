from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, schedule_itinerary_item

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


SPLASH_ISLAND = 'Splash Island'


def _hours_payload(
      attraction: str,
      *,
      weekday_start: str,
      weekday_end: str,
      weekend_start: str,
      weekend_end: str ) -> dict:
   return {
      'attraction': attraction,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def _set_splash_island_weekend_hours() -> None:
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         SPLASH_ISLAND,
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='12:00 PM',
         weekend_end='5:00 PM' ) )


def test_schedule_attraction_at_default_time_uses_attraction_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '12:00 PM'
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'


def test_schedule_attraction_at_default_time_waits_for_open_after_arrival(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna' ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '12:00 PM'
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'


def test_schedule_attraction_before_open_requires_hours_confirmation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND,
      start_time='10:00 AM' )

   assert result.status == ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS


def test_schedule_attraction_adjust_before_open_starts_at_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND,
      start_time='10:00 AM',
      confirming_attraction_outside_operating_hours=True )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '12:00 PM'
   assert splash.end_time == '1:00 PM'


def test_schedule_attraction_after_close_requires_hours_confirmation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND,
      start_time='5:30 PM' )

   assert result.status == ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS


def test_schedule_attraction_adjust_after_close_ends_at_close(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND,
      start_time='5:30 PM',
      confirming_attraction_outside_operating_hours=True )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '4:00 PM'
   assert splash.end_time == '5:00 PM'


def test_schedule_attraction_that_overruns_close_requires_hours_confirmation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND,
      start_time='4:30 PM' )

   assert result.status == ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS


def test_schedule_attraction_extends_departure_when_visit_window_is_full(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='12:00 PM',
      departure_time='12:30 PM',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna',
      start_time='12:00 PM',
      duration_minutes=30 ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == '12:30 PM'
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'
   assert result.itinerary.departure_time == splash.end_time
