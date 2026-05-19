from ... import zoo
from ..data_access.drinking_fountain import fetch_drinking_fountain_records
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_seasonal_likelihood
from ..data_access.drinking_fountain_status import fetch_drinking_fountain_status_record
from ..logic.drinking_fountain import build_drinking_fountains
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

      if drinking_fountain_status_applies_to_date( status_record, target_date ):
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
