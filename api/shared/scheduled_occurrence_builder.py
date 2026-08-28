from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from typing import Any

from .calendar_dates import CalendarDates
from .date_values import DateValues
from ..models import ScheduledOccurrence
from .scheduled_occurrence_sorter import ScheduledOccurrenceSorter


class ScheduledOccurrenceBuilder():
   @classmethod
   def build(
         cls,
         schedule_records: list[ Any ],
         *,
         days_ahead: int,
         get_time: Callable[ [ Any ], str | None ],
         get_weekday_flags: Callable[ [ Any ], tuple[ bool, bool, bool, bool, bool, bool, bool ] ],
         is_cancelled: Callable[ [ str, str ], bool ],
         extra_occurrences: list[ ScheduledOccurrence ] | None = None ) -> list[ ScheduledOccurrence ]:
      today = DateValues.parse_date_value( DateValues.today_date_key() )
      schedule_start_date = today
      schedule_end_date = today + timedelta( days=days_ahead )
      occurrences: list[ ScheduledOccurrence ] = []

      for schedule_record in schedule_records:
         parsed_start_date = DateValues.parse_date_value(
            value=schedule_record.schedule_start_date )
         slot_start_date = (
            parsed_start_date
            if parsed_start_date > schedule_start_date
            else schedule_start_date )
         slot_end_date = schedule_end_date

         if schedule_record.schedule_end_date != None:
            parsed_end_date = DateValues.parse_date_value(
               value=schedule_record.schedule_end_date )

            if parsed_end_date < slot_end_date:
               slot_end_date = parsed_end_date

         if slot_end_date < slot_start_date:
            continue

         occurrence_time = get_time( schedule_record )
         weekday_flags = get_weekday_flags( schedule_record )
         current_date = slot_start_date

         while current_date <= slot_end_date:
            current_date_key = current_date.isoformat()

            if (
                  occurrence_time
                  and CalendarDates.schedule_includes_weekday(
                     current_date.weekday(),
                     weekday_flags )
                  and not is_cancelled( current_date_key, occurrence_time ) ):
               occurrences.append(
                  ScheduledOccurrence(
                     date=current_date_key,
                     time=occurrence_time ) )

            current_date += timedelta( days=1 )

      if extra_occurrences:
         occurrences.extend( extra_occurrences )

      return ScheduledOccurrenceSorter.unique_sorted_by_key(
         occurrences,
         key=lambda occurrence: ( occurrence.date, occurrence.time ),
         sort_key=lambda occurrence: (
            occurrence.date,
            occurrence.time or '',
         ) )
