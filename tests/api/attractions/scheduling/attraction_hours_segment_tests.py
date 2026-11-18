from __future__ import annotations

from datetime import date

from api.attractions.scheduling.attraction_hours_coverage import AttractionHoursCoverage
from api.attractions.scheduling.attraction_hours_segment import AttractionHoursSegment


def Test_FittedSpan_TestOneDayKind_ExpectNone() -> None:
   segment = AttractionHoursSegment( records=[], christmas=None )
   coverage = AttractionHoursCoverage( stops_fitting_on=None, both_day_kinds=False )

   fitted = segment.fitted_span( date( 2026, 11, 16 ), date( 2026, 12, 31 ), coverage )

   assert fitted is None


def Test_FittedSpan_TestStartAfterEnd_ExpectNone() -> None:
   segment = AttractionHoursSegment( records=[], christmas=None )
   coverage = AttractionHoursCoverage( stops_fitting_on=None, both_day_kinds=True )

   fitted = segment.fitted_span( date( 2026, 12, 26 ), date( 2026, 12, 24 ), coverage )

   assert fitted is None
