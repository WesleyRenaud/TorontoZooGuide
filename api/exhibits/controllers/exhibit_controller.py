from __future__ import annotations

from ..coordinators.exhibit_coordinator import ExhibitCoordinator
from ...json_handler import JsonRequestHandler


class ExhibitController():


   @staticmethod
   def get_exhibits_in_region( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      exhibits = ExhibitCoordinator.get_exhibits_in_region( region=data.get( 'region' ) )

      handler._write_json( {
         'exhibits': exhibits,
      } )


   @staticmethod
   def get_regions( handler: JsonRequestHandler ) -> None:
      regions = ExhibitCoordinator.get_regions()

      handler._write_json( {
         'regions': [ region.to_dict() for region in regions ],
      } )


   @staticmethod
   def get_animal_names_by_exhibit( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      animals = ExhibitCoordinator.get_names_of_animals_in_exhibit(
         exhibit=data.get( 'exhibit' ) )

      handler._write_json( {
         'animals': animals,
      } )


   @staticmethod
   def get_closed_exhibits( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      closed_exhibits = ExhibitCoordinator.get_closed_exhibits_for_visit_date(
         month=data.get( 'month' ),
         day=data.get( 'day' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'closed_exhibits': closed_exhibits,
      } )


   @staticmethod
   def get_exhibits_by_region( handler: JsonRequestHandler ) -> None:
      regions = ExhibitCoordinator.get_regions_with_exhibits()

      handler._write_json( {
         'regions': [ region.to_dict() for region in regions ],
      } )


   @staticmethod
   def get_exhibits( handler: JsonRequestHandler ) -> None:
      exhibits = ExhibitCoordinator.get_exhibits()

      handler._write_json( {
         'exhibits': exhibits,
      } )


   @staticmethod
   def set_exhibit_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      exhibit = data.get( 'exhibit' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = ExhibitCoordinator.set_exhibit_as_closed(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'exhibit': exhibit,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ exhibit }" as closed.'

      handler._write_json( response )


   @staticmethod
   def set_exhibit_open( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      exhibit = data.get( 'exhibit' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = ExhibitCoordinator.set_exhibit_as_open(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'exhibit': exhibit,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ exhibit }" as open.'

      handler._write_json( response )
