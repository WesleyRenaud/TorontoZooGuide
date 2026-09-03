from __future__ import annotations

from datetime import date

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from api.itinerary.transportation.transportation_route_duration_resolver import TransportationRouteDurationResolver
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.request_connection_provider import RequestConnectionProvider
from api.transportation.data_access.transportation_provider import TransportationProvider
from api.transportation.data_access.transportation_station_provider import TransportationStationProvider
from api.transportation.data_access.transportation_station_record import TransportationStationRecord
from api.types import Types


VISIT_DATE = date( 2026, 6, 15 )
ZOOMOBILE = 'Zoomobile'
MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'
ROUTE_DURATION_MINUTES = 75

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
      transportation=ZOOMOBILE,
      added_as_attraction=False ),
]

SAVED_TRANSPORTATION = ItineraryTransportationRecord(
   transportation=ZOOMOBILE,
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
               'name': ZOOMOBILE,
               'x_coord': 30.0,
               'y_coord': 40.0,
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
   transportations = ItineraryTransportationsBuilder.build(
      [ SAVED_TRANSPORTATION ],
      target_date=VISIT_DATE )

   assert len( transportations ) == 1
   transportation = transportations[ 0 ]

   assert transportation.name == ZOOMOBILE
   assert transportation.old_likelihood == 1
   assert transportation.likelihood == 3
   assert transportation.start_time == '10:00 AM'
   assert transportation.end_time == '11:15 AM'
   assert transportation.x_coord == 10.0
   assert transportation.y_coord == 20.0
   assert transportation.main_station == MAIN_STATION
   assert transportation.legs == TRANSPORTATION_LEGS
   assert transportation.route == 'summer'
   assert transportation.route_marker_sequences == [ [ 'm-1', 'm-2' ] ]
   assert transportation.added_as_attraction is False
   assert transportation.route_duration_minutes == ROUTE_DURATION_MINUTES
   assert transportation.bulk_transit_evaluated is True


def Test_Build_TestUnscheduledTransportation_ExpectAttractionCoords(
      monkeypatch: pytest.MonkeyPatch,
      stub_itinerary_transportations_builder: None,
) -> None:
   transportations = ItineraryTransportationsBuilder.build(
      [
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=None,
            added_as_attraction=True,
            legs=[],
         ),
      ],
      target_date=VISIT_DATE )

   assert transportations[ 0 ].x_coord == 30.0
   assert transportations[ 0 ].y_coord == 40.0
