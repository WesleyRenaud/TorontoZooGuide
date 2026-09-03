from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pytest

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.exhibits.data_access.exhibit_provider import ExhibitProvider
from api.exhibits.data_access.exhibit_status_provider import ExhibitStatusProvider
from api.exhibits.domain.region_options_builder import RegionOptionsBuilder
from api.exhibits.domain.regions_with_exhibits_builder import RegionsWithExhibitsBuilder
from api.exhibits.status.exhibit_closed_status import ExhibitClosedStatus
from api.exhibits.status.exhibit_status_builder import ExhibitStatusBuilder
from api.models.date_range import DateRange
from api.models.region import Region
from api.models.region_with_exhibits import RegionWithExhibits
from api.shared.calendar_dates import CalendarDates
from api.shared.calendar_dates import DateValues
from api.types import Types

VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
REGION_NAME = 'Africa'
EXHIBIT_NAME = 'Africa Savanna'
ANIMAL_NAME = 'African Lion'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for habitat work.'

REGION = Region( name=REGION_NAME, has_exhibits=True )
REGION_WITH_EXHIBITS = RegionWithExhibits(
   name=REGION_NAME,
   exhibits=[ EXHIBIT_NAME ] )
CLOSED_STATUS = ExhibitClosedStatus(
   exhibit=EXHIBIT_NAME,
   start_date=START_DATE,
   end_date=END_DATE,
   message=MESSAGE )
DATE_RANGE = DateRange(
   start_date=START_DATE,
   end_date=END_DATE )


@dataclass
class StubClosureRecord():
   pass


def Test_GetExhibitsInRegion_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ExhibitProvider,
      'fetch_exhibit_names_in_region',
      lambda _conn, *, region: [ EXHIBIT_NAME ] if region == REGION_NAME else [] )

   assert ExhibitCoordinator.get_exhibits_in_region( REGION_NAME ) == [ EXHIBIT_NAME ]


def Test_GetExhibits_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ExhibitProvider,
      'fetch_exhibit_names',
      lambda _conn: [ EXHIBIT_NAME ] )

   assert ExhibitCoordinator.get_exhibits() == [ EXHIBIT_NAME ]


def Test_GetRegions_TestProviderAndBuilder_ExpectRegions(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   region_rows = [ object() ]

   monkeypatch.setattr(
      ExhibitProvider,
      'fetch_region_exhibit_rows',
      lambda _conn: region_rows )
   monkeypatch.setattr(
      RegionOptionsBuilder,
      'build',
      lambda rows: [ REGION ] if rows is region_rows else [] )

   assert ExhibitCoordinator.get_regions() == [ REGION ]


def Test_GetRegionsWithExhibits_TestProviderAndBuilder_ExpectRegions(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   region_rows = [ object() ]

   monkeypatch.setattr(
      ExhibitProvider,
      'fetch_region_exhibit_rows',
      lambda _conn: region_rows )
   monkeypatch.setattr(
      RegionsWithExhibitsBuilder,
      'build',
      lambda rows: [ REGION_WITH_EXHIBITS ] if rows is region_rows else [] )

   assert ExhibitCoordinator.get_regions_with_exhibits() == [ REGION_WITH_EXHIBITS ]


def Test_GetNamesOfAnimalsInExhibit_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ExhibitProvider,
      'fetch_animal_names_in_exhibit',
      lambda _conn, *, exhibit: [ ANIMAL_NAME ] if exhibit == EXHIBIT_NAME else [] )

   assert ExhibitCoordinator.get_names_of_animals_in_exhibit( EXHIBIT_NAME ) == [ ANIMAL_NAME ]


def Test_GetClosedExhibitsForVisitDate_TestProviderAndBuilder_ExpectNames(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   closure_records = [ StubClosureRecord() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      CalendarDates,
      'visit_target_date',
      lambda **_kwargs: VISIT_DATE )
   monkeypatch.setattr(
      ExhibitStatusProvider,
      'fetch_closure_records',
      lambda _conn: closure_records )

   def exhibit_names_closed_on_visit_date(
         records: list[ StubClosureRecord ],
         target_date: date ) -> list[ str ]:
      captured[ 'records' ] = records
      captured[ 'target_date' ] = target_date
      return [ EXHIBIT_NAME ]

   monkeypatch.setattr(
      ExhibitStatusBuilder,
      'exhibit_names_closed_on_visit_date',
      exhibit_names_closed_on_visit_date )

   assert ExhibitCoordinator.get_closed_exhibits_for_visit_date(
      month=VISIT_MONTH,
      day=VISIT_DAY,
      year=VISIT_YEAR ) == [ EXHIBIT_NAME ]
   assert captured[ 'records' ] is closure_records
   assert captured[ 'target_date' ] == VISIT_DATE


def Test_SetExhibitAsClosed_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      ExhibitStatusBuilder,
      'build_closed_status',
      lambda **_kwargs: CLOSED_STATUS )

   def save_closed_status(
         _conn: Types.Connection,
         *,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      captured[ 'args' ] = ( exhibit, start_date, end_date, message )
      return True

   monkeypatch.setattr( ExhibitStatusProvider, 'save_closed_status', save_closed_status )

   assert ExhibitCoordinator.set_exhibit_as_closed(
      EXHIBIT_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( EXHIBIT_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetExhibitAsOpen_TestProvider_ExpectDelegated(
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
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      captured[ 'args' ] = ( exhibit, start_date, end_date )
      return True

   monkeypatch.setattr( ExhibitStatusProvider, 'save_open_status', save_open_status )

   assert ExhibitCoordinator.set_exhibit_as_open(
      EXHIBIT_NAME,
      START_DATE,
      END_DATE ) is True
   assert captured[ 'args' ] == ( EXHIBIT_NAME, START_DATE, END_DATE )
