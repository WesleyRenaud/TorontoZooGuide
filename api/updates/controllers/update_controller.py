from ... import database as database_module
from ... import zoo
from ..data_access.update import fetch_updates
from ..data_access.update import insert_update
from ..logic.update_creation import build_update_create_input
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


   def create_update(
         self,
         title,
         description,
         update_type,
         start_date,
         end_date ):
      update = build_update_create_input(
         title=title,
         description=description,
         update_type=update_type,
         start_date=start_date,
         end_date=end_date )

      return insert_update(
         self._conn,
         update=update )
