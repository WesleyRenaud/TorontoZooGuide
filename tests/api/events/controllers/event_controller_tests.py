from __future__ import annotations

from api_test_support.patch_coordinator import patch_coordinator_with_stub
from api_test_support.post_handler import make_handler
from api_test_support.post_handler import response_json
from api_test_support.stub_event_coordinator import StubEventCoordinator
import pytest

from api import database_connection_provider as connection
from api.events.controllers.event_controller import EventController
from api.events.coordinators.event_coordinator import EventCoordinator
import api.http_request_handler as server
from api.models.event import Event
import api.request_connection_provider as request_connection
from api.types import Types


EVENT_NAME = 'Conservation Carousel Ride Night'
EVENT_LOCATION = 'Front Courtyard'
EVENT_DESCRIPTION = 'Evening carousel rides for a special cause.'
EVENT_LINK = 'https://www.torontozoo.com/events/carousel-night'
START_DATE = '2026-06-15'
END_DATE = '2026-06-30'
VISIT_MONTH = 'June'
VISIT_DAY = 15
VISIT_YEAR = 2026


def _sample_event() -> Event:
   return Event(
      name=EVENT_NAME,
      location=EVENT_LOCATION,
      description=EVENT_DESCRIPTION,
      link=EVENT_LINK,
      start_date=START_DATE,
      end_date=END_DATE )


@pytest.fixture
def stub_event_coordinator( monkeypatch: pytest.MonkeyPatch ) -> StubEventCoordinator:
   StubEventCoordinator.instances = []
   StubEventCoordinator.default_success = True
   stub = StubEventCoordinator( events=[ _sample_event() ] )

   monkeypatch.setattr( connection.DatabaseConnectionProvider, 'open', lambda db_path='animals.db': None )

   def stub_set_connection( conn: Types.Connection | None ) -> None:
      return None

   def stub_clear_connection() -> None:
      if StubEventCoordinator.instances:
         StubEventCoordinator.instances[ -1 ].closed = True

   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'set', stub_set_connection )
   monkeypatch.setattr( request_connection.RequestConnectionProvider, 'clear', stub_clear_connection )
   patch_coordinator_with_stub( monkeypatch, EventCoordinator, stub )

   return stub


def Test_GetEvents_TestHttpRequest_ExpectMapsVisitDateAndReturnsEvents(
      stub_event_coordinator: StubEventCoordinator ) -> None:
   handler = make_handler(
      '/get-events',
      {
         'day': VISIT_DAY,
         'month': VISIT_MONTH,
         'year': VISIT_YEAR,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'events' ] == [ _sample_event().to_dict() ]


def Test_CreateEvent_TestHttpRequest_ExpectMapsPayloadAndSuccessResponse(
      stub_event_coordinator: StubEventCoordinator ) -> None:
   handler = make_handler(
      '/create-event',
      {
         'name': EVENT_NAME,
         'location': EVENT_LOCATION,
         'description': EVENT_DESCRIPTION,
         'link': EVENT_LINK,
         'startDate': START_DATE,
         'endDate': END_DATE,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert stub_event_coordinator.calls == [
      (
         'create_event',
         {
            'name': EVENT_NAME,
            'location': EVENT_LOCATION,
            'description': EVENT_DESCRIPTION,
            'link': EVENT_LINK,
            'start_date': START_DATE,
            'end_date': END_DATE,
         }
      )
   ]
   assert result[ 'success' ] is True
   assert result[ 'name' ] == EVENT_NAME
   assert result[ 'endDate' ] == END_DATE


def Test_CreateEvent_TestHttpRequest_ExpectOpenEndedDatesRetained(
      stub_event_coordinator: StubEventCoordinator ) -> None:
   handler = make_handler(
      '/create-event',
      {
         'name': 'Open-ended event',
         'location': EVENT_LOCATION,
         'description': EVENT_DESCRIPTION,
         'link': EVENT_LINK,
         'startDate': START_DATE,
         'endDate': None,
      }
   )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is True
   assert result[ 'endDate' ] is None


def Test_CreateEvent_TestHttpRequest_ExpectCouldNotCreateEventApiError(
      stub_event_coordinator: StubEventCoordinator ) -> None:
   StubEventCoordinator.default_success = False
   handler = make_handler( '/create-event', { 'name': EVENT_NAME } )

   server.HttpRequestHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'apiErrorType' ] == 'couldNotCreateEvent'
