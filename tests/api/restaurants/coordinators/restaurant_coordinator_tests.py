from __future__ import annotations

from datetime import date

import pytest

from api.models.restaurant import Restaurant
from api.restaurants.coordinators import restaurant_coordinator as restaurant_coordinator_module
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant_closure_record import RestaurantClosureRecord
from api.restaurants.data_access.restaurant_provider import RestaurantProvider
from api.restaurants.data_access.restaurant_status_provider import RestaurantStatusProvider
from api.restaurants.domain.restaurant_builder import RestaurantBuilder
from api.restaurants.domain.restaurant_menu_link import RestaurantMenuLink
from api.restaurants.domain.seasonal_restaurant import SeasonalRestaurant
from api.restaurants.domain.seasonal_restaurant_builder import SeasonalRestaurantBuilder
from api.restaurants.search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder
from api.restaurants.status.restaurant_season_closure_builder import RestaurantSeasonClosureBuilder
from api.shared.calendar_dates import DateValues


VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
RESTAURANT_NAME = 'Simba Spot'
QUERY = 'simba'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for maintenance.'

RESTAURANT = Restaurant(
   name=RESTAURANT_NAME,
   location='African Savanna',
   sub_location='Near Lions' )


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


class _RestaurantContext:
   normalized_month = 6
   normalized_day = 15
   target_date = VISIT_DATE


class _RestaurantSeasonStatus:
   restaurant = RESTAURANT_NAME
   start_date = START_DATE
   end_date = END_DATE
   message = MESSAGE


def Test_GetRestaurantNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_names',
      lambda _conn: [ RESTAURANT_NAME ] )

   restaurant_names = RestaurantCoordinator.get_restaurant_names()

   assert restaurant_names == [ RESTAURANT_NAME ]


def Test_GetRestaurantMenuLinks_TestProvider_ExpectLinks(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   links = [ RestaurantMenuLink( name=RESTAURANT_NAME, menu_link='https://example.test/menu' ) ]

   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_menu_links',
      lambda _conn: links )

   result = RestaurantCoordinator.get_restaurant_menu_links()

   assert result is links


def Test_GetRestaurants_TestProvidersAndBuilder_ExpectRestaurants(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restaurant_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      RestaurantBuilder,
      'resolve_context',
      lambda **_kwargs: _RestaurantContext() )
   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_records',
      lambda _conn, *, month, day: restaurant_records if month == 6 and day == 15 else [] )
   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_schedule_records',
      lambda _conn: schedule_records )
   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_schedule_override_records',
      lambda _conn: override_records )
   monkeypatch.setattr(
      RestaurantStatusProvider,
      'fetch_closure_records',
      lambda _conn: [] )

   def build_restaurants( **kwargs: object ) -> list[ Restaurant ]:
      captured.update( kwargs )
      return [ RESTAURANT ]

   monkeypatch.setattr( RestaurantBuilder, 'build_restaurants', build_restaurants )

   restaurants = RestaurantCoordinator.get_restaurants(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restaurants=True )

   assert restaurants == [ RESTAURANT ]
   assert captured[ 'restaurant_records' ] is restaurant_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_restaurants' ] is True
   assert captured[ 'closure_records' ] == []


def Test_GetRestaurantsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restaurants = [ RESTAURANT ]

   monkeypatch.setattr(
      RestaurantCoordinator,
      'get_restaurants',
      lambda **_kwargs: restaurants )
   monkeypatch.setattr(
      RestaurantsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   restaurants_matching_query = RestaurantCoordinator.get_restaurants_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restaurants=False )

   assert restaurants_matching_query == restaurants


