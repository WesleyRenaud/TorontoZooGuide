from __future__ import annotations

import pytest

from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider


ZOOMOBILE = 'Zoomobile'
MAIN = 'Main Zoomobile Station'
CANADA = 'Canadian Domain Zoomobile Station'
EURASIA = 'Eurasia Zoomobile Station'
SUMMER_ROUTE = 'summer'
MARKER_MAXIMUM = 297


def ordered_marker_ids(
      prefix: str,
      start: int,
      end: int,
      maximum: int ) -> list[ str ]:
   marker_numbers = (
      range( start, end + 1 )
      if start <= end
      else [ *range( start, maximum + 1 ), *range( 1, end + 1 ) ]
   )

   return [
      f'{ prefix }-{ str( marker_number ).zfill( 3 ) }'
      for marker_number in marker_numbers
   ]


MAIN_TO_CANADA_MARKERS = ordered_marker_ids( 'zm-s', 5, 85, MARKER_MAXIMUM )
EURASIA_TO_MAIN_MARKERS = ordered_marker_ids( 'zm-s', 252, 4, MARKER_MAXIMUM )

MARKERS_BY_LEG = {
   ( MAIN, CANADA ): MAIN_TO_CANADA_MARKERS,
   ( EURASIA, MAIN ): EURASIA_TO_MAIN_MARKERS,
}


@pytest.fixture
def stub_transportation_route_leg_markers( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      TransportationRouteLegMarkerProvider,
      'fetch_transportation_route_leg_markers_by_leg',
      lambda conn, *, transportation, route: MARKERS_BY_LEG )


def Test_FetchTransportationRouteLegMarkerIds_TestSingleLeg_ExpectTravelOrder(
      stub_transportation_route_leg_markers: None ) -> None:
   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      None,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=MAIN,
            to_station=CANADA,
            start_time='10:00 AM',
            end_time='10:20 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == MAIN_TO_CANADA_MARKERS
   assert set( marker_ids_result ) == set( MAIN_TO_CANADA_MARKERS )


def Test_FetchTransportationRouteLegMarkerIds_TestWraparoundLeg_ExpectTravelOrder(
      stub_transportation_route_leg_markers: None ) -> None:
   marker_ids_result = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_marker_ids(
      None,
      transportation=ZOOMOBILE,
      route=SUMMER_ROUTE,
      legs=[
         ItineraryTransportationLeg(
            transportation=ZOOMOBILE,
            from_station=EURASIA,
            to_station=MAIN,
            start_time='11:00 AM',
            end_time='11:15 AM',
            added_as_attraction=False,
         ),
      ],
   )

   assert marker_ids_result == EURASIA_TO_MAIN_MARKERS
   assert marker_ids_result[ 0 ] == 'zm-s-252'
   assert marker_ids_result[ -1 ] == 'zm-s-004'
