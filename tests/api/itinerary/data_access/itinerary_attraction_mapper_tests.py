from __future__ import annotations

from api.itinerary.data_access.itinerary_attraction_mapper import ItineraryAttractionMapper
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord


ATTRACTION_ROW = {
   'ATTRACTION': 'Conservation Carousel',
   'OLD_LIKELIHOOD': None,
   'NEW_LIKELIHOOD': 100,
   'START_TIME': '11:00 AM',
   'END_TIME': '11:20 AM',
}


def Test_MapRecord_TestRow_ExpectAttractionRecord() -> None:
   assert ItineraryAttractionMapper.map_record( ATTRACTION_ROW ) == ItineraryAttractionRecord(
      attraction='Conservation Carousel',
      old_likelihood=None,
      new_likelihood=100,
      start_time='11:00 AM',
      end_time='11:20 AM',
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryAttractionMapper.map_records( [ ATTRACTION_ROW ] )

   assert records[ 0 ].attraction == 'Conservation Carousel'
