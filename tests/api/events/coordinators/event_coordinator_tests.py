from __future__ import annotations

from datetime import date

from api_test_support.frozen_datetime import patch_database_today
from api_test_support.seeded_database import SeededDatabase
import pytest

from api.events.coordinators.event_coordinator import EventCoordinator


EVENT_NAME = 'Conservation Carousel Ride Night'
EVENT_LOCATION = 'Front Courtyard'
EVENT_DESCRIPTION = 'Evening carousel rides for a special cause.'
EVENT_LINK = 'https://www.torontozoo.com/events/carousel-night'
EVENT_START_DATE = '2026-06-15'
EVENT_END_DATE = '2026-06-30'


def Test_CreateEvent_TestValidEvent_ExpectPersistsEventFields(
      db: SeededDatabase ) -> None:
   assert EventCoordinator.create_event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description=EVENT_DESCRIPTION,
      link=EVENT_LINK,
      start_date=EVENT_START_DATE,
      end_date=EVENT_END_DATE ) is True

   assert db.conn is not None
   row = db.conn.execute(
      """   SELECT NAME, LOCATION, DESCRIPTION, LINK, START_DATE, END_DATE
            FROM ZooEvent
            WHERE NAME = ?;
      """,
      ( EVENT_NAME, ) ).fetchone()

   assert row is not None
   assert tuple( row ) == (
      EVENT_NAME,
      EVENT_LOCATION,
      EVENT_DESCRIPTION,
      EVENT_LINK,
      EVENT_START_DATE,
      EVENT_END_DATE,
   )


def Test_CreateEvent_TestOpenEndedEvent_ExpectPersistsNullEndDate(
      db: SeededDatabase ) -> None:
   assert EventCoordinator.create_event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description=EVENT_DESCRIPTION,
      link=EVENT_LINK,
      start_date=EVENT_START_DATE,
      end_date=None ) is True

   assert db.conn is not None
   row = db.conn.execute(
      """   SELECT START_DATE, END_DATE
            FROM ZooEvent
            WHERE NAME = ?;
      """,
      ( EVENT_NAME, ) ).fetchone()

   assert row is not None
   assert tuple( row ) == ( EVENT_START_DATE, None )


def Test_CreateEvent_TestDuplicateNameAndStartDate_ExpectRejectsSecondInsert(
      db: SeededDatabase ) -> None:
   assert EventCoordinator.create_event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description='First description.',
      link='https://www.torontozoo.com/events/one',
      start_date=EVENT_START_DATE,
      end_date=None ) is True

   assert EventCoordinator.create_event(
      name=EVENT_NAME,
      location='Africa Savanna',
      description='Second description.',
      link='https://www.torontozoo.com/events/two',
      start_date=EVENT_START_DATE,
      end_date=None ) is False

   assert EventCoordinator.create_event(
      name=EVENT_NAME,
      location='Africa Savanna',
      description='Second description.',
      link='https://www.torontozoo.com/events/two',
      start_date='2026-07-01',
      end_date=None ) is True


def Test_GetEventsForVisitDate_TestMixedEventDates_ExpectUpcomingAndExcludesExpired(
      db: SeededDatabase,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   patch_database_today( monkeypatch, date( 2026, 6, 15 ) )

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
