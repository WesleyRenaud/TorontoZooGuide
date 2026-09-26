from __future__ import annotations

from datetime import date

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.itinerary.transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.request_connection_provider import RequestConnectionProvider
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_provider import TransportationProvider
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_record import TransportationStationRecord


VISIT_DATE = date( 2026, 6, 15 )
MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'
ROUTE_DURATION_MINUTES = 75
ATTRACTION_X_COORD = 30.0
ATTRACTION_Y_COORD = 40.0

MAIN_STATION_RECORD = TransportationStationRecord(
   name=MAIN_STATION,
   description='Main',
   x_coord=10.0,
   y_coord=20.0,
)

TRANSPORTATION_LEGS = [
   ItineraryTransportationLeg(
      from_station=MAIN_STATION,
      to_station=CANADA_STATION,
      start_time='10:00 AM',
      end_time='10:20 AM',
      transportation=TransportationName.ZOOMOBILE,
      added_as_attraction=False ),
]

SAVED_TRANSPORTATION = ItineraryTransportationRecord(
   transportation=TransportationName.ZOOMOBILE,
   old_likelihood=1,
   new_likelihood=3,
   added_as_attraction=False,
   start_time='10:00 AM',
   end_time='11:15 AM',
   route='summer',
   bulk_transit_evaluated=True,
   legs=TRANSPORTATION_LEGS,
   route_marker_sequences=[ [ 'm-1', 'm-2' ] ],
)

UNSCHEDULED_TRANSPORTATION = ItineraryTransportationRecord(
   transportation=TransportationName.ZOOMOBILE,
   old_likelihood=None,
   new_likelihood=None,
   added_as_attraction=True,
   legs=[],
)


@pytest.fixture
def stub_itinerary_transportations_builder( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_REQUEST_CONNECTION )
   monkeypatch.setattr(
      TransportationProvider,
      'fetch_transportation_records',
      lambda conn, target_date: [
         type(
            'TransportationRecord',
            (),
            {
               'name': TransportationName.ZOOMOBILE,
               'x_coord': ATTRACTION_X_COORD,
               'y_coord': ATTRACTION_Y_COORD,
            },
         )(),
      ] )
   monkeypatch.setattr(
      TransportationStationProvider,
      'fetch_main_transportation_station_record',
      lambda conn, transportation: MAIN_STATION_RECORD )
   monkeypatch.setattr(
      TransportationRouteDurationResolver,
      'minutes',
      lambda conn, *, transportation, target_date: ROUTE_DURATION_MINUTES )


def Test_Build_TestSavedTransportation_ExpectMappedModel(
      stub_itinerary_transportations_builder: None ) -> None:
   saved = SAVED_TRANSPORTATION

   transportations = ItineraryTransportationsBuilder.build(
      [ saved ],
      target_date=VISIT_DATE )

   transportation = transportations[ Position.FIRST ]

   assert len( transportations ) == 1
   assert transportation.name == saved.transportation
   assert transportation.old_likelihood == saved.old_likelihood
   assert transportation.likelihood == saved.new_likelihood
   assert transportation.start_time == saved.start_time
   assert transportation.end_time == saved.end_time
   assert transportation.x_coord == MAIN_STATION_RECORD.x_coord
   assert transportation.y_coord == MAIN_STATION_RECORD.y_coord
   assert transportation.main_station == MAIN_STATION_RECORD.name
   assert transportation.legs == saved.legs
   assert transportation.route == saved.route
   assert transportation.route_marker_sequences == saved.route_marker_sequences
   assert transportation.added_as_attraction is saved.added_as_attraction
   assert transportation.route_duration_minutes == ROUTE_DURATION_MINUTES
   assert transportation.bulk_transit_evaluated is saved.bulk_transit_evaluated


def Test_Build_TestUnscheduledTransportation_ExpectAttractionCoords(
      stub_itinerary_transportations_builder: None ) -> None:
   saved = UNSCHEDULED_TRANSPORTATION

   transportations = ItineraryTransportationsBuilder.build(
      [ saved ],
      target_date=VISIT_DATE )

   transportation = transportations[ Position.FIRST ]

   assert transportation.x_coord == ATTRACTION_X_COORD
   assert transportation.y_coord == ATTRACTION_Y_COORD
