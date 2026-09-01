from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_mapper import ItineraryGuardiansTalkMapper
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord


TALK_ROW = {
   'TALK_NAME': 'African Lion',
   'START_TIME': '2:00 PM',
   'END_TIME': '2:30 PM',
   'IS_DELETED': 0,
}


def Test_MapRecord_TestRow_ExpectGuardiansTalkRecord() -> None:
   assert ItineraryGuardiansTalkMapper.map_record( TALK_ROW ) == ItineraryGuardiansTalkRecord(
      talk_name='African Lion',
      start_time='2:00 PM',
      end_time='2:30 PM',
      is_deleted=False,
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryGuardiansTalkMapper.map_records( [ TALK_ROW ] )

   assert records[ 0 ].talk_name == 'African Lion'
