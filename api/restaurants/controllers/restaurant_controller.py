from __future__ import annotations

from ..coordinators.restaurant_coordinator import RestaurantCoordinator
from ...json_handler import JsonRequestHandler


class RestaurantController():
   @staticmethod
   def get_restaurants( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurants = RestaurantCoordinator.get_restaurants(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         include_closed_restaurants=data.get( 'includeClosedRestaurants' ),
         restaurants_to_include=data.get( 'restaurantsToInclude' ) )

      handler._write_json( {
         'restaurants': [ restaurant.to_dict() for restaurant in restaurants ],
      } )


   @staticmethod
   def get_restaurant_names( handler: JsonRequestHandler ) -> None:
      restaurants = RestaurantCoordinator.get_restaurant_names()

      handler._write_json( {
         'restaurants': restaurants,
      } )


   @staticmethod
   def set_restaurant_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurant = data.get( 'restaurant' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = RestaurantCoordinator.set_restaurant_as_closed(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'restaurant': restaurant,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ restaurant }" as closed.'

      handler._write_json( response )


   @staticmethod
   def set_restaurant_closure_override( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurant = data.get( 'restaurant' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = RestaurantCoordinator.set_restaurant_closure_override(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'restaurant': restaurant,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not create closure override for "{ restaurant }".'

      handler._write_json( response )


   @staticmethod
   def set_restaurant_opening_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurant = data.get( 'restaurant' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = RestaurantCoordinator.set_restaurant_opening_schedule(
         restaurant=restaurant,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'restaurant': restaurant,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set opening schedule for "{ restaurant }".'
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_restaurant_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurant = data.get( 'restaurant' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = RestaurantCoordinator.replace_restaurant_opening_schedule_overlaps(
         restaurant=restaurant,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'restaurant': restaurant,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not replace opening schedule overlaps for "{ restaurant }".'
         )

      handler._write_json( response )


   @staticmethod
   def trim_restaurant_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      restaurant = data.get( 'restaurant' )
      schedule_start_date = data.get( 'scheduleStartDate' )
      schedule_end_date = data.get( 'scheduleEndDate' )
      monday = data.get( 'monday' )
      tuesday = data.get( 'tuesday' )
      wednesday = data.get( 'wednesday' )
      thursday = data.get( 'thursday' )
      friday = data.get( 'friday' )
      saturday = data.get( 'saturday' )
      sunday = data.get( 'sunday' )
      holidays_only = data.get( 'holidaysOnly' )
      message = data.get( 'message' )

      success = RestaurantCoordinator.trim_restaurant_opening_schedule_overlaps(
         restaurant=restaurant,
         start_date=schedule_start_date,
         end_date=schedule_end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message )

      response = {
         'success': success,
         'restaurant': restaurant,
         'scheduleStartDate': schedule_start_date,
         'scheduleEndDate': schedule_end_date,
         'monday': monday,
         'tuesday': tuesday,
         'wednesday': wednesday,
         'thursday': thursday,
         'friday': friday,
         'saturday': saturday,
         'sunday': sunday,
         'holidaysOnly': holidays_only,
         'message': message,
      }

      if not success:
         response[ 'error' ] = (
            f'Could not trim opening schedule overlaps for "{ restaurant }".'
         )

      handler._write_json( response )
