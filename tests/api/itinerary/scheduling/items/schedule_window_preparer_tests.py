from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.core.scheduling_anchor_resolver import SchedulingAnchorResolver
from api.itinerary.scheduling.items.schedule_window_preparer import ScheduleWindowPreparer
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-15',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)

EARLY_ADMISSION_ZOO_HOURS = ZooHoursRecord(
   operating_date='2026-06-20',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='18:00',
   close_time='19:00',
)


def Test_ZooHoursWindowSeconds_TestStandardHours_ExpectOpenToClose() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS ) == (
      9 * 3600 + 30 * 60,
      19 * 3600,
   )


def Test_ZooHoursWindowSeconds_TestEarlyAdmission_ExpectEarlierAnchor() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      EARLY_ADMISSION_ZOO_HOURS,
      allow_early_admission=True ) == (
      9 * 3600,
      19 * 3600,
   )


def Test_ZooHoursWindowSeconds_TestFixedZooStartTimes_ExpectEarlierAnchor() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS,
      fixed_zoo_start_times=[ '09:00 AM' ] ) == (
      9 * 3600,
      19 * 3600,
   )


def Test_ZooHoursWindowSeconds_TestGuestDepartureBeforeClose_ExpectZooCloseEnd() -> None:
   assert ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS )[ 1 ] == 19 * 3600
   assert SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, '3:00 PM' ) == 15 * 3600


def Test_PrepareZooHours_TestGuestDepartureBeforeClose_ExpectZooCloseWindow(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='12:20 PM',
      departure_time='3:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: EARLY_ADMISSION_ZOO_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: False )

   prepared = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert prepared.window == (
      9 * 3600 + 30 * 60,
      19 * 3600,
   )


def Test_PrepareZooHours_TestNoArrivalTime_ExpectOpenAnchor(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time=None,
      departure_time=None,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: EARLY_ADMISSION_ZOO_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: False )

   prepared = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert prepared.window[ 0 ] == 9 * 3600 + 30 * 60


def Test_PrepareZooHours_TestSuppressedEarlyAdmission_ExpectNineAmAnchor(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time=None,
      departure_time=None,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: '2026-06-20' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: EARLY_ADMISSION_ZOO_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: True )

   prepared = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert prepared.window[ 0 ] == 9 * 3600
