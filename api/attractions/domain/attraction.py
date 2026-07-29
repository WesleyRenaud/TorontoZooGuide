from __future__ import annotations

from datetime import date

from .attraction_context import AttractionContext
from ..data_access.attraction_record import AttractionRecord
from ..data_access.attraction_schedule_override_record import AttractionScheduleOverrideRecord
from ..data_access.attraction_schedule_record import AttractionScheduleRecord
from ...models import Attraction
from ...shared.calendar_dates import CalendarDates
from ...shared.enums import ScheduleStatus
from ...shared.opening_schedule_seasonal_multiplier import get_day_seasonal_availability_multiplier
from ...shared.opening_schedule_status import calculate_seasonal_likelihood
from ...shared.opening_schedule_status import get_active_opening_schedule_status
from ...shared.opening_schedule_status import get_active_schedule_override_status
from ...shared.opening_schedule_status import group_records_by_name
from ...shared.opening_schedule_status import is_open_on_weekday
from ...shared.opening_schedule_status import resolve_amenity_likelihood_and_message
from ...shared.opening_schedule_visit_context import resolve_opening_schedule_visit_context
from ...shared.strings import SharedStrings
from ...types import MonthInput, SeasonalMultiplier, VisitDay, VisitYear


def resolve_attraction_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear ) -> AttractionContext:
   return resolve_opening_schedule_visit_context(
      day=day,
      month=month,
      year=year )


def calculate_attraction_likelihood(
      day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
   return calculate_seasonal_likelihood( day_seasonal_availability_multiplier )


def group_attraction_schedule_records_by_name(
      schedule_records: list[ AttractionScheduleRecord ] ) -> dict[ str, list[ AttractionScheduleRecord ] ]:
   return group_records_by_name( schedule_records, lambda record: record.attraction )


def group_attraction_schedule_override_records_by_name(
      override_records: list[ AttractionScheduleOverrideRecord ] ) -> dict[ str, list[ AttractionScheduleOverrideRecord ] ]:
   return group_records_by_name( override_records, lambda record: record.attraction )


def is_attraction_open_on_day(
      schedule_record: AttractionScheduleRecord,
      weekday: int,
      is_holiday: bool ) -> bool:
   return is_open_on_weekday(
      schedule_record=schedule_record,
      weekday=weekday,
      is_holiday=is_holiday )


def build_closed_attraction_schedule_message(
      attraction_name: str,
      schedule_record: AttractionScheduleRecord ) -> str:
   if schedule_record.schedule_message:
      return schedule_record.schedule_message

   if schedule_record.saturday and schedule_record.sunday and schedule_record.holidays_only:
      return SharedStrings.Attractions.weekends_and_holidays_only( attraction_name )

   return SharedStrings.Attractions.not_scheduled_today( attraction_name )


def get_active_attraction_schedule_status(
      schedule_records: list[ AttractionScheduleRecord ],
      attraction_name: str,
      target_date: date,
      weekday: int ) -> tuple[ ScheduleStatus, str | None ]:
   return get_active_opening_schedule_status(
      schedule_records=schedule_records,
      target_date=target_date,
      weekday=weekday,
      build_closed_message=lambda schedule_record: build_closed_attraction_schedule_message(
         attraction_name=attraction_name,
         schedule_record=schedule_record ) )


def get_active_attraction_schedule_override_status(
      override_records: list[ AttractionScheduleOverrideRecord ],
      target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
   return get_active_schedule_override_status(
      override_records=override_records,
      target_date=target_date )


def get_attraction_day_seasonal_availability_multiplier(
      attraction_record: AttractionRecord,
      is_weekend_or_holiday: bool ) -> SeasonalMultiplier:
   return get_day_seasonal_availability_multiplier(
      weekday_multiplier=attraction_record.weekday_multiplier,
      weekend_holiday_multiplier=attraction_record.weekend_holiday_multiplier,
      is_weekend_or_holiday=is_weekend_or_holiday )


def get_attraction_likelihood_and_message_for_date(
      attraction_record: AttractionRecord,
      schedule_records: list[ AttractionScheduleRecord ],
      schedule_override_records: list[ AttractionScheduleOverrideRecord ],
      target_date: date ) -> tuple[ int, str | None ]:

   return resolve_amenity_likelihood_and_message(
      name=attraction_record.name,
      schedule_records=[
         schedule_record
         for schedule_record in schedule_records
         if schedule_record.attraction == attraction_record.name
      ],
      override_records=[
         override_record
         for override_record in schedule_override_records
         if override_record.attraction == attraction_record.name
      ],
      target_date=target_date,
      weekday=target_date.weekday(),
      seasonal_multiplier=get_attraction_day_seasonal_availability_multiplier(
         attraction_record=attraction_record,
         is_weekend_or_holiday=CalendarDates.is_weekend_or_holiday(
            d=target_date ) ),
      build_closed_schedule_message=lambda schedule_record: build_closed_attraction_schedule_message(
         attraction_name=attraction_record.name,
         schedule_record=schedule_record ),
      likely_closed_message=SharedStrings.Attractions.likely_not_operating )


def build_attraction(
      attraction_record: AttractionRecord,
      schedule_records: list[ AttractionScheduleRecord ],
      schedule_override_records: list[ AttractionScheduleOverrideRecord ],
      context: AttractionContext ) -> Attraction:

   likelihood, closed_message = get_attraction_likelihood_and_message_for_date(
      attraction_record=attraction_record,
      schedule_records=schedule_records,
      schedule_override_records=schedule_override_records,
      target_date=context.target_date )

   return Attraction(
      name=attraction_record.name,
      free_with_admission=attraction_record.free_with_admission,
      description=attraction_record.description,
      info_link=attraction_record.info_link,
      hyperlink_text=attraction_record.hyperlink_text,
      x_coord=attraction_record.x_coord,
      y_coord=attraction_record.y_coord,
      region=attraction_record.region,
      is_closed=likelihood <= 0,
      closed_message=closed_message,
      likelihood=likelihood )


def build_attractions(
      attraction_records: list[ AttractionRecord ],
      schedule_records: list[ AttractionScheduleRecord ],
      schedule_override_records: list[ AttractionScheduleOverrideRecord ],
      context: AttractionContext,
      include_closed_attractions: bool = False ) -> list[ Attraction ]:

   schedule_records_by_name = group_attraction_schedule_records_by_name( schedule_records )
   schedule_override_records_by_name = group_attraction_schedule_override_records_by_name(
      schedule_override_records )
   attractions: list[ Attraction ] = []

   for attraction_record in attraction_records:
      attraction = build_attraction(
         attraction_record=attraction_record,
         schedule_records=schedule_records_by_name.get( attraction_record.name, [] ),
         schedule_override_records=schedule_override_records_by_name.get(
            attraction_record.name,
            [] ),
         context=context )

      if attraction.is_closed and not include_closed_attractions:
         continue

      attractions.append( attraction )

   return attractions
