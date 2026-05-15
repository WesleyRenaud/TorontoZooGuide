from ..data_access.attraction import fetch_attraction_record_for_calendar_day
from ..data_access.attraction import fetch_attraction_records
from ..data_access.attraction import fetch_attraction_schedule_records
from ..logic.attraction import build_attractions
from ..logic.attraction import get_attraction_likelihood_and_message_for_date
from ..logic.attraction import resolve_attraction_context


class AttractionController():
   def __init__( self, conn ):
      self._conn = conn


   def get_attractions(
         self,
         month,
         day,
         include_closed_attractions=False ):

      context = resolve_attraction_context(
         month=month,
         day=day )

      return build_attractions(
         attraction_records=fetch_attraction_records(
            self._conn,
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_attraction_schedule_records( self._conn ),
         context=context,
         include_closed_attractions=include_closed_attractions )


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
