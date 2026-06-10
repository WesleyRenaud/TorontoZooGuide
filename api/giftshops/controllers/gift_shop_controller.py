from __future__ import annotations

from ..coordinators.gift_shop_coordinator import GiftShopCoordinator
from ...json_handler import JsonRequestHandler


class GiftShopController():
   @staticmethod
   def get_gift_shops( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shops = GiftShopCoordinator.get_gift_shops(
         day=data.get( 'day' ),
         month=data.get( 'month' ),
         year=data.get( 'year' ),
         include_closed_gift_shops=data.get( 'includeClosedGiftShops' ),
         gift_shops_to_include=data.get( 'giftShopsToInclude' ) )

      handler._write_json( {
         'gift_shops': [ gift_shop.to_dict() for gift_shop in gift_shops ],
      } )


   @staticmethod
   def get_gift_shop_names( handler: JsonRequestHandler ) -> None:
      gift_shops = GiftShopCoordinator.get_gift_shop_names()

      handler._write_json( {
         'gift_shops': gift_shops,
      } )


   @staticmethod
   def set_gift_shop_closed( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shop = data.get( 'giftShop' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = GiftShopCoordinator.set_gift_shop_as_closed(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'gift_shop': gift_shop,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not set "{ gift_shop }" as closed.'

      handler._write_json( response )


   @staticmethod
   def set_gift_shop_closure_override( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shop = data.get( 'giftShop' )
      start_date = data.get( 'startDate' )
      end_date = data.get( 'endDate' )
      message = data.get( 'message' )

      success = GiftShopCoordinator.set_gift_shop_closure_override(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         message=message )

      response = {
         'success': success,
         'gift_shop': gift_shop,
         'startDate': start_date,
         'endDate': end_date,
         'message': message,
      }

      if not success:
         response[ 'error' ] = f'Could not create closure override for "{ gift_shop }".'

      handler._write_json( response )


   @staticmethod
   def set_gift_shop_opening_schedule( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shop = data.get( 'giftShop' )
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

      success = GiftShopCoordinator.set_gift_shop_opening_schedule(
         gift_shop=gift_shop,
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
         'gift_shop': gift_shop,
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
         response[ 'error' ] = f'Could not set opening schedule for "{ gift_shop }".'
         response[ 'errorType' ] = 'overlappingSchedule'

      handler._write_json( response )


   @staticmethod
   def replace_gift_shop_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shop = data.get( 'giftShop' )
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

      success = GiftShopCoordinator.replace_gift_shop_opening_schedule_overlaps(
         gift_shop=gift_shop,
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
         'gift_shop': gift_shop,
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
            f'Could not replace opening schedule overlaps for "{ gift_shop }".'
         )

      handler._write_json( response )


   @staticmethod
   def trim_gift_shop_opening_schedule_overlaps( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      gift_shop = data.get( 'giftShop' )
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

      success = GiftShopCoordinator.trim_gift_shop_opening_schedule_overlaps(
         gift_shop=gift_shop,
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
         'gift_shop': gift_shop,
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
            f'Could not trim opening schedule overlaps for "{ gift_shop }".'
         )

      handler._write_json( response )
