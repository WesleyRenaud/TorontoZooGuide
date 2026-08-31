from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_mapper import ItineraryTransportationMapper
from api.itinerary.data_access.itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


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
      transportation='Zoomobile',
      added_as_attraction=added_as_attraction )


def Test_TransportationRowKey_TestNameAndMode_ExpectTuple() -> None:
   assert ItineraryTransportationMapper.transportation_row_key(
      'Zoomobile',
      True ) == ( 'Zoomobile', True )


def Test_MapRecords_TestLegsAndMarkersByKey_ExpectSortedGroupedRecord() -> None:
   rows = [
      {
         'TRANSPORTATION': 'Zoomobile',
         'OLD_LIKELIHOOD': None,
         'NEW_LIKELIHOOD': 100,
         'START_TIME': '11:00 AM',
         'END_TIME': '11:30 AM',
         'ADDED_AS_ATTRACTION': 0,
         'ROUTE': 'summer',
         'BULK_TRANSIT_EVALUATED': 1,
      },
   ]
   legs = [
      _leg(
         from_station='Canada',
         to_station='Africa',
         start_time='11:20 AM',
         end_time='11:30 AM' ),
      _leg(
         from_station='Main',
         to_station='Canada',
         start_time='11:00 AM',
         end_time='11:20 AM' ),
      _leg(
         from_station='Main',
         to_station='Africa',
         start_time='1:00 PM',
         end_time='1:20 PM',
         added_as_attraction=True ),
   ]
   markers = [
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=False,
         sequence=0,
         marker_order=0,
         marker_id='m-1' ),
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=False,
         sequence=0,
         marker_order=1,
         marker_id='m-2' ),
      ItineraryTransportationRouteMarkerRecord(
         transportation='Zoomobile',
         added_as_attraction=True,
         sequence=0,
         marker_order=0,
         marker_id='m-ignored' ),
   ]

   records = ItineraryTransportationMapper.map_records( rows, legs, markers )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.transportation == 'Zoomobile'
   assert record.added_as_attraction is False
   assert record.route == 'summer'
   assert record.bulk_transit_evaluated is True
   assert [
      ( leg.from_station, leg.start_time )
      for leg in record.legs
   ] == [
      ( 'Main', '11:00 AM' ),
      ( 'Canada', '11:20 AM' ),
   ]
   assert record.route_marker_sequences == [ [ 'm-1', 'm-2' ] ]
