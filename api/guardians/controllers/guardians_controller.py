from ... import zoo
from ..data_access.guardians_talk import fetch_meet_the_guardians_talk_records
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_occurrence_is_cancelled
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records
from ..logic.guardians_talk import build_guardians_talk_details
from ..logic.guardians_talk_schedule import build_guardians_talk_schedule_for_target_date
from ..logic.guardians_talk_schedule import find_guardians_talk_on_day_schedule
from ..logic.guardians_talks_matching_query import build_guardians_talks_matching_query
from ..logic.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from ..logic.itinerary_guardians_talks import build_itinerary_guardians_talks


class GuardiansController():
   def __init__( self, conn ):
      self._conn = conn


   def get_guardians_talk_details( self, guardians_talks_to_include=None ):
      talk_records = fetch_meet_the_guardians_talk_records( self._conn )

      return build_guardians_talk_details(
         talk_records,
         guardians_talks_to_include=guardians_talks_to_include )


   def get_guardians_talks_for_saved_itinerary( self, saved_guardians_talks ):
      if not saved_guardians_talks:
         return []

      guardians_talk_names = [
         saved_talk.talk_name
         for saved_talk in saved_guardians_talks
      ]

      guardians_talks = self.get_guardians_talk_details(
         guardians_talk_names )

      return build_itinerary_guardians_talks(
         guardians_talks,
         saved_guardians_talks )


   def get_guardians_talk_schedule( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      return self.get_guardians_talk_schedule_for_target_date( target_date )


   def get_guardians_talks_matching_query( self, query, month, day, year ):
      guardians_talks = self.get_guardians_talk_schedule(
         month=month,
         day=day,
         year=year )

      return build_guardians_talks_matching_query(
         guardians_talks,
         query )


   def get_guardians_talk_on_day_schedule(
         self,
         month,
         day,
         talk_name,
         year,
         day_schedule=None ):
      rows = (
         day_schedule
         if day_schedule is not None
         else self.get_guardians_talk_schedule(
            month=month,
            day=day,
            year=year )
      )

      return find_guardians_talk_on_day_schedule(
         rows,
         talk_name )


   def validate_guardians_talks(
         self,
         month,
         day,
         year,
         guardians_talks_to_include=None ):
      day_schedule = self.get_guardians_talk_schedule(
         month=month,
         day=day,
         year=year )

      return validate_guardians_talks_for_itinerary(
         guardians_talks_to_include,
         day_schedule )


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
