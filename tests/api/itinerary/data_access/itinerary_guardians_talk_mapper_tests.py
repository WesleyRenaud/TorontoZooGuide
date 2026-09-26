from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_mapper import ItineraryGuardiansTalkMapper
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.value_conversion import ValueConversion


def Test_MapRecord_TestRow_ExpectGuardiansTalkRecord() -> None:
   talk_name = 'African Lion'
   start_time = '2:00 PM'
   duration_minutes = 30
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   is_deleted = 0
   row = {
      'TALK_NAME': talk_name,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'IS_DELETED': is_deleted,
   }

   record = ItineraryGuardiansTalkMapper.map_record( row )

   assert record == ItineraryGuardiansTalkRecord(
      talk_name=talk_name,
      start_time=start_time,
      end_time=end_time,
      is_deleted=ValueConversion.as_boolean( is_deleted ) )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   talk_name = 'African Lion'
   start_time = '2:00 PM'
   duration_minutes = 30
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   is_deleted = 0
   row = {
      'TALK_NAME': talk_name,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'IS_DELETED': is_deleted,
   }
   rows = [ row ]

   records = ItineraryGuardiansTalkMapper.map_records( rows )

   assert records[ Position.FIRST ].talk_name == talk_name
