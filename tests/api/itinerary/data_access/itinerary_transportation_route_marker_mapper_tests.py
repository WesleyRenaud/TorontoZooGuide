from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_route_marker_mapper import ItineraryTransportationRouteMarkerMapper
from api.itinerary.data_access.itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord


def Test_MapRecord_TestRow_ExpectMarkerRecord() -> None:
   record = ItineraryTransportationRouteMarkerMapper.map_record(
      {
         'TRANSPORTATION': 'Zoomobile',
         'ADDED_AS_ATTRACTION': 0,
         'SEQUENCE': 1,
         'MARKER_ORDER': 2,
         'MARKER_ID': 'm-1',
      } )

   assert record == ItineraryTransportationRouteMarkerRecord(
      transportation='Zoomobile',
      added_as_attraction=False,
      sequence=1,
      marker_order=2,
      marker_id='m-1',
   )


def Test_RouteMarkerSequencesForMarkers_TestSequenceChange_ExpectSplitLists() -> None:
   markers = [
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=False,
         sequence=0,
         marker_order=0,
         marker_id='m-a' ),
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=False,
         sequence=0,
         marker_order=1,
         marker_id='m-b' ),
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=False,
         sequence=1,
         marker_order=0,
         marker_id='m-c' ),
   ]

   assert ItineraryTransportationRouteMarkerMapper.route_marker_sequences_for_markers(
      markers ) == [
      [ 'm-a', 'm-b' ],
      [ 'm-c' ],
   ]


def Test_RouteMarkerSequencesForMarkers_TestEmpty_ExpectEmpty() -> None:
   assert ItineraryTransportationRouteMarkerMapper.route_marker_sequences_for_markers(
      [] ) == []
