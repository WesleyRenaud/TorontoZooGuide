from ... import zoo
from ..data_access.zoo_hours import fetch_zoo_hours_record
from ..logic.zoo_hours import build_zoo_hours


class ZooHoursController():
   def __init__( self, conn ):
      self._conn = conn


   def get_zoo_hours( self, day, month, year ):
      operating_date = zoo.ZooUtil.visit_target_date(
         month,
         day,
         year )

      zoo_hours_record = fetch_zoo_hours_record(
         self._conn,
         operating_date )

      if zoo_hours_record == None:
         return None

      return build_zoo_hours( zoo_hours_record )
