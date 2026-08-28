from __future__ import annotations

from datetime import date

from ..data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from ..data_access.attraction_provider import AttractionProvider
from ..data_access.attraction_schedule_provider import AttractionScheduleProvider
from ..domain.attraction_builder import AttractionBuilder
from ...itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..itinerary.itinerary_attractions_builder import ItineraryAttractionsBuilder
from ...models import Attraction
from ...request_connection_provider import RequestConnectionProvider
from ..scheduling.attraction_hours_schedule import AttractionHoursSchedule
from ..scheduling.attraction_hours_schedule_conflict_resolver import AttractionHoursScheduleConflictResolver
from ..scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from ..scheduling.attraction_hours_schedule_time_bounds_builder import AttractionHoursScheduleTimeBoundsBuilder
from ..scheduling.attraction_schedule_conflict_resolver import AttractionScheduleConflictResolver
from ..search.attractions_matching_query_builder import AttractionsMatchingQueryBuilder
from ...shared.amenity_coordinator_mutations import AmenityCoordinatorMutations
from ..status.attraction_hours_schedule_status_builder import AttractionHoursScheduleStatusBuilder
from ..status.attraction_status_builder import AttractionStatusBuilder
from ...types import Types


_mutations = AmenityCoordinatorMutations(
   build_closed_schedule=AttractionStatusBuilder.build_closed_schedule,
   build_opening_schedule=AttractionStatusBuilder.build_opening_schedule,
   build_closure_override=AttractionStatusBuilder.build_closure_override,
   save_opening_schedule=AttractionScheduleProvider.save_opening_schedule,
   save_schedule_override=AttractionScheduleProvider.save_schedule_override,
   save_replacing_overlaps=AttractionScheduleConflictResolver.save_replacing_overlaps,
   save_trimming_overlaps=AttractionScheduleConflictResolver.save_trimming_overlaps,
)


class AttractionCoordinator():
   @classmethod
   def get_attraction_names( cls ) -> list[ str ]:
      return AttractionProvider.fetch_attraction_names( RequestConnectionProvider.get() )


   @classmethod
   def get_attractions(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_attractions: bool = False ) -> list[ Attraction ]:

      context = AttractionBuilder.resolve_context(
         day=day,
         month=month,
         year=year )

      return AttractionBuilder.build_attractions(
         attraction_records=AttractionProvider.fetch_attraction_records(
            RequestConnectionProvider.get(),
            visit_date=context.target_date ),
         schedule_records=AttractionProvider.fetch_attraction_schedule_records(
            RequestConnectionProvider.get() ),
         schedule_override_records=AttractionProvider.fetch_attraction_schedule_override_records(
            RequestConnectionProvider.get() ),
         context=context,
         include_closed_attractions=include_closed_attractions )


   @classmethod
   def get_attractions_for_saved_itinerary(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         saved_attractions: list[ ItineraryAttractionRecord ] ) -> list[ Attraction ]:

      if not saved_attractions:
         return []

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=True )

      return ItineraryAttractionsBuilder.build(
         attractions,
         saved_attractions )


   @classmethod
   def get_attractions_matching_query(
         cls,
         query: str,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         include_closed_attractions: bool ) -> list[ Attraction ]:

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )

      return AttractionsMatchingQueryBuilder.build(
         attractions,
         query )


   @classmethod
   def get_attraction_likelihood_for_visit_date(
         cls,
         visit_date: date,
         attraction_name: str ) -> int | None:

      attraction_record = AttractionProvider.fetch_attraction_record_for_calendar_day(
         RequestConnectionProvider.get(),
         attraction_name=attraction_name,
         visit_date=visit_date )

      if attraction_record == None:
         return None

      likelihood, _ = AttractionBuilder.get_likelihood_and_message_for_date(
         attraction_record=attraction_record,
         schedule_records=AttractionProvider.fetch_attraction_schedule_records(
            RequestConnectionProvider.get() ),
         schedule_override_records=AttractionProvider.fetch_attraction_schedule_override_records(
            RequestConnectionProvider.get() ),
         target_date=visit_date )

      return likelihood


   @classmethod
   def set_attraction_as_closed(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_as_closed( attraction, start_date, end_date, message )


   @classmethod
   def set_attraction_closure_override(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( attraction, start_date, end_date, message )


   @classmethod
   def set_attraction_opening_schedule(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.set_opening_schedule(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   @classmethod
   def replace_attraction_opening_schedule_overlaps(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.replace_opening_schedule_overlaps(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   @classmethod
   def trim_attraction_opening_schedule_overlaps(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.trim_opening_schedule_overlaps(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   @classmethod
   def get_attraction_hours_schedule_time_bounds(
         cls,
         start_date: Types.DateInput = None,
         end_date: Types.DateInput = None ) -> AttractionHoursScheduleTimeBounds:
      return AttractionHoursScheduleTimeBoundsBuilder.fetch(
         RequestConnectionProvider.get(),
         start_date=start_date,
         end_date=end_date )


   @classmethod
   def _build_attraction_hours_schedule(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> AttractionHoursSchedule:
      schedule = AttractionHoursScheduleStatusBuilder.build_hours_schedule(
         attraction,
         start_date,
         end_date,
         weekday_start_time,
         weekday_end_time,
         weekend_holiday_start_time,
         weekend_holiday_end_time )
      bounds = AttractionHoursScheduleTimeBoundsBuilder.fetch(
         RequestConnectionProvider.get(),
         start_date=schedule.start_date,
         end_date=schedule.end_date )

      if not AttractionHoursScheduleTimeBoundsBuilder.times_are_within_bounds(
            bounds,
            weekday_start_time=schedule.weekday_start_time,
            weekday_end_time=schedule.weekday_end_time,
            weekend_holiday_start_time=schedule.weekend_holiday_start_time,
            weekend_holiday_end_time=schedule.weekend_holiday_end_time ):
         raise ValueError(
            'Attraction hours must fall within regular zoo hours for the '
            'selected date range.' )

      return schedule


   @classmethod
   def set_attraction_hours_schedule(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> bool:
      schedule = cls._build_attraction_hours_schedule(
         attraction,
         start_date,
         end_date,
         weekday_start_time,
         weekday_end_time,
         weekend_holiday_start_time,
         weekend_holiday_end_time )

      return AttractionHoursScheduleProvider.save_hours_schedule(
         RequestConnectionProvider.get(),
         schedule )


   @classmethod
   def replace_attraction_hours_schedule_overlaps(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> bool:
      schedule = cls._build_attraction_hours_schedule(
         attraction,
         start_date,
         end_date,
         weekday_start_time,
         weekday_end_time,
         weekend_holiday_start_time,
         weekend_holiday_end_time )

      return AttractionHoursScheduleConflictResolver.save_replacing_overlaps(
         RequestConnectionProvider.get(),
         schedule )


   @classmethod
   def trim_attraction_hours_schedule_overlaps(
         cls,
         attraction: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         weekday_start_time: Types.TimeInput,
         weekday_end_time: Types.TimeInput,
         weekend_holiday_start_time: Types.TimeInput,
         weekend_holiday_end_time: Types.TimeInput ) -> bool:
      schedule = cls._build_attraction_hours_schedule(
         attraction,
         start_date,
         end_date,
         weekday_start_time,
         weekday_end_time,
         weekend_holiday_start_time,
         weekend_holiday_end_time )

      return AttractionHoursScheduleConflictResolver.save_trimming_overlaps(
         RequestConnectionProvider.get(),
         schedule )
