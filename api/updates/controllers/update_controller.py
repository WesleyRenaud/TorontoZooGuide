from ... import database as database_module
from ... import zoo
from ..data_access.update import fetch_updates
from ..logic.update import filter_updates_started_on_or_before


class UpdateController():
   def __init__( self, conn ):
      self._conn = conn


   def get_updates_for_visit_date( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      updates = fetch_updates( self._conn, target_date )

      return filter_updates_started_on_or_before(
         updates,
         target_date )


   def get_unexpired_updates( self ):
      as_of_date = database_module.datetime.now().date()

      return fetch_updates( self._conn, as_of_date )
