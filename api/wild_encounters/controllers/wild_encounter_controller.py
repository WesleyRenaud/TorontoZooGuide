from __future__ import annotations

from ..coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from ...json_handler import JsonRequestHandler


class WildEncounterController():
   @staticmethod
   def get_wild_encounters( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounters = WildEncounterCoordinator.get_available_wild_encounters(
         month=data.get( 'month' ),
         day=data.get( 'day' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'wild_encounters': [ wild_encounter.to_dict() for wild_encounter in wild_encounters ],
      } )


   @staticmethod
   def get_wild_encounter_names( handler: JsonRequestHandler ) -> None:
      wild_encounters = WildEncounterCoordinator.get_wild_encounter_names()

      handler._write_json( {
         'wild_encounters': wild_encounters,
      } )


   @staticmethod
   def get_wild_encounter_occurrences( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )

      occurrences = WildEncounterCoordinator.get_wild_encounter_occurrences(
         wild_encounter_name=wild_encounter )

      handler._write_json( {
         'occurrences': [ occurrence.to_dict() for occurrence in occurrences ],
         'wildEncounter': wild_encounter,
      } )


   @staticmethod
   def set_wild_encounter_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_start_date = data.get( 'startDate' )
      schedule_end_date = data.get( 'endDate' )
      encounter_times = data.get( 'times' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      message = data.get( 'message' )

      success = WildEncounterCoordinator.set_wild_encounter_schedule(
         wild_encounter_name=wild_encounter,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         encounter_times=encounter_times,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         message=message )

      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'startDate': schedule_start_date,
         'endDate': schedule_end_date,
         'times': encounter_times,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set schedule for "{ wild_encounter }".'

      handler._write_json( response )


   @staticmethod
   def get_wild_encounter_schedule_times( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_times = WildEncounterCoordinator.get_wild_encounter_schedule_times(
         wild_encounter_name=wild_encounter )

      handler._write_json( {
         'wildEncounter': wild_encounter,
         'times': schedule_times,
      } )


   @staticmethod
   def end_wild_encounter_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      schedule_end_date = data.get( 'endDate' )
      encounter_times = data.get( 'times' )

      success = WildEncounterCoordinator.end_wild_encounter_schedule(
         wild_encounter_name=wild_encounter,
         schedule_end_date=schedule_end_date,
         encounter_times=encounter_times )

      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'endDate': schedule_end_date,
         'times': encounter_times,
      }

      if not success:
         response[ 'error' ] = f'Could not end schedule for "{ wild_encounter }".'

      handler._write_json( response )


   @staticmethod
   def cancel_wild_encounter_occurrence( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      wild_encounter = data.get( 'wildEncounter' )
      date = data.get( 'date' )
      encounter_times = data.get( 'times' )

      success = WildEncounterCoordinator.cancel_wild_encounter_occurrence(
         wild_encounter_name=wild_encounter,
         date=date,
         encounter_times=encounter_times )

      response = {
         'success': success,
         'wildEncounter': wild_encounter,
         'date': date,
         'times': encounter_times,
      }

      if not success:
         response[ 'error' ] = f'Could not cancel "{ wild_encounter }" on { date }.'

      handler._write_json( response )
