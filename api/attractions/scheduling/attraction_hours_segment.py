from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .attraction_hours_coverage import AttractionHoursCoverage
from .attraction_hours_span import AttractionHoursSpan
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


@dataclass( frozen=True )
class AttractionHoursSegment:
   records: list[ ZooHoursRecord ]
   christmas: date | None


   @classmethod
   def split_on_christmas(
         cls,
         records: list[ ZooHoursRecord ] ) -> list[ AttractionHoursSegment ]:
      segments: list[ AttractionHoursSegment ] = []
      start = 0

      for index, record in enumerate( records ):
         day = DateValues.parse_date_value( record.operating_date )

         if day is None or not CalendarDates.is_christmas( day ):
            continue

         segments.append( cls( records=records[ start:index ], christmas=day ) )
         start = index + 1

      segments.append( cls( records=records[ start: ], christmas=None ) )
      return segments


   def fitted_span(
         self,
         start: date,
         season_end: date | None,
         coverage: AttractionHoursCoverage ) -> AttractionHoursSpan | None:
      if coverage.stops_fitting_on is not None:
         end = CalendarDates.one_day_earlier( coverage.stops_fitting_on )
      elif self.christmas is not None:
         end = CalendarDates.one_day_earlier( self.christmas )
      else:
         end = season_end

      if coverage.stops_fitting_on is None and not coverage.both_day_kinds:
         return None

      if end is not None and start > end:
         return None

      return AttractionHoursSpan( start=start, end=end )
