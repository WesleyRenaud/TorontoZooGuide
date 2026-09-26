from __future__ import annotations

import pytest

from api.itinerary.domain.transportation_route_marker_sequences_builder import TransportationRouteMarkerSequencesBuilder
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums.transportation_name import TransportationName
from api.transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider


MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
ROUTE = 'summer'
MARKERS_BY_LEG = {
   ( MAIN, CANADA ): [ 'm-a', 'm-b' ],
   ( CANADA, AFRICA ): [ 'm-c' ],
   ( TUNDRA, EURASIA ): [ 'm-d', 'm-e' ],
}


def _leg(
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=from_station,
      to_station=to_station,
      start_time=start_time,
      end_time=end_time,
      transportation=TransportationName.ZOOMOBILE,
      added_as_attraction=False )


@pytest.fixture
def stub_transportation_route_leg_markers( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationRouteLegMarkerProvider,
      'fetch_transportation_route_leg_markers_by_leg',
      lambda conn, *, transportation, route: MARKERS_BY_LEG )


def Test_Build_TestDiscontinuousLegs_ExpectSplitSequences(
      stub_transportation_route_leg_markers: None ) -> None:
   first_leg = _leg(
      from_station=MAIN,
      to_station=CANADA,
      start_time='10:00 AM',
      end_time='10:20 AM' )
   second_leg = _leg(
      from_station=TUNDRA,
      to_station=EURASIA,
      start_time='2:00 PM',
      end_time='2:15 PM' )

   sequences = TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=TransportationName.ZOOMOBILE,
      route=ROUTE,
      legs=[ first_leg, second_leg ] )

   assert sequences == [
      MARKERS_BY_LEG[ ( first_leg.from_station, first_leg.to_station ) ],
      MARKERS_BY_LEG[ ( second_leg.from_station, second_leg.to_station ) ],
   ]


def Test_Build_TestConsecutiveLegs_ExpectConcatenatedSequence(
      stub_transportation_route_leg_markers: None ) -> None:
   first_leg = _leg(
      from_station=MAIN,
      to_station=CANADA,
      start_time='10:00 AM',
      end_time='10:20 AM' )
   second_leg = _leg(
      from_station=CANADA,
      to_station=AFRICA,
      start_time=first_leg.end_time,
      end_time='10:30 AM' )

   sequences = TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=TransportationName.ZOOMOBILE,
      route=ROUTE,
      legs=[ first_leg, second_leg ] )

   assert sequences == [
      MARKERS_BY_LEG[ ( first_leg.from_station, first_leg.to_station ) ]
      + MARKERS_BY_LEG[ ( second_leg.from_station, second_leg.to_station ) ],
   ]


def Test_Build_TestEmptyLegs_ExpectEmptySequences() -> None:
   legs: list[ ItineraryTransportationLeg ] = []

   sequences = TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=TransportationName.ZOOMOBILE,
      route=ROUTE,
      legs=legs )

   assert sequences == []
