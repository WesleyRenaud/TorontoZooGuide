from ... import zoo
from ..data_access.wild_encounter import fetch_wild_encounter_records
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_records
from ..logic.wild_encounter import build_wild_encounter_details
from ..logic.wild_encounter_schedule import build_wild_encounter_schedule_for_target_date
from ..logic.wild_encounter_schedule import filter_available_wild_encounters
from ..logic.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary
from ..logic.wild_encounter_schedule import find_wild_encounter_on_day_schedule
from ..logic.wild_encounters_matching_query import build_wild_encounters_matching_query
from ..logic.itinerary_wild_encounters import build_itinerary_wild_encounters


class WildEncounterController():
   def __init__( self, conn ):
      self._conn = conn


   def get_wild_encounter_details( self, wild_encounters_to_include=None ):
      wild_encounter_records = fetch_wild_encounter_records( self._conn )

      return build_wild_encounter_details(
         wild_encounter_records,
         wild_encounters_to_include=wild_encounters_to_include )


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


   def validate_wild_encounters(
         self,
         month,
         day,
         year,
         wild_encounters_to_include=None ):
      day_schedule = self.get_wild_encounter_schedule(
         month=month,
         day=day,
         year=year )

      return validate_wild_encounters_for_itinerary(
         wild_encounters_to_include,
         day_schedule )


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
