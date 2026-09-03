from __future__ import annotations

from datetime import date

import pytest

from api.models.zoo_hours import ZooHours
from api.shared.calendar_dates import CalendarDates
from api.types import Types
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from api.zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from api.zoo_hours.domain.zoo_hours_builder import ZooHoursBuilder

VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
DATE_KEY = '2026-06-15'
EARLY_ADMISSION = '9:00 AM'
OPEN_TIME = '9:30 AM'
LAST_ADMISSION = '6:00 PM'
CLOSE_TIME = '6:30 PM'

ZOO_HOURS = ZooHours(
   date=DATE_KEY,
   early_admission_time=EARLY_ADMISSION,
   open_time=OPEN_TIME,
   last_admission_time=LAST_ADMISSION,
   close_time=CLOSE_TIME )

def Test_GetZooHours_TestPresentRecord_ExpectBuilt(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoo_hours_record = object()

   monkeypatch.setattr(
      CalendarDates,
      'visit_target_date',
      lambda *_args, **_kwargs: VISIT_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda _conn, operating_date: zoo_hours_record if operating_date == VISIT_DATE else None )
   monkeypatch.setattr(
      ZooHoursBuilder,
      'build',
      lambda record: ZOO_HOURS if record is zoo_hours_record else None )

   assert ZooHoursCoordinator.get_zoo_hours(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) is ZOO_HOURS

def Test_GetZooHours_TestMissingRecord_ExpectNone(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      CalendarDates,
      'visit_target_date',
      lambda *_args, **_kwargs: VISIT_DATE )
   monkeypatch.setattr(
      ZooHoursProvider,
      'fetch_zoo_hours_record',
      lambda _conn, operating_date: None )

   assert ZooHoursCoordinator.get_zoo_hours(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) is None