def Test_SetRestaurantAsClosed_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      restaurant_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = RestaurantCoordinator.set_restaurant_as_closed(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( RESTAURANT_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetRestaurantClosureOverride_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      restaurant_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = RestaurantCoordinator.set_restaurant_closure_override(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( RESTAURANT_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetRestaurantOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      restaurant_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = RestaurantCoordinator.set_restaurant_opening_schedule(
      RESTAURANT_NAME,
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
      RESTAURANT_NAME,
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


def Test_ReplaceRestaurantOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      restaurant_coordinator_module,
      '_mutations',
      _Mutations( name=RESTAURANT_NAME ) )

   result = RestaurantCoordinator.replace_restaurant_opening_schedule_overlaps(
      RESTAURANT_NAME,
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


def Test_TrimRestaurantOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      restaurant_coordinator_module,
      '_mutations',
      _Mutations( name=RESTAURANT_NAME ) )

   result = RestaurantCoordinator.trim_restaurant_opening_schedule_overlaps(
      RESTAURANT_NAME,
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


def Test_GetClosureRecords_TestProvider_ExpectRecords(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   closure_record = RestaurantClosureRecord(
      restaurant=RESTAURANT_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True )

   monkeypatch.setattr(
      RestaurantStatusProvider,
      'fetch_closure_records',
      lambda _conn: [ closure_record ] )

   records = RestaurantCoordinator.get_closure_records()

   assert records == [ closure_record ]


def Test_GetSeasonalRestaurants_TestClosures_ExpectBuiltRestaurants(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restaurants = [ RestaurantMenuLink( name=RESTAURANT_NAME, menu_link='https://example.test/menu' ) ]
   closure_records = [ RestaurantClosureRecord(
      restaurant=RESTAURANT_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True,
   ) ]
   built = [ SeasonalRestaurant(
      name=RESTAURANT_NAME,
      menu_link='https://example.test/menu',
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   ) ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr( RestaurantCoordinator, 'get_restaurant_menu_links', lambda: restaurants )
   monkeypatch.setattr( RestaurantCoordinator, 'get_closure_records', lambda: closure_records )

   def build( **kwargs: object ) -> list[ SeasonalRestaurant ]:
      captured.update( kwargs )
      return built

   monkeypatch.setattr( SeasonalRestaurantBuilder, 'build', build )

   result = RestaurantCoordinator.get_seasonal_restaurants()

   assert result is built
   assert captured[ 'restaurants' ] is restaurants
   assert captured[ 'closure_records' ] is closure_records


def Test_GetClosedForSeasonRestaurantNames_TestProvider_ExpectNames(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( DateValues, 'today_date_key', lambda: '2026-11-02' )
   monkeypatch.setattr(
      RestaurantStatusProvider,
      'fetch_closed_for_season_names',
      lambda _conn, *, today: [ RESTAURANT_NAME ] if today == '2026-11-02' else [] )

   names = RestaurantCoordinator.get_closed_for_season_restaurant_names()

   assert names == [ RESTAURANT_NAME ]


def Test_SetRestaurantAsClosedForSeason_TestBuilderAndProvider_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def build( **kwargs: object ) -> _RestaurantSeasonStatus:
      captured[ 'built' ] = kwargs
      return _RestaurantSeasonStatus()

   def save( _conn: str, **kwargs: object ) -> bool:
      captured[ 'saved' ] = kwargs
      return True

   monkeypatch.setattr( RestaurantSeasonClosureBuilder, 'build', build )
   monkeypatch.setattr( RestaurantStatusProvider, 'save_closed_for_season', save )

   result = RestaurantCoordinator.set_restaurant_as_closed_for_season(
      restaurant=RESTAURANT_NAME,
      start_date=None,
      end_date=None,
      message='' )

   assert result is True
   assert captured[ 'built' ] == {
      'restaurant': RESTAURANT_NAME,
      'start_date': None,
      'end_date': None,
      'message': '',
   }
   assert captured[ 'saved' ] == {
      'restaurant': RESTAURANT_NAME,
      'start_date': START_DATE,
      'end_date': END_DATE,
      'message': MESSAGE,
   }


def Test_SetRestaurantAsOpenForSeason_TestProvider_ExpectDeleted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RestaurantStatusProvider,
      'delete_closed_for_season',
      lambda _conn, *, restaurant: restaurant == RESTAURANT_NAME )

   result = RestaurantCoordinator.set_restaurant_as_open_for_season( RESTAURANT_NAME )

   assert result is True
