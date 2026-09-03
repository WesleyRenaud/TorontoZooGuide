from __future__ import annotations

from datetime import date

import pytest

from api.models.restaurant import Restaurant
from api.restaurants.coordinators import restaurant_coordinator as restaurant_coordinator_module
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restaurants.data_access.restaurant_provider import RestaurantProvider
from api.restaurants.domain.restaurant_builder import RestaurantBuilder
from api.restaurants.search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder
from api.types import Types

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

def Test_GetRestaurantNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RestaurantProvider,
      'fetch_restaurant_names',
      lambda _conn: [ RESTAURANT_NAME ] )

   assert RestaurantCoordinator.get_restaurant_names() == [ RESTAURANT_NAME ]

def Test_GetRestaurants_TestProvidersAndBuilder_ExpectRestaurants(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restaurant_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   class _Context:
      normalized_month = 6
      normalized_day = 15
      target_date = VISIT_DATE

   monkeypatch.setattr(
      RestaurantBuilder,
      'resolve_context',
      lambda **_kwargs: _Context() )
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

   def build_restaurants( **kwargs: object ) -> list[ Restaurant ]:
      captured.update( kwargs )
      return [ RESTAURANT ]

   monkeypatch.setattr( RestaurantBuilder, 'build_restaurants', build_restaurants )

   assert RestaurantCoordinator.get_restaurants(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restaurants=True ) == [ RESTAURANT ]
   assert captured[ 'restaurant_records' ] is restaurant_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_restaurants' ] is True

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

   assert RestaurantCoordinator.get_restaurants_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restaurants=False ) == restaurants

def Test_SetRestaurantAsClosed_TestMutations_ExpectDelegated(
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

   monkeypatch.setattr( restaurant_coordinator_module, '_mutations', StubMutations() )

   assert RestaurantCoordinator.set_restaurant_as_closed(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( RESTAURANT_NAME, START_DATE, END_DATE, MESSAGE )

def Test_SetRestaurantClosureOverride_TestMutations_ExpectDelegated(
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

   monkeypatch.setattr( restaurant_coordinator_module, '_mutations', StubMutations() )

   assert RestaurantCoordinator.set_restaurant_closure_override(
      RESTAURANT_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( RESTAURANT_NAME, START_DATE, END_DATE, MESSAGE )

def Test_SetRestaurantOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_opening_schedule( self, *args: object ) -> bool:
         captured[ 'args' ] = args
         return True

   monkeypatch.setattr( restaurant_coordinator_module, '_mutations', StubMutations() )

   assert RestaurantCoordinator.set_restaurant_opening_schedule(
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
      MESSAGE ) is True
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
   class StubMutations:
      def replace_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == RESTAURANT_NAME

   monkeypatch.setattr( restaurant_coordinator_module, '_mutations', StubMutations() )

   assert RestaurantCoordinator.replace_restaurant_opening_schedule_overlaps(
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
      MESSAGE ) is True

def Test_TrimRestaurantOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   class StubMutations:
      def trim_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == RESTAURANT_NAME

   monkeypatch.setattr( restaurant_coordinator_module, '_mutations', StubMutations() )

   assert RestaurantCoordinator.trim_restaurant_opening_schedule_overlaps(
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
      MESSAGE ) is True
