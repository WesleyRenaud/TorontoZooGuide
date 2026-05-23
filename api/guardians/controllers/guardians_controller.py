from ... import zoo
from ..data_access.guardians_talk import fetch_guardians_talk_locations
from ..data_access.guardians_talk import fetch_guardians_talk_names
from ..data_access.guardians_talk import fetch_guardians_talk_names_at_location
from ..data_access.guardians_talk import fetch_meet_the_guardians_talk_records
from ..data_access.guardians_talk_cancellation import save_guardians_talk_cancellation
from ..data_access.guardians_talk_schedule import save_guardians_talk_schedule
from ..data_access.guardians_talk_schedule import save_guardians_talk_schedule_end
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_cancellation_records
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_occurrence_is_cancelled
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_record_for_occurrences
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records
from ..logic.guardians_talk import build_guardians_talk_details
from ..logic.guardians_talk_occurrences import build_guardians_talk_occurrences
from ..logic.guardians_talk_schedule import build_guardians_talk_schedule_for_target_date
from ..logic.guardians_talk_schedule_status import build_guardians_talk_schedule
from ..logic.guardians_talk_cancellation_status import build_guardians_talk_cancellation
from ..logic.guardians_talk_schedule_status import build_guardians_talk_schedule_end
from ..logic.guardians_talk_schedule import find_guardians_talk_on_day_schedule
from ..logic.guardians_talks_matching_query import build_guardians_talks_matching_query
from ..logic.itinerary_guardians_talks import build_itinerary_guardians_talks
from ...request_connection import get_connection


class GuardiansController():


   @classmethod
   def get_guardians_talk_locations( cls ):
      return fetch_guardians_talk_locations( get_connection() )


   @classmethod
   def get_guardians_talk_names( cls ):
      return fetch_guardians_talk_names( get_connection() )


   @classmethod
   def get_guardians_talk_names_at_location( cls, location ):
      return fetch_guardians_talk_names_at_location(
         get_connection(),
         location=location )


   @classmethod
   def get_guardians_talk_occurrences( cls, talk, location, days_ahead=60 ):
      schedule_record = fetch_guardians_talk_schedule_record_for_occurrences(
         get_connection(),
         talk_name=talk,
         location=location )
      cancellation_records = fetch_guardians_talk_cancellation_records(
         get_connection(),
         talk_name=talk,
         location=location )

      return build_guardians_talk_occurrences(
         schedule_record=schedule_record,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead )


   @classmethod
   def get_guardians_talk_details( cls, guardians_talks_to_include=None ):
      talk_records = fetch_meet_the_guardians_talk_records( get_connection() )

      return build_guardians_talk_details(
         talk_records,
         guardians_talks_to_include=guardians_talks_to_include )


   @classmethod
   def set_guardians_talk_schedule(
         cls,
         talk,
         location,
         start_date,
         end_date,
         monday_time,
         tuesday_time,
         wednesday_time,
         thursday_time,
         friday_time,
         saturday_time,
         sunday_time,
         message ):
      schedule = build_guardians_talk_schedule(
         talk=talk,
         location=location,
         start_date=start_date,
         end_date=end_date,
         monday_time=monday_time,
         tuesday_time=tuesday_time,
         wednesday_time=wednesday_time,
         thursday_time=thursday_time,
         friday_time=friday_time,
         saturday_time=saturday_time,
         sunday_time=sunday_time,
         message=message )

      return save_guardians_talk_schedule(
         get_connection(),
         schedule=schedule )


   @classmethod
   def end_guardians_talk_schedule( cls, talk, location, schedule_end_date ):
      schedule_end = build_guardians_talk_schedule_end(
         talk=talk,
         location=location,
         schedule_end_date=schedule_end_date )

      return save_guardians_talk_schedule_end(
         get_connection(),
         schedule_end=schedule_end )


   @classmethod
   def cancel_guardians_talk_occurrence( cls, talk, location, date, time ):
      cancellation = build_guardians_talk_cancellation(
         talk=talk,
         location=location,
         date=date,
         time=time )

      return save_guardians_talk_cancellation(
         get_connection(),
         cancellation=cancellation )


   @classmethod
   def get_guardians_talks_for_saved_itinerary( cls, saved_guardians_talks ):
      if not saved_guardians_talks:
         return []

      guardians_talk_names = [
         saved_talk.talk_name
         for saved_talk in saved_guardians_talks
      ]

      guardians_talks = cls.get_guardians_talk_details(
         guardians_talk_names )

      return build_itinerary_guardians_talks(
         guardians_talks,
         saved_guardians_talks )


   @classmethod
   def get_guardians_talk_schedule( cls, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      return cls.get_guardians_talk_schedule_for_target_date( target_date )


   @classmethod
   def get_guardians_talks_matching_query( cls, query, month, day, year ):
      guardians_talks = cls.get_guardians_talk_schedule(
         month=month,
         day=day,
         year=year )

      return build_guardians_talks_matching_query(
         guardians_talks,
         query )


   @classmethod
   def get_guardians_talk_on_day_schedule(
         cls,
         month,
         day,
         talk_name,
         year,
         day_schedule=None ):
      rows = (
         day_schedule
         if day_schedule is not None
         else cls.get_guardians_talk_schedule(
            month=month,
            day=day,
            year=year )
      )

      return find_guardians_talk_on_day_schedule(
         rows,
         talk_name )


   @classmethod
   def _guardians_talk_occurrence_is_cancelled( cls, talk_name, location, cancellation_date, talk_time ):
      return fetch_guardians_talk_occurrence_is_cancelled(
         get_connection(),
         talk_name,
         location,
         cancellation_date,
         talk_time )


   @classmethod
   def get_guardians_talk_schedule_for_target_date( cls, target_date ):
      records = fetch_guardians_talk_schedule_records( get_connection() )

      return build_guardians_talk_schedule_for_target_date(
         records,
         target_date,
         cls._guardians_talk_occurrence_is_cancelled )
