from __future__ import annotations

from datetime import date

from api.app_string_provider import AppStringProvider
from api.exhibits.data_access.exhibit_closure_record import ExhibitClosureRecord
from api.exhibits.status.exhibit_status_builder import ExhibitStatusBuilder


EXHIBIT_NAME = 'Africa Savanna'
CUSTOM_CLOSED_MESSAGE = 'Closed for maintenance.'
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

   assert status.message == AppStringProvider.format(
      'guestStatus.locations.temporarilyClosed',
      name=EXHIBIT_NAME )


def Test_IsClosureActiveOnVisitDate_TestInactiveClosure_ExpectFalse() -> None:
   is_closed = False

   active = ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=is_closed,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=VISIT_DATE )

   assert active is False


def Test_IsClosureActiveOnVisitDate_TestMissingVisitDate_ExpectFalse() -> None:
   target_date = None

   active = ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=target_date )

   assert active is False


def Test_IsClosureActiveOnVisitDate_TestVisitDateInRange_ExpectTrue() -> None:
   active = ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=VISIT_DATE )

   assert active is True


def Test_IsClosureActiveOnVisitDate_TestVisitDateBeforeRange_ExpectFalse() -> None:
   active = ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=BEFORE_VISIT_DATE )

   assert active is False


def Test_IsClosureActiveOnVisitDate_TestVisitDateAfterRange_ExpectFalse() -> None:
   active = ExhibitStatusBuilder.is_closure_active_on_visit_date(
      is_closed=True,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE,
      target_date=AFTER_VISIT_DATE )

   assert active is False


def Test_ExhibitNamesClosedOnVisitDate_TestMixedRecords_ExpectActiveExhibitsOnly() -> None:
   savanna_closure = ExhibitClosureRecord(
      exhibit=EXHIBIT_NAME,
      closed_start=CLOSURE_START_DATE,
      closed_end=CLOSURE_END_DATE )
   eurasia_closure = ExhibitClosureRecord(
      exhibit='Eurasia Wilds',
      closed_start='2026-07-01',
      closed_end='2026-07-31' )
   closure_records = [ savanna_closure, eurasia_closure ]

   closed_exhibits = ExhibitStatusBuilder.exhibit_names_closed_on_visit_date(
      closure_records,
      VISIT_DATE )

   assert closed_exhibits == [ savanna_closure.exhibit ]
