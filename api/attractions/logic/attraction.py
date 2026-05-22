from ... import zoo
from ...shared.strings import SharedStrings
from ...shared.enums import ScheduleStatus
from .attraction_context import AttractionContext


def resolve_attraction_context( day, month, year ):
   target_date = zoo.ZooUtil.visit_target_date(
      month=month,
      day=day,
      year=year )
   weekday = target_date.weekday()
   is_weekend_or_holiday = (
      weekday >= 5
      or zoo.ZooUtil.is_holiday( d=target_date ) )

   return AttractionContext(
      normalized_month=target_date.month,
      normalized_day=target_date.day,
      target_date=target_date,
      weekday=weekday,
      is_weekend_or_holiday=is_weekend_or_holiday )


def calculate_attraction_likelihood( day_seasonal_availability_multiplier ):
   seasonal_multiplier = (
      day_seasonal_availability_multiplier
      if day_seasonal_availability_multiplier is not None
      else 1.0
   )
   likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

   return max( round( likelihood * 100 ), 0 )


def group_attraction_schedule_records_by_name( schedule_records ):
   schedule_records_by_attraction = {}

   for schedule_record in schedule_records:
      if schedule_record.attraction not in schedule_records_by_attraction:
         schedule_records_by_attraction[ schedule_record.attraction ] = []

      schedule_records_by_attraction[ schedule_record.attraction ].append( schedule_record )

   return schedule_records_by_attraction


def group_attraction_schedule_override_records_by_name( override_records ):
   override_records_by_attraction = {}

   for override_record in override_records:
      if override_record.attraction not in override_records_by_attraction:
         override_records_by_attraction[ override_record.attraction ] = []

      override_records_by_attraction[ override_record.attraction ].append( override_record )

   return override_records_by_attraction


def is_attraction_open_on_day( schedule_record, weekday, is_holiday ):
   weekday_values = [
      schedule_record.monday,
      schedule_record.tuesday,
      schedule_record.wednesday,
      schedule_record.thursday,
      schedule_record.friday,
      schedule_record.saturday,
      schedule_record.sunday,
   ]

   return (
      bool( weekday_values[ weekday ] )
      or ( schedule_record.holidays_only and is_holiday ) )


def build_closed_attraction_schedule_message( attraction_name, schedule_record ):
   if schedule_record.schedule_message:
      return schedule_record.schedule_message

   if schedule_record.saturday and schedule_record.sunday and schedule_record.holidays_only:
      return SharedStrings.Attractions.weekends_and_holidays_only( attraction_name )

   return SharedStrings.Attractions.not_scheduled_today( attraction_name )


def get_active_attraction_schedule_status(
      schedule_records,
      attraction_name,
      target_date,
      weekday ):

   if len( schedule_records ) == 0:
      return ScheduleStatus.UNKNOWN, None

   for schedule_record in schedule_records:
      is_active = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=schedule_record.schedule_start_date,
         end_date_value=schedule_record.schedule_end_date )

      if not is_active:
         continue

      is_holiday = zoo.ZooUtil.is_holiday( d=target_date )

      if is_attraction_open_on_day(
            schedule_record=schedule_record,
            weekday=weekday,
            is_holiday=is_holiday ):
         return ScheduleStatus.OPEN, None

      return ScheduleStatus.CLOSED, build_closed_attraction_schedule_message(
         attraction_name=attraction_name,
         schedule_record=schedule_record )

   return ScheduleStatus.UNKNOWN, None


def get_active_attraction_schedule_override_status(
      override_records,
      target_date ):

   for override_record in override_records:
      is_active = zoo.ZooUtil.is_date_in_range(
         target_date=target_date,
         start_date_value=override_record.override_start_date,
         end_date_value=override_record.override_end_date )

      if not is_active:
         continue

      if override_record.is_closed:
         return ScheduleStatus.CLOSED, override_record.override_message

      return ScheduleStatus.OPEN, None

   return ScheduleStatus.UNKNOWN, None


def get_attraction_day_seasonal_availability_multiplier(
      attraction_record,
      is_weekend_or_holiday ):

   if is_weekend_or_holiday:
      return attraction_record.weekend_holiday_multiplier

   return attraction_record.weekday_multiplier


def get_attraction_likelihood_and_message_for_date(
      attraction_record,
      schedule_records,
      schedule_override_records,
      target_date ):

   weekday = target_date.weekday()
   is_weekend_or_holiday = (
      weekday >= 5
      or zoo.ZooUtil.is_holiday( d=target_date ) )
   likelihood = 100
   closed_message = None

   override_status, override_message = get_active_attraction_schedule_override_status(
      override_records=[
         override_record
         for override_record in schedule_override_records
         if override_record.attraction == attraction_record.name
      ],
      target_date=target_date )

   if override_status == ScheduleStatus.CLOSED:
      return 0, override_message

   schedule_status, schedule_message = get_active_attraction_schedule_status(
      schedule_records=[
         schedule_record
         for schedule_record in schedule_records
         if schedule_record.attraction == attraction_record.name
      ],
      attraction_name=attraction_record.name,
      target_date=target_date,
      weekday=weekday )

   if schedule_status == ScheduleStatus.CLOSED:
      likelihood = 0
      closed_message = schedule_message
   elif schedule_status == ScheduleStatus.UNKNOWN:
      likelihood = calculate_attraction_likelihood(
         get_attraction_day_seasonal_availability_multiplier(
            attraction_record=attraction_record,
            is_weekend_or_holiday=is_weekend_or_holiday ) )

      if likelihood == 0:
         closed_message = SharedStrings.Attractions.likely_not_operating( attraction_record.name )

   return likelihood, closed_message


def build_attraction(
      attraction_record,
      schedule_records,
      schedule_override_records,
      context ):

   likelihood, closed_message = get_attraction_likelihood_and_message_for_date(
      attraction_record=attraction_record,
      schedule_records=schedule_records,
      schedule_override_records=schedule_override_records,
      target_date=context.target_date )

   return zoo.Attraction(
      name=attraction_record.name,
      free_with_admission=attraction_record.free_with_admission,
      description=attraction_record.description,
      info_link=attraction_record.info_link,
      hyperlink_text=attraction_record.hyperlink_text,
      x_coord=attraction_record.x_coord,
      y_coord=attraction_record.y_coord,
      is_closed=likelihood <= 0,
      closed_message=closed_message,
      likelihood=likelihood )


def build_attractions(
      attraction_records,
      schedule_records,
      schedule_override_records,
      context,
      include_closed_attractions=False ):

   schedule_records_by_name = group_attraction_schedule_records_by_name( schedule_records )
   schedule_override_records_by_name = group_attraction_schedule_override_records_by_name(
      schedule_override_records )
   attractions = []

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
