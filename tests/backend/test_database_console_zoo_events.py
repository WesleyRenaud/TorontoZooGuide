from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.events.coordinators.event_coordinator import EventCoordinator
from conftest import DbControllers


def test_create_event_persists_event_fields( db: DbControllers ) -> None:
   assert EventCoordinator.create_event(
      name='Conservation Carousel Ride Night',
      location='Front Courtyard',
      description='Evening carousel rides for a special cause.',
      link='https://www.torontozoo.com/events/carousel-night',
      start_date='2026-06-15',
      end_date='2026-06-30' ) is True

   assert db.conn is not None
   row = db.conn.execute(
      """   SELECT NAME, LOCATION, DESCRIPTION, LINK, START_DATE, END_DATE
            FROM ZooEvent
            WHERE NAME = ?;
      """,
      ( 'Conservation Carousel Ride Night', ) ).fetchone()

   assert row is not None
   assert tuple( row ) == (
      'Conservation Carousel Ride Night',
      'Front Courtyard',
      'Evening carousel rides for a special cause.',
      'https://www.torontozoo.com/events/carousel-night',
      '2026-06-15',
      '2026-06-30'
   )


def test_create_event_persists_open_ended_event( db: DbControllers ) -> None:
   assert EventCoordinator.create_event(
      name='Conservation Carousel Ride Night',
      location='Front Courtyard',
      description='Evening carousel rides for a special cause.',
      link='https://www.torontozoo.com/events/carousel-night',
      start_date='2026-06-15',
      end_date=None ) is True

   assert db.conn is not None
   row = db.conn.execute(
      """   SELECT START_DATE, END_DATE
            FROM ZooEvent
            WHERE NAME = ?;
      """,
      ( 'Conservation Carousel Ride Night', ) ).fetchone()

   assert row is not None
   assert tuple( row ) == ( '2026-06-15', None )


def test_create_event_rejects_duplicate_name_and_start_date(
      db: DbControllers ) -> None:
   assert EventCoordinator.create_event(
      name='Conservation Carousel Ride Night',
      location='Front Courtyard',
      description='First description.',
      link='https://www.torontozoo.com/events/one',
      start_date='2026-06-15',
      end_date=None ) is True

   assert EventCoordinator.create_event(
      name='Conservation Carousel Ride Night',
      location='Africa Savanna',
      description='Second description.',
      link='https://www.torontozoo.com/events/two',
      start_date='2026-06-15',
      end_date=None ) is False

   assert EventCoordinator.create_event(
      name='Conservation Carousel Ride Night',
      location='Africa Savanna',
      description='Second description.',
      link='https://www.torontozoo.com/events/two',
      start_date='2026-07-01',
      end_date=None ) is True


def test_get_events_for_visit_date_includes_upcoming_and_excludes_expired_events(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert EventCoordinator.create_event(
      name='Active open-ended event',
      location='Front Courtyard',
      description='Still happening.',
      link='https://www.torontozoo.com/events/active',
      start_date='2026-06-01',
      end_date=None ) is True

   assert EventCoordinator.create_event(
      name='Active ranged event',
      location='Africa Savanna',
      description='Ends later.',
      link='https://www.torontozoo.com/events/ranged',
      start_date='2026-06-10',
      end_date='2026-06-30' ) is True

   assert EventCoordinator.create_event(
      name='Future event',
      location='Indo-Malaya',
      description='Starts later.',
      link='https://www.torontozoo.com/events/future',
      start_date='2026-07-01',
      end_date='2026-07-15' ) is True

   assert EventCoordinator.create_event(
      name='Expired event',
      location='Canadian Domain',
      description='Already ended.',
      link='https://www.torontozoo.com/events/expired',
      start_date='2026-05-01',
      end_date='2026-05-31' ) is True

   events = EventCoordinator.get_events_for_visit_date(
      month='June',
      day=15,
      year=2026 )

   assert [ event.name for event in events ] == [
      'Active open-ended event',
      'Active ranged event',
      'Future event',
   ]
