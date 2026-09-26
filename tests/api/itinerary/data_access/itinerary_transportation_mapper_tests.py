from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_mapper import ItineraryTransportationMapper
from api.itinerary.data_access.itinerary_transportation_route_marker_mapper import ItineraryTransportationRouteMarkerMapper
from api.itinerary.data_access.itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.shared.value_conversion import ValueConversion


def _leg(
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str,
      added_as_attraction: bool = False ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=from_station,
      to_station=to_station,
      start_time=start_time,
      end_time=end_time,
      transportation=TransportationName.ZOOMOBILE,
      added_as_attraction=added_as_attraction )


def Test_TransportationRowKey_TestNameAndMode_ExpectTuple() -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True

   key = ItineraryTransportationMapper.transportation_row_key(
      transportation,
      added_as_attraction )

   assert key == ( transportation, added_as_attraction )


def Test_MapRecords_TestLegsAndMarkersByKey_ExpectSortedGroupedRecord() -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = 0
   old_likelihood = None
   new_likelihood = 100
   start_time = '11:00 AM'
   first_leg_duration_minutes = 20
   second_leg_start_time = DateValues.add_minutes_to_time(
      start_time,
      first_leg_duration_minutes )
   second_leg_duration_minutes = 10
   end_time = DateValues.add_minutes_to_time(
      second_leg_start_time,
      second_leg_duration_minutes )
   route = 'summer'
   bulk_transit_evaluated = 1
   attraction_leg_start_time = '1:00 PM'
   attraction_leg_duration_minutes = 20
   first_marker_id = 'm-1'
   second_marker_id = 'm-2'
   ignored_marker_id = 'm-ignored'
   first_leg = _leg(
      from_station='Canada',
      to_station='Africa',
      start_time=second_leg_start_time,
      end_time=end_time )
   second_leg = _leg(
      from_station='Main',
      to_station='Canada',
      start_time=start_time,
      end_time=second_leg_start_time )
   attraction_leg = _leg(
      from_station='Main',
      to_station='Africa',
      start_time=attraction_leg_start_time,
      end_time=DateValues.add_minutes_to_time(
         attraction_leg_start_time,
         attraction_leg_duration_minutes ),
      added_as_attraction=True )
   rows = [
      {
         'TRANSPORTATION': transportation,
         'OLD_LIKELIHOOD': old_likelihood,
         'NEW_LIKELIHOOD': new_likelihood,
         'START_TIME': start_time,
         'END_TIME': end_time,
         'ADDED_AS_ATTRACTION': added_as_attraction,
         'ROUTE': route,
         'BULK_TRANSIT_EVALUATED': bulk_transit_evaluated,
      },
   ]
   legs = [ first_leg, second_leg, attraction_leg ]
   matching_markers = [
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=ValueConversion.as_boolean( added_as_attraction ),
         sequence=Position.FIRST,
         marker_order=Position.FIRST,
         marker_id=first_marker_id ),
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=ValueConversion.as_boolean( added_as_attraction ),
         sequence=Position.FIRST,
         marker_order=Position.SECOND,
         marker_id=second_marker_id ),
   ]
   markers = [
      *matching_markers,
      ItineraryTransportationRouteMarkerRecord(
         transportation=transportation,
         added_as_attraction=True,
         sequence=Position.FIRST,
         marker_order=Position.FIRST,
         marker_id=ignored_marker_id ),
   ]

   records = ItineraryTransportationMapper.map_records( rows, legs, markers )

   record = records[ Position.FIRST ]
   matching_legs = [
      leg
      for leg in legs
      if leg.added_as_attraction is ValueConversion.as_boolean( added_as_attraction )
   ]
   assert len( records ) == len( rows )
   assert record.transportation == transportation
   assert record.added_as_attraction is ValueConversion.as_boolean(
      added_as_attraction )
   assert record.route == route
   assert record.bulk_transit_evaluated is ValueConversion.as_boolean(
      bulk_transit_evaluated )
   assert [
      ( leg.from_station, leg.start_time )
      for leg in record.legs
   ] == [
      ( leg.from_station, leg.start_time )
      for leg in sorted(
         matching_legs,
         key=lambda leg: DateValues.time_value_in_seconds( leg.start_time ) )
   ]
   assert record.route_marker_sequences == (
      ItineraryTransportationRouteMarkerMapper.route_marker_sequences_for_markers(
         matching_markers ) )
