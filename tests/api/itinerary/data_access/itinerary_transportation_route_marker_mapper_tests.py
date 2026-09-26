from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_route_marker_mapper import ItineraryTransportationRouteMarkerMapper
from api.itinerary.data_access.itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.shared.value_conversion import ValueConversion


def Test_MapRecord_TestRow_ExpectMarkerRecord() -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = 0
   sequence = 1
   marker_order = 2
   marker_id = 'm-1'
   row = {
      'TRANSPORTATION': transportation,
      'ADDED_AS_ATTRACTION': added_as_attraction,
      'SEQUENCE': sequence,
      'MARKER_ORDER': marker_order,
      'MARKER_ID': marker_id,
   }

   record = ItineraryTransportationRouteMarkerMapper.map_record( row )

   assert record == ItineraryTransportationRouteMarkerRecord(
      transportation=transportation,
      added_as_attraction=ValueConversion.as_boolean( added_as_attraction ),
      sequence=sequence,
      marker_order=marker_order,
      marker_id=marker_id )


def Test_RouteMarkerSequencesForMarkers_TestSequenceChange_ExpectSplitLists() -> None:
   transportation = TransportationName.ZOOMOBILE
   first_marker_id = 'm-a'
   second_marker_id = 'm-b'
   third_marker_id = 'm-c'
   first_sequence = Position.FIRST
   second_sequence = Position.SECOND
   markers = [
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=False,
         sequence=first_sequence,
         marker_order=Position.FIRST,
         marker_id=first_marker_id ),
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=False,
         sequence=first_sequence,
         marker_order=Position.SECOND,
         marker_id=second_marker_id ),
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=False,
         sequence=second_sequence,
         marker_order=Position.FIRST,
         marker_id=third_marker_id ),
   ]

   sequences = ItineraryTransportationRouteMarkerMapper.route_marker_sequences_for_markers(
      markers )

   assert sequences == [
      [ first_marker_id, second_marker_id ],
      [ third_marker_id ],
   ]


def Test_RouteMarkerSequencesForMarkers_TestEmpty_ExpectEmpty() -> None:
   markers = []

   sequences = ItineraryTransportationRouteMarkerMapper.route_marker_sequences_for_markers(
      markers )

   assert sequences == []
