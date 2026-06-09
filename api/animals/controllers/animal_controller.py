from __future__ import annotations

from ..coordinators.animal_coordinator import AnimalCoordinator
from ...json_handler import JsonRequestHandler
from ...shared.enums import AnimalViewingScope
from ...shared.typed_dict import to_dict_with_type


class AnimalController():


   @staticmethod
   def get_visible_animals( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      animals = AnimalCoordinator.get_animals_viewable_on_day(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         temp=data.get( 'temp' ),
         include_off_display_animals=data.get( 'includeOffDisplayAnimals' ) or False,
         threshold=0 )

      handler._write_json( {
         'animals': [ animal.to_dict() for animal in animals ],
      } )


   @staticmethod
   def get_animal_viewing_scopes( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      viewing_scopes = AnimalCoordinator.get_animal_viewing_scopes(
         species=data.get( 'species' ),
         exhibit=data.get( 'exhibit' ) )

      handler._write_json( {
         'viewingScopes': [
            viewing_scope.value for viewing_scope in viewing_scopes
         ],
      } )


   @staticmethod
   def get_animal_information( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      animal_info = AnimalCoordinator.get_animal_information( species=data.get( 'species' ) )

      handler._write_json( {
         'information': [ animal_info.to_dict() ],
      } )


   @staticmethod
   def get_animals_by_exhibit( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      animals = AnimalCoordinator.get_animals_viewable_on_day(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         temp=data.get( 'temp' ),
         include_off_display_animals=False,
         threshold=0,
         exhibits_to_include=data.get( 'exhibitsToInclude' ) or [] )

      handler._write_json( {
         'animals': [
            to_dict_with_type( animal, 'animal' ) for animal in animals
         ],
      } )


   @staticmethod
   def get_animal_species_names( handler: JsonRequestHandler ) -> None:
      species = AnimalCoordinator.get_animal_species_names()

      handler._write_json( {
         'species': species,
      } )


   @staticmethod
   def set_animal_off_display( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )
      viewing_scope = AnimalViewingScope.normalize( data.get( 'viewingScope' ) )

      success = AnimalCoordinator.set_animal_as_off_display(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message,
         viewing_scope=viewing_scope )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
         'viewingScope': viewing_scope.value,
      }

      if not success:
         response[ 'error' ] = f'No animal found with species "{ species }".'

      handler._write_json( response )


   @staticmethod
   def set_animal_on_display( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )
      viewing_scope = AnimalViewingScope.normalize( data.get( 'viewingScope' ) )

      success = AnimalCoordinator.set_animal_as_on_display(
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
         'viewingScope': viewing_scope.value,
      }

      if not success:
         response[ 'error' ] = f'No off-display entry found for "{ species }" in "{ exhibit }".'

      handler._write_json( response )


   @staticmethod
   def set_animal_visibility_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      daily_start_time = data.get( 'dailyStartTime' )
      daily_end_time = data.get( 'dailyEndTime' )
      message = data.get( 'message' )

      success = AnimalCoordinator.set_animal_limited_viewing_schedule(
         species=species,
         exhibit=exhibit,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         daily_start_time=daily_start_time,
         daily_end_time=daily_end_time,
         message=message )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'dailyStartTime': daily_start_time,
         'dailyEndTime': daily_end_time,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not set limited viewing schedule for "{ species }" in "{ exhibit }".'
         )

      handler._write_json( response )


   @staticmethod
   def remove_animal_visibility_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )

      success = AnimalCoordinator.remove_animal_visibility_schedule(
         species=species,
         exhibit=exhibit )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not remove visibility schedule for "{ species }" in "{ exhibit }".'
         )

      handler._write_json( response )


   @staticmethod
   def set_animal_viewing_alert( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )
      alert_start_date = data.get( 'alertStartDate' )
      alert_end_date = data.get( 'alertEndDate' )
      message = data.get( 'message' )

      success = AnimalCoordinator.set_animal_viewing_alert(
         species=species,
         exhibit=exhibit,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
         'alertStartDate': alert_start_date,
         'alertEndDate': alert_end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not set viewing alert for "{ species }" in "{ exhibit }".'
         )

      handler._write_json( response )


   @staticmethod
   def remove_animal_viewing_alert( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      species = data.get( 'species' )
      exhibit = data.get( 'exhibit' )

      success = AnimalCoordinator.remove_animal_viewing_alert(
         species=species,
         exhibit=exhibit )

      response = {
         'success': success,
         'species': species,
         'exhibit': exhibit,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not remove viewing alert for "{ species }" in "{ exhibit }".'
         )

      handler._write_json( response )
