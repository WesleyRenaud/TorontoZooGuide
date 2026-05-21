from ... import zoo
from ..data_access.restroom import fetch_restroom_names
from ..data_access.restroom import fetch_restroom_records
from ..data_access.restroom_alert import delete_restroom_alert
from ..data_access.restroom_alert import save_restroom_alert
from ..data_access.restroom_status import save_restroom_closed_status
from ..data_access.restroom_status import save_restroom_open_status
from ..logic.restroom import build_restrooms
from ..logic.restroom_alert_builder import build_restroom_alert
from ..logic.restroom import resolve_restroom_context
from ..logic.restroom_status import build_restroom_closed_status
from ..logic.restrooms_matching_query import build_restrooms_matching_query


class RestroomController():
   def __init__( self, conn ):
      self._conn = conn


   def get_restroom_names( self ):
      return fetch_restroom_names( self._conn )


   def get_restrooms(
         self,
         day,
         month,
         year,
         include_closed_restrooms=False ):

      return build_restrooms(
         restroom_records=fetch_restroom_records( self._conn ),
         context=resolve_restroom_context(
            day=day,
            month=month,
            year=year ),
         include_closed_restrooms=include_closed_restrooms )


   def get_restrooms_matching_query(
         self,
         query,
         day,
         month,
         year,
         include_closed_restrooms ):

      restrooms = self.get_restrooms(
         day=day,
         month=month,
         year=year,
         include_closed_restrooms=include_closed_restrooms )

      return build_restrooms_matching_query(
         restrooms,
         query )


   def set_restroom_as_closed( self, restroom, start_date, end_date, message ):
      status = build_restroom_closed_status(
         restroom=restroom,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_restroom_closed_status(
         self._conn,
         restroom=status.restroom,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   def set_restroom_as_open( self, restroom, start_date, end_date ):
      date_range = zoo.ZooUtil.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return save_restroom_open_status(
         self._conn,
         restroom=restroom,
         start_date=date_range.start_date,
         end_date=date_range.end_date )


   def set_restroom_alert(
         self,
         restroom,
         alert_start_date,
         alert_end_date,
         message ):
      alert = build_restroom_alert(
         restroom=restroom,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      return save_restroom_alert(
         self._conn,
         restroom=alert.restroom,
         alert_start_date=alert.start_date,
         alert_end_date=alert.end_date,
         message=alert.message )


   def remove_restroom_alert( self, restroom ):
      return delete_restroom_alert(
         self._conn,
         restroom=restroom )
