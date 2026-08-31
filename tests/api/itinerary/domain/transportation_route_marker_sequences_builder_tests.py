from __future__ import annotations

import pytest

from api.itinerary.domain.transportation_route_marker_sequences_builder import TransportationRouteMarkerSequencesBuilder
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider


ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
AFRICA = 'Africa Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'

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
      transportation=ZOOMOBILE,
      added_as_attraction=False )


@pytest.fixture
def stub_transportation_route_leg_markers( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationRouteLegMarkerProvider,
      'fetch_transportation_route_leg_markers_by_leg',
      lambda conn, *, transportation, route: MARKERS_BY_LEG )


def Test_Build_TestDiscontinuousLegs_ExpectSplitSequences(
      stub_transportation_route_leg_markers: None ) -> None:
   sequences = TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         _leg(
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM' ),
         _leg(
            from_station=TUNDRA,
            to_station=EURASIA,
            start_time='2:00 PM',
            end_time='2:15 PM' ),
      ],
   )

   assert sequences == [
      [ 'm-a', 'm-b' ],
      [ 'm-d', 'm-e' ],
   ]


def Test_Build_TestConsecutiveLegs_ExpectConcatenatedSequence(
      stub_transportation_route_leg_markers: None ) -> None:
   sequences = TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[
         _leg(
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM' ),
         _leg(
            from_station=CANADA,
            to_station=AFRICA,
            start_time='10:20 AM',
            end_time='10:30 AM' ),
      ],
   )

   assert sequences == [
      [ 'm-a', 'm-b', 'm-c' ],
   ]


def Test_Build_TestEmptyLegs_ExpectEmptySequences() -> None:
   assert TransportationRouteMarkerSequencesBuilder.build(
      None,
      transportation=ZOOMOBILE,
      route='summer',
      legs=[] ) == []
