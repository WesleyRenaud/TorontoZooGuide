from __future__ import annotations

from datetime import date

from api.exhibits.data_access.exhibit_closure_record import ExhibitClosureRecord
from api.exhibits.status.exhibit_status_builder import ExhibitStatusBuilder


EXHIBIT_NAME = 'Africa Savanna'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'
DEFAULT_CLOSED_MESSAGE = 'The Africa Savanna is temporarily closed.'
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
VISIT_DATE = date( 2026, 6, 15 )
BEFORE_VISIT_DATE = date( 2026, 5, 31 )
AFTER_VISIT_DATE = date( 2026, 7, 1 )


def Test_BuildClosedStatus_TestCustomMessage_ExpectMessageRetained() -> None:
   status = ExhibitStatusBuilder.build_closed_status(
      exhibit=EXHIBIT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message=CUSTOM_CLOSED_MESSAGE )

   assert status.exhibit == EXHIBIT_NAME
   assert status.start_date == CLOSURE_START_DATE
   assert status.end_date == CLOSURE_END_DATE
   assert status.message == CUSTOM_CLOSED_MESSAGE


def Test_BuildClosedStatus_TestEmptyMessage_ExpectDefaultGuestStatusMessage() -> None:
   status = ExhibitStatusBuilder.build_closed_status(
      exhibit=EXHIBIT_NAME,
      start_date=CLOSURE_START_DATE,
      end_date=CLOSURE_END_DATE,
      message='' )

   assert status.message == DEFAULT_CLOSED_MESSAGE


def Test_IsClosureActiveOnVisitDate_TestInactiveClosure_ExpectFalse() -> None:
   assert ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=False,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=VISIT_DATE ) is False


def Test_IsClosureActiveOnVisitDate_TestMissingVisitDate_ExpectFalse() -> None:
   assert ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=None ) is False


def Test_IsClosureActiveOnVisitDate_TestVisitDateInRange_ExpectTrue() -> None:
   assert ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=VISIT_DATE ) is True


def Test_IsClosureActiveOnVisitDate_TestVisitDateOutsideRange_ExpectFalse() -> None:
   assert ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=BEFORE_VISIT_DATE ) is False
   assert ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=AFTER_VISIT_DATE ) is False


def Test_ExhibitNamesClosedOnVisitDate_TestMixedRecords_ExpectActiveExhibitsOnly() -> None:
   closure_records = [
      ExhibitClosureRecord(
         exhibit=EXHIBIT_NAME,
         closed_start=CLOSURE_START_DATE,
         closed_end=CLOSURE_END_DATE ),
      ExhibitClosureRecord(
         exhibit='Eurasia Wilds',
         closed_start='2026-07-01',
         closed_end='2026-07-31' ),
   ]

   assert ExhibitStatusBuilder.exhibit_names_closed_on_visit_date(
      closure_records,
      VISIT_DATE ) == [ EXHIBIT_NAME ]
