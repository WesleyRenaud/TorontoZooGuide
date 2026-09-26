from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from api.shared.date_values import DateValues


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   talk_name = 'African Lion'
   start_time = '2:00 PM'
   duration_minutes = 30
   record = ItineraryGuardiansTalkRecord(
      talk_name=talk_name,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      is_deleted=False )

   name_key = record.name_key()

   assert name_key == ItineraryNameKeyBuilder.build( record.talk_name )
