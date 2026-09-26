from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.date_values import DateValues


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   wild_encounter = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   record = ItineraryWildEncounterRecord(
      wild_encounter=wild_encounter,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      is_deleted=False )

   name_key = record.name_key()

   assert name_key == ItineraryNameKeyBuilder.build( record.wild_encounter )


def Test_ScheduleItemKey_TestRecord_ExpectWildEncounterKey() -> None:
   wild_encounter = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   record = ItineraryWildEncounterRecord(
      wild_encounter=wild_encounter,
      start_time=start_time,
      end_time=end_time,
      is_deleted=False )

   key = record.schedule_item_key()

   assert key == WildEncounterScheduleItemKey(
      name=record.wild_encounter,
      start_time=record.start_time,
      end_time=record.end_time )


def Test_ScheduleItemKey_TestMissingStartTime_ExpectValueError() -> None:
   wild_encounter = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   record = ItineraryWildEncounterRecord(
      wild_encounter=wild_encounter,
      start_time=None,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      is_deleted=False )

   with pytest.raises( ValueError, match=repr( record.wild_encounter ) ):
      record.schedule_item_key()
