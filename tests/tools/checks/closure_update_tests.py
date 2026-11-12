from __future__ import annotations

from datetime import date

from api.models.update import Update
from api.updates.domain.update_type import UpdateType
from tools.checks.closure_update import ClosureUpdate
from tools.checks.closure_update_plan import ClosureUpdatePlan
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
   plan = ClosureUpdatePlan.build(
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
   plan = ClosureUpdatePlan.build(
      [ notice( 'Pathway is closed.', 'Detour.' ) ],
      [ stored( 'Pathway is closed.', 'Detour.', end='2026-11-20' ) ],
      TODAY,
   )

   assert dates( plan.extended ) == [
      ( 'Pathway is closed.', date( 2026, 5, 3 ), HORIZON ),
   ]
   assert plan.added == []
   assert plan.ended == []


def Test_Build_TestLaterEnd_ExpectNoChange() -> None:
   plan = ClosureUpdatePlan.build(
      [ notice( 'Pathway is closed.' ) ],
      [ stored( 'Pathway is closed.', end='2027-06-01' ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestOpenEnd_ExpectNoChange() -> None:
   plan = ClosureUpdatePlan.build(
      [ notice( 'Pathway is closed.' ) ],
      [ stored( 'Pathway is closed.' ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestBirth_ExpectBirthStays() -> None:
   plan = ClosureUpdatePlan.build(
      [],
      [ stored( 'New Baby Camel!', 'Born.', UpdateType.ANIMAL_BIRTH.value ) ],
      TODAY,
   )

   assert plan.count() == 0


def Test_Build_TestMissingOnWebsite_ExpectEnd() -> None:
   plan = ClosureUpdatePlan.build(
      [],
      [ stored( 'Old closure', 'The shop is closed.', end='2026-12-01' ) ],
      TODAY,
   )

   assert dates( plan.ended ) == [
      ( 'Old closure', date( 2026, 5, 3 ), TODAY ),
   ]
   assert plan.added == []
   assert plan.extended == []
