from __future__ import annotations

from datetime import date

import pytest

from api.giftshops.coordinators import gift_shop_coordinator as gift_shop_coordinator_module
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop_provider import GiftShopProvider
from api.giftshops.domain.gift_shop_builder import GiftShopBuilder
from api.giftshops.search.gift_shops_matching_query_builder import GiftShopsMatchingQueryBuilder
from api.models.gift_shop import GiftShop
from api.types import Types

VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
GIFT_SHOP_NAME = 'Zoo Shop'
QUERY = 'shop'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for maintenance.'

GIFT_SHOP = GiftShop(
   name=GIFT_SHOP_NAME,
   location='Main Entrance' )


def Test_GetGiftShopNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GiftShopProvider,
      'fetch_gift_shop_names',
      lambda _conn: [ GIFT_SHOP_NAME ] )

   assert GiftShopCoordinator.get_gift_shop_names() == [ GIFT_SHOP_NAME ]


def Test_GetGiftShops_TestProvidersAndBuilder_ExpectGiftShops(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   gift_shop_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   class _Context:
      normalized_month = 6
      normalized_day = 15
      target_date = VISIT_DATE

   monkeypatch.setattr(
      GiftShopBuilder,
      'resolve_context',
      lambda **_kwargs: _Context() )
   monkeypatch.setattr(
      GiftShopProvider,
      'fetch_gift_shop_records',
      lambda _conn, *, month, day: gift_shop_records if month == 6 and day == 15 else [] )
   monkeypatch.setattr(
      GiftShopProvider,
      'fetch_gift_shop_schedule_records',
      lambda _conn: schedule_records )
   monkeypatch.setattr(
      GiftShopProvider,
      'fetch_gift_shop_schedule_override_records',
      lambda _conn: override_records )

   def build_gift_shops( **kwargs: object ) -> list[ GiftShop ]:
      captured.update( kwargs )
      return [ GIFT_SHOP ]

   monkeypatch.setattr( GiftShopBuilder, 'build_gift_shops', build_gift_shops )

   assert GiftShopCoordinator.get_gift_shops(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_gift_shops=True ) == [ GIFT_SHOP ]
   assert captured[ 'gift_shop_records' ] is gift_shop_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_gift_shops' ] is True


def Test_GetGiftShopsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   gift_shops = [ GIFT_SHOP ]
   captured: dict[ str, object ] = {}

   def get_gift_shops( **kwargs: object ) -> list[ GiftShop ]:
      captured.update( kwargs )
      return gift_shops

   monkeypatch.setattr( GiftShopCoordinator, 'get_gift_shops', get_gift_shops )
   monkeypatch.setattr(
      GiftShopsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   assert GiftShopCoordinator.get_gift_shops_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == gift_shops
   assert captured[ 'include_closed_gift_shops' ] is True


def Test_SetGiftShopAsClosed_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_as_closed(
            self,
            name: str,
            start_date: Types.DateInput,
            end_date: Types.DateInput,
            message: str ) -> bool:
         captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

   monkeypatch.setattr( gift_shop_coordinator_module, '_mutations', StubMutations() )

   assert GiftShopCoordinator.set_gift_shop_as_closed(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( GIFT_SHOP_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetGiftShopClosureOverride_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_closure_override(
            self,
            name: str,
            start_date: Types.DateInput,
            end_date: Types.DateInput,
            message: str ) -> bool:
         captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

   monkeypatch.setattr( gift_shop_coordinator_module, '_mutations', StubMutations() )

   assert GiftShopCoordinator.set_gift_shop_closure_override(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( GIFT_SHOP_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetGiftShopOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_opening_schedule( self, *args: object ) -> bool:
         captured[ 'args' ] = args
         return True

   monkeypatch.setattr( gift_shop_coordinator_module, '_mutations', StubMutations() )

   assert GiftShopCoordinator.set_gift_shop_opening_schedule(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE ) is True
   assert captured[ 'args' ] == (
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE )


def Test_ReplaceGiftShopOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   class StubMutations:
      def replace_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == GIFT_SHOP_NAME

   monkeypatch.setattr( gift_shop_coordinator_module, '_mutations', StubMutations() )

   assert GiftShopCoordinator.replace_gift_shop_opening_schedule_overlaps(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE ) is True


def Test_TrimGiftShopOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   class StubMutations:
      def trim_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == GIFT_SHOP_NAME

   monkeypatch.setattr( gift_shop_coordinator_module, '_mutations', StubMutations() )

   assert GiftShopCoordinator.trim_gift_shop_opening_schedule_overlaps(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE ) is True
