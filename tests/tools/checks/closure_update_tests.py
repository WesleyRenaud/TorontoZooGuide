from __future__ import annotations

from datetime import date

from api.models.update import Update
from api.updates.domain.update_type import UpdateType
from tools.checks.closure_update import ClosureUpdate
from tools.checks.closure_update_builder import ClosureUpdateBuilder
from tools.checks.website_closure import WebsiteClosure


TODAY = date( 2026, 11, 11 )
HORIZON = date( 2026, 12, 11 )


def notice( title: str, description: str = '' ) -> WebsiteClosure:
   return WebsiteClosure( title, description )


def stored(
      title: str,
      description: str = '',
      update_type: str = UpdateType.CLOSURE.value,
      start: str = '2026-05-03',
      end: str | None = None ) -> Update:
   return Update( title, description, update_type, start, end )


def dates( updates: list[ ClosureUpdate ] ) -> list[ tuple[ str, date, date ] ]:
   return [
      ( update.title, update.start, update.end )
      for update in updates
   ]


def Test_Build_TestNewNotice_ExpectMonthLongAddition() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'Polar bear viewing is closed.' ) ],
      [],
      TODAY,
   )

   assert dates( plan.added ) == [
      ( 'Polar bear viewing is closed.', TODAY, HORIZON ),
   ]
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestSoonerEnd_ExpectExtension() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'Pathway is closed.', 'Detour.' ) ],
      [ stored( 'Pathway is closed.', 'Detour.', end='2026-11-20' ) ],
      TODAY,
   )

   assert dates( plan.extended ) == [
      ( 'Pathway is closed.', date( 2026, 5, 3 ), HORIZON ),
   ]
   assert 'Extended the update through December 11, 2026.' in plan.extended[ 0 ].extended_line()
   assert plan.added == []
   assert plan.ended == []


def Test_Build_TestLaterEnd_ExpectNoChange() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'Pathway is closed.' ) ],
      [ stored( 'Pathway is closed.', end='2027-06-01' ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestOpenEnd_ExpectNoChange() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'Pathway is closed.' ) ],
      [ stored( 'Pathway is closed.' ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestBirth_ExpectBirthStays() -> None:
   plan = ClosureUpdateBuilder.build(
      [],
      [ stored( 'New Baby Camel!', 'Born.', UpdateType.ANIMAL_BIRTH.value ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestMissingOnWebsite_ExpectEnd() -> None:
   plan = ClosureUpdateBuilder.build(
      [],
      [ stored( 'Old closure', 'The shop is closed.', end='2026-12-01' ) ],
      TODAY,
   )

   assert dates( plan.ended ) == [
      ( 'Old closure', date( 2026, 5, 3 ), date( 2026, 11, 10 ) ),
   ]
   assert plan.added == []
   assert plan.extended == []


def Test_Build_TestClosedOnANamedDay_ExpectEndOnThatDay() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'The VR station is closed for today, Sunday, November 15.' ) ],
      [],
      TODAY,
   )

   assert dates( plan.added ) == [
      (
         'The VR station is closed for today, Sunday, November 15.',
         TODAY,
         date( 2026, 11, 15 ),
      ),
   ]
   assert plan.extended == []
   assert plan.trimmed == []


def Test_Build_TestClosedToday_ExpectEndToday() -> None:
   plan = ClosureUpdateBuilder.build(
      [ notice( 'The VR station is closed today.' ) ],
      [],
      TODAY,
   )

   assert dates( plan.added ) == [
      ( 'The VR station is closed today.', TODAY, TODAY ),
   ]


def Test_Build_TestDateRange_ExpectEndOnTheLastDay() -> None:
   day = date( 2026, 6, 1 )
   plan = ClosureUpdateBuilder.build(
      [ notice( 'TundraAir Ride Closure June 2nd-4th.' ) ],
      [],
      day,
   )

   assert dates( plan.added ) == [
      ( 'TundraAir Ride Closure June 2nd-4th.', day, date( 2026, 6, 4 ) ),
   ]


def Test_Build_TestMidMonthRange_ExpectLaterOfMidpointAndOneWeek() -> None:
   title = 'Monday, November 30 - Mid-December (Subject to Change)'
   start = date( 2026, 11, 25 )
   first = ClosureUpdateBuilder.build(
      [ notice( title ) ],
      [ stored( title, start='2026-11-25', end='2026-11-30' ) ],
      date( 2026, 12, 3 ),
   )
   second = ClosureUpdateBuilder.build(
      [ notice( title ) ],
      [ stored( title, start='2026-11-25', end='2026-12-15' ) ],
      date( 2026, 12, 10 ),
   )

   assert dates( first.extended ) == [ ( title, start, date( 2026, 12, 15 ) ) ]
   assert dates( second.extended ) == [ ( title, start, date( 2026, 12, 17 ) ) ]


def Test_Build_TestMonthEndOnANamedDay_ExpectTrimmed() -> None:
   title = 'The VR station is closed for today, Sunday, November 15.'
   plan = ClosureUpdateBuilder.build(
      [ notice( title ) ],
      [ stored( title, start='2026-11-15', end='2026-12-15' ) ],
      TODAY,
   )

   assert dates( plan.trimmed ) == [
      ( title, date( 2026, 11, 15 ), date( 2026, 11, 15 ) ),
   ]
   assert plan.added == []
   assert plan.extended == []


def Test_AddedLine_TestDescription_ExpectNoticeText() -> None:
   update = ClosureUpdate(
      'Tuesday, November 17',
      'The Indo-Malaya Pavilion will open late.',
      date( 2026, 11, 17 ),
      date( 2026, 11, 17 ),
   )
   line = update.added_line()

   assert 'Tuesday, November 17' in line
   assert 'The Indo-Malaya Pavilion will open late.' in line
   assert 'Set the update for November 17, 2026.' in line
   assert 'through' not in line


def Test_ExtendedLine_TestDescription_ExpectTitleAndEnd() -> None:
   update = ClosureUpdate(
      'Eurasia Wilds Loop Pathway Closure',
      'A portion of the pathway is closed.',
      date( 2026, 5, 3 ),
      date( 2026, 12, 17 ),
   )
   line = update.extended_line()

   assert line.startswith( 'Eurasia Wilds Loop Pathway Closure' )
   assert 'A portion of the pathway is closed.' not in line
   assert 'Extended the update through December 17, 2026.' in line


def Test_AddedLine_TestSeveralDays_ExpectThrough() -> None:
   update = ClosureUpdate(
      'TundraAir Ride Closure',
      'Closed June 2nd-4th.',
      date( 2026, 6, 2 ),
      date( 2026, 6, 4 ),
   )
   line = update.added_line()

   assert 'Set the update from June 2, 2026 through June 4, 2026.' in line

