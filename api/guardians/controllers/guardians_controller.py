from ... import zoo
from ..data_access.guardians_talk import fetch_meet_the_guardians_talk_records
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_occurrence_is_cancelled
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records
from ..logic.guardians_talk import build_guardians_talk_details
from ..logic.guardians_talk_schedule import build_guardians_talk_schedule_for_target_date


class GuardiansController():
   def __init__( self, conn ):
      self._conn = conn


   def get_guardians_talk_details( self, guardians_talks_to_include=None ):
      talk_records = fetch_meet_the_guardians_talk_records( self._conn )

      return build_guardians_talk_details(
         talk_records,
         guardians_talks_to_include=guardians_talks_to_include )


   def get_guardians_talk_schedule( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      return self.get_guardians_talk_schedule_for_target_date( target_date )


   def _guardians_talk_occurrence_is_cancelled( self, talk_name, location, cancellation_date, talk_time ):
      return fetch_guardians_talk_occurrence_is_cancelled(
         self._conn,
         talk_name,
         location,
         cancellation_date,
         talk_time )


   def get_guardians_talk_schedule_for_target_date( self, target_date ):
      records = fetch_guardians_talk_schedule_records( self._conn )

      return build_guardians_talk_schedule_for_target_date(
         records,
         target_date,
         self._guardians_talk_occurrence_is_cancelled )
