from __future__ import annotations

from datetime import date

from ...app_strings import format_app_string
from .attraction_context import AttractionContext
from ..data_access.attraction_record import AttractionRecord
from ..data_access.attraction_schedule_override_record import AttractionScheduleOverrideRecord
from ..data_access.attraction_schedule_record import AttractionScheduleRecord
from ...models import Attraction
from ...shared.calendar_dates import CalendarDates
from ...shared.enums import ScheduleStatus
from ...shared.opening_schedule_seasonal_multiplier_resolver import OpeningScheduleSeasonalMultiplierResolver
from ...shared.opening_schedule_status_resolver import OpeningScheduleStatusResolver
from ...shared.opening_schedule_visit_context_resolver import OpeningScheduleVisitContextResolver
from ...types import MonthInput, SeasonalMultiplier, VisitDay, VisitYear


class AttractionBuilder():
   @classmethod
   def resolve_context(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> AttractionContext:
      return OpeningScheduleVisitContextResolver.resolve( day=day, month=month, year=year )


   @classmethod
   def calculate_likelihood(
         cls,
         day_seasonal_availability_multiplier: SeasonalMultiplier ) -> int:
      return OpeningScheduleStatusResolver.calculate_seasonal_likelihood( day_seasonal_availability_multiplier )


   @classmethod
   def group_schedule_records_by_name(
         cls,
         schedule_records: list[ AttractionScheduleRecord ] ) -> dict[ str, list[ AttractionScheduleRecord ] ]:
      return OpeningScheduleStatusResolver.group_records_by_name( schedule_records, lambda record: record.attraction )


   @classmethod
   def group_schedule_override_records_by_name(
         cls,
         override_records: list[ AttractionScheduleOverrideRecord ] ) -> dict[ str, list[ AttractionScheduleOverrideRecord ] ]:
      return OpeningScheduleStatusResolver.group_records_by_name( override_records, lambda record: record.attraction )


   @classmethod
   def is_open_on_day(
         cls,
         schedule_record: AttractionScheduleRecord,
         weekday: int,
         is_holiday: bool ) -> bool:
      return OpeningScheduleStatusResolver.is_open_on_weekday(
         schedule_record=schedule_record,
         weekday=weekday,
         is_holiday=is_holiday )


   @classmethod
   def build_closed_schedule_message(
         cls,
         attraction_name: str,
         schedule_record: AttractionScheduleRecord ) -> str:
      if schedule_record.schedule_message:
         return schedule_record.schedule_message
      if schedule_record.saturday and schedule_record.sunday and schedule_record.holidays_only:
         return format_app_string(
            'guestStatus.attractions.weekendsAndHolidaysOnly',
            attractionName=attraction_name )
      return format_app_string(
         'guestStatus.attractions.notScheduledToday',
         attractionName=attraction_name )


   @classmethod
   def get_active_schedule_status(
         cls,
         schedule_records: list[ AttractionScheduleRecord ],
         attraction_name: str,
         target_date: date,
         weekday: int ) -> tuple[ ScheduleStatus, str | None ]:
      return OpeningScheduleStatusResolver.get_active_opening_schedule_status(
         schedule_records=schedule_records,
         target_date=target_date,
         weekday=weekday,
         build_closed_message=lambda schedule_record: cls.build_closed_schedule_message(
            attraction_name=attraction_name,
            schedule_record=schedule_record ) )


   @classmethod
   def get_active_schedule_override_status(
         cls,
         override_records: list[ AttractionScheduleOverrideRecord ],
         target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
      return OpeningScheduleStatusResolver.get_active_schedule_override_status(
         override_records=override_records,
         target_date=target_date )


   @classmethod
   def get_day_seasonal_availability_multiplier(
         cls,
         attraction_record: AttractionRecord,
         is_weekend_or_holiday: bool ) -> SeasonalMultiplier:
      return OpeningScheduleSeasonalMultiplierResolver.resolve(
         weekday_multiplier=attraction_record.weekday_multiplier,
         weekend_holiday_multiplier=attraction_record.weekend_holiday_multiplier,
         is_weekend_or_holiday=is_weekend_or_holiday )


   @classmethod
   def get_likelihood_and_message_for_date(
         cls,
         attraction_record: AttractionRecord,
         schedule_records: list[ AttractionScheduleRecord ],
         schedule_override_records: list[ AttractionScheduleOverrideRecord ],
         target_date: date ) -> tuple[ int, str | None ]:
      return OpeningScheduleStatusResolver.resolve_amenity_likelihood_and_message(
         name=attraction_record.name,
         schedule_records=[
            record for record in schedule_records
            if record.attraction == attraction_record.name
         ],
         override_records=[
            record for record in schedule_override_records
            if record.attraction == attraction_record.name
         ],
         target_date=target_date,
         weekday=target_date.weekday(),
         seasonal_multiplier=cls.get_day_seasonal_availability_multiplier(
            attraction_record=attraction_record,
            is_weekend_or_holiday=CalendarDates.is_weekend_or_holiday( d=target_date ) ),
         build_closed_schedule_message=lambda schedule_record: cls.build_closed_schedule_message(
            attraction_name=attraction_record.name,
            schedule_record=schedule_record ),
         likely_closed_message=lambda name: format_app_string(
            'guestStatus.attractions.likelyNotOperating',
            attractionName=name ) )


   @classmethod
   def build_attraction(
         cls,
         attraction_record: AttractionRecord,
         schedule_records: list[ AttractionScheduleRecord ],
         schedule_override_records: list[ AttractionScheduleOverrideRecord ],
         context: AttractionContext ) -> Attraction:
      likelihood, closed_message = cls.get_likelihood_and_message_for_date(
         attraction_record=attraction_record,
         schedule_records=schedule_records,
         schedule_override_records=schedule_override_records,
         target_date=context.target_date )
      if context.is_weekend_or_holiday:
         open_time = attraction_record.weekend_holiday_start_time
         close_time = attraction_record.weekend_holiday_end_time
      else:
         open_time = attraction_record.weekday_start_time
         close_time = attraction_record.weekday_end_time
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
         likelihood=likelihood,
         open_time=open_time,
         close_time=close_time,
         is_also_transportation=attraction_record.is_also_transportation )


   @classmethod
   def build_attractions(
         cls,
         attraction_records: list[ AttractionRecord ],
         schedule_records: list[ AttractionScheduleRecord ],
         schedule_override_records: list[ AttractionScheduleOverrideRecord ],
         context: AttractionContext,
         include_closed_attractions: bool = False ) -> list[ Attraction ]:
      schedule_records_by_name = cls.group_schedule_records_by_name( schedule_records )
      override_records_by_name = cls.group_schedule_override_records_by_name(
         schedule_override_records )
      attractions: list[ Attraction ] = []
      for attraction_record in attraction_records:
         attraction = cls.build_attraction(
            attraction_record=attraction_record,
            schedule_records=schedule_records_by_name.get( attraction_record.name, [] ),
            schedule_override_records=override_records_by_name.get(
               attraction_record.name,
               [] ),
            context=context )
         if attraction.is_closed and not include_closed_attractions:
            continue
         attractions.append( attraction )
      return attractions
