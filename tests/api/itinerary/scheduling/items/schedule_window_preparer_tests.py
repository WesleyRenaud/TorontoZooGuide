from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.core.scheduling_anchor_resolver import SchedulingAnchorResolver
from api.itinerary.scheduling.items.schedule_window_preparer import ScheduleWindowPreparer
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType, Position
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
   window = ScheduleWindowPreparer.zoo_hours_window_seconds( ZOO_HOURS )

   assert window == (
      DateValues.time_value_in_seconds( ZOO_HOURS.open_time ),
      DateValues.time_value_in_seconds( ZOO_HOURS.close_time ),
   )


def Test_ZooHoursWindowSeconds_TestEarlyAdmission_ExpectEarlierAnchor() -> None:
   window = ScheduleWindowPreparer.zoo_hours_window_seconds(
      EARLY_ADMISSION_ZOO_HOURS,
      allow_early_admission=True )

   assert window == (
      DateValues.time_value_in_seconds( EARLY_ADMISSION_ZOO_HOURS.early_admission_time ),
      DateValues.time_value_in_seconds( EARLY_ADMISSION_ZOO_HOURS.close_time ),
   )


def Test_ZooHoursWindowSeconds_TestFixedZooStartTimes_ExpectEarlierAnchor() -> None:
   earlier_fixed_start = '09:00 AM'

   window = ScheduleWindowPreparer.zoo_hours_window_seconds(
      ZOO_HOURS,
      fixed_zoo_start_times=[ earlier_fixed_start ] )

   assert window == (
      DateValues.time_value_in_seconds( earlier_fixed_start ),
      DateValues.time_value_in_seconds( ZOO_HOURS.close_time ),
   )


def Test_ZooHoursWindowSeconds_TestStandardHours_ExpectZooCloseEnd() -> None:
   window = ScheduleWindowPreparer.zoo_hours_window_seconds( ZOO_HOURS )

   assert window[ Position.SECOND ] == DateValues.time_value_in_seconds(
      ZOO_HOURS.close_time )


def Test_DayEndSeconds_TestGuestDepartureBeforeClose_ExpectDepartureSeconds() -> None:
   departure_time = '3:00 PM'

   seconds = SchedulingAnchorResolver.day_end_seconds( ZOO_HOURS, departure_time )

   assert seconds == DateValues.time_value_in_seconds( departure_time )


def Test_ZooHoursWindowSeconds_TestMissingHours_ExpectNone() -> None:
   window = ScheduleWindowPreparer.zoo_hours_window_seconds( None )

   assert window is None


def Test_PrepareZooHours_TestGuestDepartureBeforeClose_ExpectZooCloseWindow(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=EARLY_ADMISSION_ZOO_HOURS.operating_date,
      arrival_time='12:20 PM',
      departure_time='3:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: EARLY_ADMISSION_ZOO_HOURS.operating_date )
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
      DateValues.time_value_in_seconds( EARLY_ADMISSION_ZOO_HOURS.open_time ),
      DateValues.time_value_in_seconds( EARLY_ADMISSION_ZOO_HOURS.close_time ),
   )


def Test_PrepareZooHours_TestNoArrivalTime_ExpectOpenAnchor(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=EARLY_ADMISSION_ZOO_HOURS.operating_date,
      arrival_time=None,
      departure_time=None,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: EARLY_ADMISSION_ZOO_HOURS.operating_date )
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

   assert prepared.window[ Position.FIRST ] == DateValues.time_value_in_seconds(
      EARLY_ADMISSION_ZOO_HOURS.open_time )


def Test_PrepareZooHours_TestSuppressedEarlyAdmission_ExpectNineAmAnchor(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=EARLY_ADMISSION_ZOO_HOURS.operating_date,
      arrival_time=None,
      departure_time=None,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: EARLY_ADMISSION_ZOO_HOURS.operating_date )
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

   assert prepared.window[ Position.FIRST ] == DateValues.time_value_in_seconds(
      EARLY_ADMISSION_ZOO_HOURS.early_admission_time )


def Test_Prepare_TestMissingVisitDate_ExpectDateNotSetResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_Prepare_TestValidInputs_ExpectPreparedWindow(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: ZOO_HOURS.operating_date )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: ZOO_HOURS )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: False )

   prepared = ScheduleWindowPreparer.prepare(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert prepared.window == (
      DateValues.time_value_in_seconds( saved_itinerary.arrival_time ),
      DateValues.time_value_in_seconds( saved_itinerary.departure_time ),
   )


def Test_Prepare_TestUnparseableVisitDate_ExpectDateNotSetResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: ZOO_HOURS.operating_date )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.DateValues.parse_date_value',
      lambda value: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_Prepare_TestUnavailableScheduleWindow_ExpectUnavailableResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: ZOO_HOURS.operating_date )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: False )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE


def Test_PrepareZooHours_TestMissingVisitDate_ExpectDateNotSetResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_PrepareZooHours_TestUnparseableVisitDate_ExpectDateNotSetResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: ZOO_HOURS.operating_date )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.DateValues.parse_date_value',
      lambda value: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.ITINERARY_DATE_NOT_SET


def Test_PrepareZooHours_TestUnavailableScheduleWindow_ExpectUnavailableResult(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value=ZOO_HOURS.operating_date,
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryProvider.fetch_itinerary_date',
      lambda conn: ZOO_HOURS.operating_date )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ZooHoursProvider.fetch_zoo_hours_record',
      lambda conn, visit_date: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItineraryStatusProvider.is_itinerary_error_suppressed',
      lambda conn, error_type: False )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.schedule_window_preparer.ItinerarySaveResultBuilder.save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=None ) )

   result = ScheduleWindowPreparer.prepare_zoo_hours(
      sqlite3.connect( ':memory:' ),
      saved_itinerary,
      visit_date_temp=None )

   assert isinstance( result, ItinerarySaveResult )
   assert result.status == ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE
