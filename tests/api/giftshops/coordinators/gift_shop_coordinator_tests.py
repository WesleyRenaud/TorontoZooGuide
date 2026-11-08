from __future__ import annotations

from datetime import date

import pytest

from api.giftshops.coordinators import gift_shop_coordinator as gift_shop_coordinator_module
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.data_access.gift_shop_closure_record import GiftShopClosureRecord
from api.giftshops.data_access.gift_shop_provider import GiftShopProvider
from api.giftshops.data_access.gift_shop_status_provider import GiftShopStatusProvider
from api.giftshops.domain.gift_shop_builder import GiftShopBuilder
from api.giftshops.domain.seasonal_gift_shop import SeasonalGiftShop
from api.giftshops.domain.seasonal_gift_shop_builder import SeasonalGiftShopBuilder
from api.giftshops.search.gift_shops_matching_query_builder import GiftShopsMatchingQueryBuilder
from api.giftshops.status.gift_shop_season_closure_builder import GiftShopSeasonClosureBuilder
from api.models.gift_shop import GiftShop
from api.shared.calendar_dates import DateValues


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


class _Mutations:
   def __init__(
         self,
         captured: dict[ str, object ] | None = None,
         name: str | None = None ) -> None:
      self.captured = captured
      self.name = name


   def set_as_closed(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      return self._closed( name, start_date, end_date, message )


   def set_closure_override(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      return self._closed( name, start_date, end_date, message )


   def set_opening_schedule(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   def replace_opening_schedule_overlaps(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   def trim_opening_schedule_overlaps(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   def _closed(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      if self.captured != None:
         self.captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

      return name == self.name


   def _opening(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      if self.captured != None:
         self.captured[ 'args' ] = (
            name,
            start_date,
            end_date,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            holidays_only,
            message )
         return True

      return name == self.name


class _GiftShopContext:
   normalized_month = 6
   normalized_day = 15
   target_date = VISIT_DATE


class _GiftShopSeasonStatus:
   gift_shop = GIFT_SHOP_NAME
   start_date = START_DATE
   end_date = END_DATE
   message = MESSAGE


def Test_GetGiftShopNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GiftShopProvider,
      'fetch_gift_shop_names',
      lambda _conn: [ GIFT_SHOP_NAME ] )

   gift_shop_names = GiftShopCoordinator.get_gift_shop_names()

   assert gift_shop_names == [ GIFT_SHOP_NAME ]


def Test_GetGiftShops_TestProvidersAndBuilder_ExpectGiftShops(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   gift_shop_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      GiftShopBuilder,
      'resolve_context',
      lambda **_kwargs: _GiftShopContext() )
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
   monkeypatch.setattr(
      GiftShopStatusProvider,
      'fetch_closure_records',
      lambda _conn: [] )

   def build_gift_shops( **kwargs: object ) -> list[ GiftShop ]:
      captured.update( kwargs )
      return [ GIFT_SHOP ]

   monkeypatch.setattr( GiftShopBuilder, 'build_gift_shops', build_gift_shops )

   gift_shops = GiftShopCoordinator.get_gift_shops(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_gift_shops=True )

   assert gift_shops == [ GIFT_SHOP ]
   assert captured[ 'gift_shop_records' ] is gift_shop_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_gift_shops' ] is True
   assert captured[ 'closure_records' ] == []


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

   gift_shops_matching_query = GiftShopCoordinator.get_gift_shops_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   assert gift_shops_matching_query == gift_shops
   assert captured[ 'include_closed_gift_shops' ] is True


def Test_SetGiftShopAsClosed_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      gift_shop_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = GiftShopCoordinator.set_gift_shop_as_closed(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( GIFT_SHOP_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetGiftShopClosureOverride_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      gift_shop_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = GiftShopCoordinator.set_gift_shop_closure_override(
      GIFT_SHOP_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( GIFT_SHOP_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetGiftShopOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      gift_shop_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = GiftShopCoordinator.set_gift_shop_opening_schedule(
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

   assert result is True
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
   monkeypatch.setattr(
      gift_shop_coordinator_module,
      '_mutations',
      _Mutations( name=GIFT_SHOP_NAME ) )

   result = GiftShopCoordinator.replace_gift_shop_opening_schedule_overlaps(
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

   assert result is True


def Test_TrimGiftShopOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      gift_shop_coordinator_module,
      '_mutations',
      _Mutations( name=GIFT_SHOP_NAME ) )

   result = GiftShopCoordinator.trim_gift_shop_opening_schedule_overlaps(
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

   assert result is True


def Test_GetClosedForSeasonGiftShopNames_TestProvider_ExpectNames(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( DateValues, 'today_date_key', lambda: '2026-11-02' )
   monkeypatch.setattr(
      GiftShopStatusProvider,
      'fetch_closed_for_season_names',
      lambda _conn, *, today: [ GIFT_SHOP_NAME ] if today == '2026-11-02' else [] )

   names = GiftShopCoordinator.get_closed_for_season_gift_shop_names()

   assert names == [ GIFT_SHOP_NAME ]


def Test_SetGiftShopAsClosedForSeason_TestBuilderAndProvider_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def build( **kwargs: object ) -> _GiftShopSeasonStatus:
      captured[ 'built' ] = kwargs
      return _GiftShopSeasonStatus()

   def save( _conn: str, **kwargs: object ) -> bool:
      captured[ 'saved' ] = kwargs
      return True

   monkeypatch.setattr( GiftShopSeasonClosureBuilder, 'build', build )
   monkeypatch.setattr( GiftShopStatusProvider, 'save_closed_for_season', save )

   result = GiftShopCoordinator.set_gift_shop_as_closed_for_season(
      gift_shop=GIFT_SHOP_NAME,
      start_date=None,
      end_date=None,
      message='' )

   assert result is True
   assert captured[ 'built' ] == {
      'gift_shop': GIFT_SHOP_NAME,
      'start_date': None,
      'end_date': None,
      'message': '',
   }
   assert captured[ 'saved' ] == {
      'gift_shop': GIFT_SHOP_NAME,
      'start_date': START_DATE,
      'end_date': END_DATE,
      'message': MESSAGE,
   }


def Test_SetGiftShopAsOpenForSeason_TestProvider_ExpectDeleted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GiftShopStatusProvider,
      'delete_closed_for_season',
      lambda _conn, *, gift_shop: gift_shop == GIFT_SHOP_NAME )

   result = GiftShopCoordinator.set_gift_shop_as_open_for_season( GIFT_SHOP_NAME )

   assert result is True


def Test_GetClosureRecords_TestProvider_ExpectRecords(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   closure_record = GiftShopClosureRecord(
      gift_shop=GIFT_SHOP_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True )

   monkeypatch.setattr(
      GiftShopStatusProvider,
      'fetch_closure_records',
      lambda _conn: [ closure_record ] )

   records = GiftShopCoordinator.get_closure_records()

   assert records == [ closure_record ]


def Test_GetSeasonalGiftShops_TestClosures_ExpectBuiltGiftShops(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   gift_shops = [ GIFT_SHOP_NAME ]
   closure_records = [ GiftShopClosureRecord(
      gift_shop=GIFT_SHOP_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True,
   ) ]
   built = [ SeasonalGiftShop(
      name=GIFT_SHOP_NAME,
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   ) ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr( GiftShopCoordinator, 'get_gift_shop_names', lambda: gift_shops )
   monkeypatch.setattr( GiftShopCoordinator, 'get_closure_records', lambda: closure_records )

   def build( **kwargs: object ) -> list[ SeasonalGiftShop ]:
      captured.update( kwargs )
      return built

   monkeypatch.setattr( SeasonalGiftShopBuilder, 'build', build )

   result = GiftShopCoordinator.get_seasonal_gift_shops()

   assert result is built
   assert captured[ 'gift_shops' ] is gift_shops
   assert captured[ 'closure_records' ] is closure_records
