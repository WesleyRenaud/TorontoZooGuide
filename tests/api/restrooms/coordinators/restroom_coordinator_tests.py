from __future__ import annotations

import pytest

from api.models.date_range import DateRange
from api.models.restroom import Restroom
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.restrooms.data_access.restroom_alert_provider import RestroomAlertProvider
from api.restrooms.data_access.restroom_provider import RestroomProvider
from api.restrooms.data_access.restroom_status_provider import RestroomStatusProvider
from api.restrooms.domain.restroom_builder import RestroomBuilder
from api.restrooms.domain.restroom_context_builder import RestroomContextBuilder
from api.restrooms.search.restrooms_matching_query_builder import RestroomsMatchingQueryBuilder
from api.restrooms.status.restroom_alert import RestroomAlert
from api.restrooms.status.restroom_alert_builder import RestroomAlertBuilder
from api.restrooms.status.restroom_closed_status import RestroomClosedStatus
from api.restrooms.status.restroom_status_builder import RestroomStatusBuilder
from api.shared.calendar_dates import DateValues
from api.types import Types

VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
RESTROOM_TITLE = 'Africa Savanna Restroom'
QUERY = 'africa'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for cleaning.'

RESTROOM = Restroom( title=RESTROOM_TITLE )
CLOSED_STATUS = RestroomClosedStatus(
   restroom=RESTROOM_TITLE,
   start_date=START_DATE,
   end_date=END_DATE,
   message=MESSAGE )
ALERT = RestroomAlert(
   restroom=RESTROOM_TITLE,
   start_date=START_DATE,
   end_date=END_DATE,
   message=MESSAGE )
DATE_RANGE = DateRange(
   start_date=START_DATE,
   end_date=END_DATE )

def Test_GetRestroomNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      RestroomProvider,
      'fetch_restroom_names',
      lambda _conn: [ RESTROOM_TITLE ] )

   assert RestroomCoordinator.get_restroom_names() == [ RESTROOM_TITLE ]

def Test_GetRestrooms_TestProvidersAndBuilder_ExpectRestrooms(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restroom_records = [ object() ]
   context = object()
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      RestroomProvider,
      'fetch_restroom_records',
      lambda _conn: restroom_records )
   monkeypatch.setattr(
      RestroomContextBuilder,
      'resolve',
      lambda **_kwargs: context )

   def build_restrooms( **kwargs: object ) -> list[ Restroom ]:
      captured.update( kwargs )
      return [ RESTROOM ]

   monkeypatch.setattr( RestroomBuilder, 'build_restrooms', build_restrooms )

   assert RestroomCoordinator.get_restrooms(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restrooms=True ) == [ RESTROOM ]
   assert captured[ 'restroom_records' ] is restroom_records
   assert captured[ 'context' ] is context
   assert captured[ 'include_closed_restrooms' ] is True

def Test_GetRestroomsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restrooms = [ RESTROOM ]

   monkeypatch.setattr(
      RestroomCoordinator,
      'get_restrooms',
      lambda **_kwargs: restrooms )
   monkeypatch.setattr(
      RestroomsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   assert RestroomCoordinator.get_restrooms_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_restrooms=False ) == restrooms

def Test_SetRestroomAsClosed_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      RestroomStatusBuilder,
      'build_closed_status',
      lambda **_kwargs: CLOSED_STATUS )

   def save_closed_status(
         _conn: Types.Connection,
         *,
         restroom: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      captured[ 'args' ] = ( restroom, start_date, end_date, message )
      return True

   monkeypatch.setattr( RestroomStatusProvider, 'save_closed_status', save_closed_status )

   assert RestroomCoordinator.set_restroom_as_closed(
      RESTROOM_TITLE,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( RESTROOM_TITLE, START_DATE, END_DATE, MESSAGE )

def Test_SetRestroomAsOpen_TestProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      DateValues,
      'resolve_open_ended_date_range',
      lambda **_kwargs: DATE_RANGE )

   def save_open_status(
         _conn: Types.Connection,
         *,
         restroom: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      captured[ 'args' ] = ( restroom, start_date, end_date )
      return True

   monkeypatch.setattr( RestroomStatusProvider, 'save_open_status', save_open_status )

   assert RestroomCoordinator.set_restroom_as_open(
      RESTROOM_TITLE,
      START_DATE,
      END_DATE ) is True
   assert captured[ 'args' ] == ( RESTROOM_TITLE, START_DATE, END_DATE )

def Test_SetRestroomAlert_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      RestroomAlertBuilder,
      'build_alert',
      lambda **_kwargs: ALERT )

   def save_alert(
         _conn: Types.Connection,
         *,
         restroom: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      captured[ 'args' ] = ( restroom, alert_start_date, alert_end_date, message )
      return True

   monkeypatch.setattr( RestroomAlertProvider, 'save_alert', save_alert )

   assert RestroomCoordinator.set_restroom_alert(
      RESTROOM_TITLE,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( RESTROOM_TITLE, START_DATE, END_DATE, MESSAGE )

def Test_RemoveRestroomAlert_TestProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def delete_alert( _conn: Types.Connection, *, restroom: str ) -> bool:
      captured[ 'restroom' ] = restroom
      return True

   monkeypatch.setattr( RestroomAlertProvider, 'delete_alert', delete_alert )

   assert RestroomCoordinator.remove_restroom_alert( RESTROOM_TITLE ) is True
   assert captured[ 'restroom' ] == RESTROOM_TITLE
