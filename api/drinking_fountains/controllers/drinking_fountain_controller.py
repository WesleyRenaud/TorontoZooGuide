from ... import zoo
from ..data_access.drinking_fountain import fetch_drinking_fountain_records
from ..data_access.drinking_fountain_status import save_drinking_fountain_closed_status
from ..data_access.drinking_fountain_status import save_drinking_fountain_open_status
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_seasonal_likelihood
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_status_record
from ..logic.drinking_fountain import build_drinking_fountains
from ..logic.drinking_fountain_status import build_drinking_fountain_closed_status
from ..logic.drinking_fountain_status import build_drinking_fountain_open_status
from ..logic.drinking_fountain_status import build_drinking_fountain_seasonal_status
from ..logic.drinking_fountain_status import build_drinking_fountain_status
from ..logic.drinking_fountain_status import drinking_fountain_status_applies_to_date


class DrinkingFountainController():
   def __init__( self, conn ):
      self._conn = conn


   def get_drinking_fountains( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      status_record = fetch_drinking_fountain_status_record( self._conn )

      if status_record and drinking_fountain_status_applies_to_date( status_record, target_date ):
         is_closed, closed_message, likelihood = build_drinking_fountain_status(
            status_record )
      else:
         seasonal_likelihood = fetch_drinking_fountain_seasonal_likelihood(
            self._conn,
            target_date )
         is_closed, closed_message, likelihood = build_drinking_fountain_seasonal_status(
            seasonal_likelihood )

      fountain_records = fetch_drinking_fountain_records( self._conn )

      return build_drinking_fountains(
         fountain_records,
         is_closed,
         closed_message,
         likelihood )


   def set_drinking_fountains_as_closed( self, start_date=None, end_date=None, message=None ):
      status = build_drinking_fountain_closed_status(
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_drinking_fountain_closed_status(
         self._conn,
         status=status )


   def set_drinking_fountains_as_open( self, start_date=None, end_date=None ):
      status = build_drinking_fountain_open_status(
         start_date=start_date,
         end_date=end_date )

      return save_drinking_fountain_open_status(
         self._conn,
         status=status )
