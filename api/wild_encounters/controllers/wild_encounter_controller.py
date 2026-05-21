from ... import zoo
from ..data_access.wild_encounter import fetch_wild_encounter_names
from ..data_access.wild_encounter import fetch_wild_encounter_records
from ..data_access.wild_encounter_cancellation import save_wild_encounter_cancellation
from ..data_access.wild_encounter_schedule import save_wild_encounter_schedule
from ..data_access.wild_encounter_schedule import save_wild_encounter_schedule_end
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_cancellation_records
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_record_for_occurrences
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_records
from ..logic.wild_encounter import build_wild_encounter_details
from ..logic.wild_encounter_occurrences import build_wild_encounter_occurrences
from ..logic.wild_encounter_schedule_status import build_wild_encounter_schedule
from ..logic.wild_encounter_cancellation_status import build_wild_encounter_cancellation
from ..logic.wild_encounter_schedule_status import build_wild_encounter_schedule_end
from ..logic.wild_encounter_schedule import build_wild_encounter_schedule_for_target_date
from ..logic.wild_encounter_schedule import filter_available_wild_encounters
from ..logic.wild_encounter_schedule import find_wild_encounter_on_day_schedule
from ..logic.wild_encounters_matching_query import build_wild_encounters_matching_query
from ..logic.itinerary_wild_encounters import build_itinerary_wild_encounters


class WildEncounterController():
   def __init__( self, conn ):
      self._conn = conn


   def get_wild_encounter_names( self ):
      return fetch_wild_encounter_names( self._conn )


   def get_wild_encounter_occurrences( self, wild_encounter, days_ahead=60 ):
      schedule_record = fetch_wild_encounter_schedule_record_for_occurrences(
         self._conn,
         wild_encounter=wild_encounter )
      cancellation_records = fetch_wild_encounter_cancellation_records(
         self._conn,
         wild_encounter=wild_encounter )

      return build_wild_encounter_occurrences(
         schedule_record=schedule_record,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead )


   def get_wild_encounter_details( self, wild_encounters_to_include=None ):
      wild_encounter_records = fetch_wild_encounter_records( self._conn )

      return build_wild_encounter_details(
         wild_encounter_records,
         wild_encounters_to_include=wild_encounters_to_include )


   def set_wild_encounter_schedule(
         self,
         wild_encounter,
         start_date,
         end_date,
         encounter_time,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         message ):
      schedule = build_wild_encounter_schedule(
         wild_encounter=wild_encounter,
         start_date=start_date,
         end_date=end_date,
         encounter_time=encounter_time,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         message=message )

      return save_wild_encounter_schedule(
         self._conn,
         schedule=schedule )


   def end_wild_encounter_schedule( self, wild_encounter, schedule_end_date ):
      schedule_end = build_wild_encounter_schedule_end(
         wild_encounter=wild_encounter,
         schedule_end_date=schedule_end_date )

      return save_wild_encounter_schedule_end(
         self._conn,
         schedule_end=schedule_end )


   def cancel_wild_encounter_occurrence( self, wild_encounter, date, time ):
      cancellation = build_wild_encounter_cancellation(
         wild_encounter=wild_encounter,
         date=date,
         time=time )

      return save_wild_encounter_cancellation(
         self._conn,
         cancellation=cancellation )


   def get_wild_encounters_for_saved_itinerary( self, saved_wild_encounters ):
      if not saved_wild_encounters:
         return []

      wild_encounter_names = [
         saved_encounter.wild_encounter
         for saved_encounter in saved_wild_encounters
      ]

      wild_encounters = self.get_wild_encounter_details(
         wild_encounter_names )

      return build_itinerary_wild_encounters(
         wild_encounters,
         saved_wild_encounters )


   def get_wild_encounter_schedule( self, month, day, year ):
      target_date = zoo.ZooUtil.visit_target_date(
         month=month,
         day=day,
         year=year )

      records = fetch_wild_encounter_schedule_records(
         self._conn,
         target_date )

      return build_wild_encounter_schedule_for_target_date(
         records,
         target_date )


   def get_wild_encounter_on_day_schedule(
         self,
         month,
         day,
         encounter_name,
         year,
         day_schedule=None ):
      rows = (
         day_schedule
         if day_schedule is not None
         else self.get_wild_encounter_schedule(
            month=month,
            day=day,
            year=year )
      )

      return find_wild_encounter_on_day_schedule(
         rows,
         encounter_name )


   def get_available_wild_encounters( self, month, day, year ):
      return filter_available_wild_encounters(
         self.get_wild_encounter_schedule(
            month=month,
            day=day,
            year=year ) )


   def get_wild_encounters_matching_query( self, query, month, day, year ):
      wild_encounters = self.get_available_wild_encounters(
         month=month,
         day=day,
         year=year )

      return build_wild_encounters_matching_query(
         wild_encounters,
         query )
