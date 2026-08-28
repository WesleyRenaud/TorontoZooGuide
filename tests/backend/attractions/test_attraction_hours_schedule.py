from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.request_connection_provider import RequestConnectionProvider
from conftest import DbControllers


ATTRACTION = 'Conservation Carousel'


def _hours_payload(
      *,
      start_date: str,
      end_date: str | None,
      weekday_start: str = '10:00 AM',
      weekday_end: str = '4:00 PM',
      weekend_start: str = '10:00 AM',
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


def test_set_attraction_hours_schedule_saves_and_resolves_blank_dates(
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

   records = AttractionHoursScheduleProvider.fetch_hours_schedule_records( RequestConnectionProvider.get() )
   matching = [
      record
      for record in records
      if record.attraction == ATTRACTION
   ]

   assert len( matching ) == 1
   assert matching[ 0 ].schedule_start_date == '2026-06-15'
   assert matching[ 0 ].schedule_end_date is None
   assert matching[ 0 ].weekday_start_time == '10:00 AM'
   assert matching[ 0 ].weekday_end_time == '4:00 PM'
   assert matching[ 0 ].weekend_holiday_start_time == '11:00 AM'
   assert matching[ 0 ].weekend_holiday_end_time == '4:00 PM'


def test_set_attraction_hours_schedule_rejects_overlapping_ranges(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-15',
         end_date='2026-07-15' ) ) is False

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-07-01',
         end_date='2026-07-31' ) )


def test_replace_attraction_hours_schedule_overlaps(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-06-30' ) )

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         start_date='2026-06-15',
         end_date='2026-07-15',
         weekday_start='11:00 AM',
         weekday_end='3:00 PM' ) )

   matching = [
      record
      for record in AttractionHoursScheduleProvider.fetch_hours_schedule_records( RequestConnectionProvider.get() )
      if record.attraction == ATTRACTION
   ]

   assert len( matching ) == 1
   assert matching[ 0 ].schedule_start_date == '2026-06-15'
   assert matching[ 0 ].schedule_end_date == '2026-07-15'
   assert matching[ 0 ].weekday_start_time == '11:00 AM'


def test_trim_attraction_hours_schedule_overlaps_copies_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-01',
         end_date='2026-07-31',
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='10:00 AM',
         weekend_end='6:00 PM' ) )

   assert AttractionCoordinator.trim_attraction_hours_schedule_overlaps(
      **_hours_payload(
         start_date='2026-06-15',
         end_date='2026-06-20',
         weekday_start='11:00 AM',
         weekday_end='3:00 PM',
         weekend_start='11:00 AM',
         weekend_end='4:00 PM' ) )

   matching = sorted(
      [
         record
         for record in AttractionHoursScheduleProvider.fetch_hours_schedule_records( RequestConnectionProvider.get() )
         if record.attraction == ATTRACTION
      ],
      key=lambda record: record.schedule_start_date )

   assert [
      (
         record.schedule_start_date,
         record.schedule_end_date,
         record.weekday_start_time,
         record.weekend_holiday_end_time,
      )
      for record in matching
   ] == [
      ( '2026-06-01', '2026-06-14', '10:00 AM', '6:00 PM' ),
      ( '2026-06-15', '2026-06-20', '11:00 AM', '4:00 PM' ),
      ( '2026-06-21', '2026-07-31', '10:00 AM', '6:00 PM' ),
   ]


def test_get_attraction_hours_schedule_time_bounds(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
      start_date='2026-06-15',
      end_date='2026-06-30' )

   assert bounds.weekday.open_time == '09:30'
   assert bounds.weekday.close_time == '18:00'
   assert bounds.weekend_holiday.open_time == '09:30'
   assert bounds.weekend_holiday.close_time == '19:00'


def test_get_attraction_hours_schedule_time_bounds_uses_restrictive_hours(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
      start_date='2026-06-15',
      end_date='2026-10-25' )

   assert bounds.weekday.open_time == '09:30'
   assert bounds.weekday.close_time == '16:30'
   assert bounds.weekend_holiday.open_time == '09:30'
   assert bounds.weekend_holiday.close_time == '16:30'


def test_set_attraction_hours_rejects_times_outside_range_zoo_hours(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   try:
      AttractionCoordinator.set_attraction_hours_schedule(
         **_hours_payload(
            start_date='2026-06-15',
            end_date='2026-10-25',
            weekday_start='10:00 AM',
            weekday_end='5:00 PM' ) )
      raised = False
   except ValueError:
      raised = True

   assert raised


def test_set_attraction_hours_allows_summer_weekday_close_in_summer_range(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionCoordinator.set_attraction_hours_schedule(
      **_hours_payload(
         start_date='2026-06-15',
         end_date='2026-09-04',
         weekday_start='10:00 AM',
         weekday_end='5:00 PM' ) )


def test_get_attraction_hours_schedule_time_bounds_from_weekend(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
      start_date='2026-06-20',
      end_date='2026-06-22' )

   assert bounds.weekday.operating_date == '2026-06-22'
   assert bounds.weekend_holiday.operating_date == '2026-06-20'


def test_get_attraction_hours_schedule_time_bounds_requires_zoo_hours(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   cur = db.conn.cursor()

   try:
      cur.execute( 'DELETE FROM ZooHours;' )
      db.conn.commit()
   finally:
      cur.close()

   try:
      AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
         start_date='2026-06-15',
         end_date='2026-06-30' )
      raised = False
   except ValueError:
      raised = True

   assert raised
