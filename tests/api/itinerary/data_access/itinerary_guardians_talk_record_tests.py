from __future__ import annotations

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord


TALK_RECORD = ItineraryGuardiansTalkRecord(
   talk_name='African Lion',
   start_time='2:00 PM',
   end_time='2:30 PM',
   is_deleted=False,
)


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   assert TALK_RECORD.name_key() == 'african lion'
