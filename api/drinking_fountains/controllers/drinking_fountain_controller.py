from __future__ import annotations

from ..coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from ...json_handler import JsonRequestHandler


class DrinkingFountainController():


   @staticmethod
   def get_drinking_fountains( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      drinking_fountains = DrinkingFountainCoordinator.get_drinking_fountains(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ) )

      handler._write_json( {
         'drinking_fountains': [
            drinking_fountain.to_dict() for drinking_fountain in drinking_fountains
         ],
      } )


   @staticmethod
   def set_drinking_fountains_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = DrinkingFountainCoordinator.set_drinking_fountains_as_closed(
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = 'Could not set drinking fountains as closed.'

      handler._write_json( response )


   @staticmethod
   def set_drinking_fountains_open( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )

      success = DrinkingFountainCoordinator.set_drinking_fountains_as_open(
         start_date=start_date,
         end_date=end_date )

      response = {
         'success': success,
         'startDate': start_date,
         'endDate': end_date,
      }

      if not success:
         response[ 'error' ] = 'Could not set drinking fountains as open.'

      handler._write_json( response )
