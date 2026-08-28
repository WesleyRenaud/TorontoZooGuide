from __future__ import annotations

from api_test_support.json_handler_test_double import JsonHandlerTestDouble
from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_gift_shop_coordinator import StubGiftShopCoordinator
import pytest

from api import database_connection_provider as connection
from api.giftshops.controllers.gift_shop_controller import GiftShopController
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
import api.http_request_handler as server
from api.models.gift_shop import GiftShop
import api.request_connection_provider as request_connection
from api.types import Types


GIFT_SHOP_NAME = 'Zootique'
OTHER_GIFT_SHOP_NAME = 'African Artisan Market'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026
CLOSURE_START_DATE = '2026-06-01'
CLOSURE_END_DATE = '2026-06-30'
CLOSURE_MESSAGE = 'Closed.'
SCHEDULE_START_DATE = '2026-06-01'
SCHEDULE_END_DATE = '2026-06-30'
SCHEDULE_MESSAGE = 'Schedule.'


def _sample_gift_shop() -> GiftShop:
   return GiftShop(
      name=GIFT_SHOP_NAME,
      location='Africa',
      likelihood=100,
      is_closed=False )


def _weekly_schedule_body() -> dict[ str, object ]:
   return {
      'giftShop': GIFT_SHOP_NAME,
      'scheduleStartDate': SCHEDULE_START_DATE,
      'scheduleEndDate': SCHEDULE_END_DATE,
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
      'holidaysOnly': False,
      'message': SCHEDULE_MESSAGE,
   }


def _weekly_schedule_call() -> dict[ str, object ]:
   return {
      'gift_shop': GIFT_SHOP_NAME,
      'start_date': SCHEDULE_START_DATE,
      'end_date': SCHEDULE_END_DATE,
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
      'holidays_only': False,
      'message': SCHEDULE_MESSAGE,
   }


@pytest.fixture
def stub_gift_shop_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubGiftShopCoordinator:
   StubGiftShopCoordinator.instances = []
   StubGiftShopCoordinator.default_success = True
   stub = StubGiftShopCoordinator(
      gift_shop_names=[ GIFT_SHOP_NAME, OTHER_GIFT_SHOP_NAME ],
      gift_shops=[ _sample_gift_shop() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubGiftShopCoordinator.instances:
         StubGiftShopCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, GiftShopCoordinator, stub )

   return stub


def Test_GetGiftShops_TestHttpRequest_ExpectMapsVisitDateAndReturnsGiftShops(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler(
      '/get-gift-shops',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
         'includeClosedGiftShops': True,
         'giftShopsToInclude': [ GIFT_SHOP_NAME ],
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'gift_shops' ] == [ _sample_gift_shop().to_dict() ]
   assert stub_gift_shop_coordinator.calls == [
      (
         'get_gift_shops',
         {
            'day': VISIT_DAY,
            'month': VISIT_MONTH,
            'year': VISIT_YEAR,
            'include_closed_gift_shops': True,
            'gift_shops_to_include': [ GIFT_SHOP_NAME ],
         }
      )
   ]


def Test_GetGiftShopNames_TestDirectCall_ExpectWritesGiftShopNamesFromCoordinator(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = JsonHandlerTestDouble()

   GiftShopController.get_gift_shop_names( handler )

   assert handler.statuses == [ 200 ]
   assert handler.json_response() == {
      'gift_shops': [ GIFT_SHOP_NAME, OTHER_GIFT_SHOP_NAME ],
   }


def Test_SetGiftShopClosed_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler(
      '/set-gift-shop-closed',
      {
         'giftShop': GIFT_SHOP_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_gift_shop_coordinator.calls == [
      (
         'set_gift_shop_as_closed',
         {
            'gift_shop': GIFT_SHOP_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'gift_shop' ] == GIFT_SHOP_NAME


def Test_SetGiftShopClosed_TestHttpRequest_ExpectCouldNotSetClosedApiError(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   StubGiftShopCoordinator.default_success = False
   handler = make_handler( '/set-gift-shop-closed', { 'giftShop': GIFT_SHOP_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetClosed'


def Test_SetGiftShopClosureOverride_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler(
      '/set-gift-shop-closure-override',
      {
         'giftShop': GIFT_SHOP_NAME,
         'startDate': CLOSURE_START_DATE,
         'endDate': CLOSURE_END_DATE,
         'message': CLOSURE_MESSAGE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_gift_shop_coordinator.calls == [
      (
         'set_gift_shop_closure_override',
         {
            'gift_shop': GIFT_SHOP_NAME,
            'start_date': CLOSURE_START_DATE,
            'end_date': CLOSURE_END_DATE,
            'message': CLOSURE_MESSAGE,
         }
      )
   ]
   assert result[ 'success' ] is True


def Test_SetGiftShopClosureOverride_TestHttpRequest_ExpectCouldNotCreateClosureOverrideApiError(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   StubGiftShopCoordinator.default_success = False
   handler = make_handler(
      '/set-gift-shop-closure-override',
      { 'giftShop': GIFT_SHOP_NAME }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotCreateClosureOverride'


def Test_SetGiftShopOpeningSchedule_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler( '/set-gift-shop-opening-schedule', _weekly_schedule_body() )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_gift_shop_coordinator.calls == [
      ( 'set_gift_shop_opening_schedule', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_SetGiftShopOpeningSchedule_TestHttpRequest_ExpectOverlappingScheduleApiError(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   StubGiftShopCoordinator.default_success = False
   handler = make_handler( '/set-gift-shop-opening-schedule', _weekly_schedule_body() )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotSetOpeningSchedule'
   assert result[ 'errorType' ] == 'overlappingSchedule'


def Test_ReplaceGiftShopOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler(
      '/replace-gift-shop-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_gift_shop_coordinator.calls == [
      ( 'replace_gift_shop_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_ReplaceGiftShopOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotReplaceApiError(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   StubGiftShopCoordinator.default_success = False
   handler = make_handler(
      '/replace-gift-shop-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotReplaceOpeningScheduleOverlaps'


def Test_TrimGiftShopOpeningScheduleOverlaps_TestHttpRequest_ExpectMapsPayload(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   handler = make_handler(
      '/trim-gift-shop-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_gift_shop_coordinator.calls == [
      ( 'trim_gift_shop_opening_schedule_overlaps', _weekly_schedule_call() )
   ]
   assert result[ 'success' ] is True


def Test_TrimGiftShopOpeningScheduleOverlaps_TestHttpRequest_ExpectCouldNotTrimApiError(
      stub_gift_shop_coordinator: StubGiftShopCoordinator ) -> None:
   StubGiftShopCoordinator.default_success = False
   handler = make_handler(
      '/trim-gift-shop-opening-schedule-overlaps',
      _weekly_schedule_body()
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotTrimOpeningScheduleOverlaps'
