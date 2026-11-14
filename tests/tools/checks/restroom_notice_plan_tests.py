from __future__ import annotations

from datetime import date

from api.restrooms.data_access.restroom_record import RestroomRecord
from tools.checks.restroom_notice import RestroomNotice
from tools.checks.restroom_notice_plan import RestroomNoticePlan


TODAY = date( 2026, 11, 14 )


def record(
      title: str,
      is_closed: int | None = None,
      message: str | None = None,
      start: str | None = None,
      end: str | None = None,
      alert: str | None = None,
      alert_start: str | None = None,
      alert_end: str | None = None ) -> RestroomRecord:
   return RestroomRecord(
      title,
      0,
      0,
      is_closed,
      message,
      start,
      end,
      alert,
      alert_start,
      alert_end,
   )


def Test_Build_TestNewNotice_ExpectMonthLongClosure() -> None:
   plan = RestroomNoticePlan.build(
      [ RestroomNotice( 'Eurasia Restroom', 'The Eurasia washrooms are closed.', True ) ],
      [],
      TODAY,
   )

   assert [ ( change.restroom, change.start, change.end ) for change in plan.added ] == [
      ( 'Eurasia Restroom', TODAY, date( 2026, 12, 14 ) ),
   ]
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestMissingNotice_ExpectEndedToday() -> None:
   plan = RestroomNoticePlan.build(
      [],
      [ record( 'Eurasia Restroom', 1, 'The Eurasia washrooms are closed.', '2026-11-01', '2026-12-01' ) ],
      TODAY,
   )

   assert [ ( change.restroom, change.start, change.end, change.closure ) for change in plan.ended ] == [
      ( 'Eurasia Restroom', date( 2026, 11, 1 ), TODAY, True ),
   ]
   assert plan.added == []


def Test_Build_TestSameWording_ExpectExtendedToTheMonth() -> None:
   message = 'The Eurasia washrooms are closed.'
   plan = RestroomNoticePlan.build(
      [ RestroomNotice( 'Eurasia Restroom', message, True ) ],
      [ record( 'Eurasia Restroom', 1, message, '2026-11-01', '2026-11-20' ) ],
      TODAY,
   )

   assert [ ( change.start, change.end ) for change in plan.extended ] == [
      ( date( 2026, 11, 1 ), date( 2026, 12, 14 ) ),
   ]
   assert plan.added == []
   assert plan.ended == []


def Test_Build_TestLongerEnd_ExpectLeftAlone() -> None:
   message = 'The Eurasia washrooms are closed.'
   plan = RestroomNoticePlan.build(
      [ RestroomNotice( 'Eurasia Restroom', message, True ) ],
      [ record( 'Eurasia Restroom', 1, message, '2026-05-01', '2027-06-01' ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestDifferentWording_ExpectReplacement() -> None:
   plan = RestroomNoticePlan.build(
      [ RestroomNotice( 'Eurasia Restroom', 'New wording.', True ) ],
      [ record( 'Eurasia Restroom', 1, 'Old wording.', '2026-11-01', '2026-12-01' ) ],
      TODAY,
   )

   assert [ change.message for change in plan.added ] == [ 'New wording.' ]
   assert [ change.message for change in plan.ended ] == [ 'Old wording.' ]
   assert plan.extended == []


def Test_Build_TestOpenRowAndPastAlert_ExpectIgnored() -> None:
   plan = RestroomNoticePlan.build(
      [],
      [
         record( 'Entrance Restroom', 0, None, '2026-04-26', None ),
         record(
            'Zootique Restroom',
            alert='The washroom will open late.',
            alert_start='2026-06-01',
            alert_end='2026-06-01',
         ),
      ],
      TODAY,
   )

   assert plan.count() == 0
