from ..data_access.attraction import fetch_attraction_record_for_calendar_day
from ..data_access.attraction import fetch_attraction_names
from ..data_access.attraction import fetch_attraction_records
from ..data_access.attraction import fetch_attraction_schedule_records
from ..logic.attraction import build_attractions
from ..logic.attraction import get_attraction_likelihood_and_message_for_date
from ..logic.attraction import resolve_attraction_context
from ..logic.attractions_matching_query import build_attractions_matching_query
from ..logic.itinerary_attractions import build_itinerary_attractions


class AttractionController():
   def __init__( self, conn ):
      self._conn = conn


   def get_attraction_names( self ):
      return fetch_attraction_names( self._conn )


   def get_attractions(
         self,
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
            self._conn,
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_attraction_schedule_records( self._conn ),
         context=context,
         include_closed_attractions=include_closed_attractions )


   def get_attractions_for_saved_itinerary(
         self,
         day,
         month,
         year,
         saved_attractions ):

      if not saved_attractions:
         return []

      attractions = self.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=True )

      return build_itinerary_attractions(
         attractions,
         saved_attractions )


   def get_attractions_matching_query(
         self,
         query,
         day,
         month,
         year,
         include_closed_attractions ):

      attractions = self.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )

      return build_attractions_matching_query(
         attractions,
         query )


   def get_attraction_likelihood_for_visit_date(
         self,
         visit_date,
         attraction_name ):

      attraction_record = fetch_attraction_record_for_calendar_day(
         self._conn,
         attraction_name=attraction_name,
         month=visit_date.month,
         day=visit_date.day )

      if attraction_record == None:
         return None

      likelihood, _ = get_attraction_likelihood_and_message_for_date(
         attraction_record=attraction_record,
         schedule_records=fetch_attraction_schedule_records( self._conn ),
         target_date=visit_date )

      return likelihood
