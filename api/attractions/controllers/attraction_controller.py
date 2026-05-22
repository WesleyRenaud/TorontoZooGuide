from ..data_access.attraction import fetch_attraction_record_for_calendar_day
from ..data_access.attraction import fetch_attraction_names
from ..data_access.attraction import fetch_attraction_records
from ..data_access.attraction import fetch_attraction_schedule_override_records
from ..data_access.attraction import fetch_attraction_schedule_records
from ..data_access.attraction_schedule import save_attraction_opening_schedule
from ..data_access.attraction_schedule import save_attraction_schedule_override
from ..logic.attraction import build_attractions
from ..logic.attraction import get_attraction_likelihood_and_message_for_date
from ..logic.attraction import resolve_attraction_context
from ..logic.attraction_status import build_attraction_closed_schedule
from ..logic.attraction_status import build_attraction_closure_override
from ..logic.attraction_status import build_attraction_opening_schedule
from ..logic.attractions_matching_query import build_attractions_matching_query
from ..logic.itinerary_attractions import build_itinerary_attractions
from ...request_connection import get_connection


class AttractionController():


   @classmethod
   def get_attraction_names( cls ):
      return fetch_attraction_names( get_connection() )


   @classmethod
   def get_attractions(
         cls,
         day,
         month,
         year,
         include_closed_attractions=False ):

      context = resolve_attraction_context(
         day=day,
         month=month,
         year=year )

      return build_attractions(
         attraction_records=fetch_attraction_records(
            get_connection(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_attraction_schedule_records( get_connection() ),
         schedule_override_records=fetch_attraction_schedule_override_records(
            get_connection() ),
         context=context,
         include_closed_attractions=include_closed_attractions )


   @classmethod
   def get_attractions_for_saved_itinerary(
         cls,
         day,
         month,
         year,
         saved_attractions ):

      if not saved_attractions:
         return []

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=True )

      return build_itinerary_attractions(
         attractions,
         saved_attractions )


   @classmethod
   def get_attractions_matching_query(
         cls,
         query,
         day,
         month,
         year,
         include_closed_attractions ):

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )

      return build_attractions_matching_query(
         attractions,
         query )


   @classmethod
   def get_attraction_likelihood_for_visit_date(
         cls,
         visit_date,
         attraction_name ):

      attraction_record = fetch_attraction_record_for_calendar_day(
         get_connection(),
         attraction_name=attraction_name,
         month=visit_date.month,
         day=visit_date.day )

      if attraction_record == None:
         return None

      likelihood, _ = get_attraction_likelihood_and_message_for_date(
         attraction_record=attraction_record,
         schedule_records=fetch_attraction_schedule_records( get_connection() ),
         schedule_override_records=fetch_attraction_schedule_override_records(
            get_connection() ),
         target_date=visit_date )

      return likelihood


   @classmethod
   def set_attraction_as_closed(
         cls,
         attraction,
         start_date,
         end_date,
         message ):
      schedule = build_attraction_closed_schedule(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_attraction_opening_schedule(
         get_connection(),
         schedule=schedule )


   @classmethod
   def set_attraction_closure_override(
         cls,
         attraction,
         start_date,
         end_date,
         message ):
      override = build_attraction_closure_override(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_attraction_schedule_override(
         get_connection(),
         override=override )


   @classmethod
   def set_attraction_opening_schedule(
         cls,
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
         message ):
      schedule = build_attraction_opening_schedule(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      return save_attraction_opening_schedule(
         get_connection(),
         schedule=schedule )
