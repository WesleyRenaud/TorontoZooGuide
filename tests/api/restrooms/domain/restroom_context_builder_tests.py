from __future__ import annotations

from datetime import date

from api.restrooms.domain.restroom_context_builder import RestroomContextBuilder


VISIT_DAY = 15
VISIT_MONTH = 6
VISIT_YEAR = 2026


def Test_Resolve_TestVisitDate_ExpectRestroomContext() -> None:
   context = RestroomContextBuilder.resolve(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert context.target_date == date( VISIT_YEAR, VISIT_MONTH, VISIT_DAY )
