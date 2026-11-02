from __future__ import annotations

from datetime import date
from datetime import datetime

from api.app_string_provider import AppStringProvider
from api.attractions.data_access.attraction_closure_record import AttractionClosureRecord
from api.attractions.status.attraction_season_closure_builder import AttractionSeasonClosureBuilder


ATTRACTION_NAME = 'Conservation Carousel'
CUSTOM_MESSAGE = 'Closed until the ride reopens in spring.'
START_DATE = '2026-11-02'
VISIT_DATE = date( 2026, 11, 2 )


def Test_Build_TestEmptyMessage_ExpectSeasonMessage() -> None:
   status = AttractionSeasonClosureBuilder.build(
      attraction=ATTRACTION_NAME,
      start_date=None,
      end_date=None,
      message='' )

   assert status.attraction == ATTRACTION_NAME
   assert status.start_date == datetime.now().date().isoformat()
   assert status.end_date is None
   assert status.is_closed_for_season is True
   assert status.message == AppStringProvider.format(
      'guestStatus.locations.closedForSeason',
      name=ATTRACTION_NAME )


def Test_Build_TestCustomMessage_ExpectMessageRetained() -> None:
   status = AttractionSeasonClosureBuilder.build(
      attraction=ATTRACTION_NAME,
      start_date=START_DATE,
      end_date='2027-04-01',
      message=CUSTOM_MESSAGE )

   assert status.start_date == START_DATE
   assert status.end_date == '2027-04-01'
   assert status.message == CUSTOM_MESSAGE


def Test_IsActiveOnDate_TestMissingDate_ExpectFalse() -> None:
   record = AttractionClosureRecord(
      attraction=ATTRACTION_NAME,
      closed_start=START_DATE,
      closed_end=None,
      closed_message=CUSTOM_MESSAGE,
      is_closed_for_season=True )

   assert AttractionSeasonClosureBuilder.is_active_on_date( record, None ) is False


def Test_IsActiveOnDate_TestMissingRecord_ExpectFalse() -> None:
   assert AttractionSeasonClosureBuilder.is_active_on_date( None, VISIT_DATE ) is False


def Test_IsActiveOnDate_TestInsideWindow_ExpectTrue() -> None:
   record = AttractionClosureRecord(
      attraction=ATTRACTION_NAME,
      closed_start=START_DATE,
      closed_end=None,
      closed_message=CUSTOM_MESSAGE,
      is_closed_for_season=True )

   assert AttractionSeasonClosureBuilder.is_active_on_date( record, VISIT_DATE ) is True
