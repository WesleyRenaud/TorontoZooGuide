from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


ENCOUNTER_RECORD = ItineraryWildEncounterRecord(
   wild_encounter='Kangaroo',
   start_time='1:00 PM',
   end_time='1:45 PM',
   is_deleted=False,
)


def Test_NameKey_TestRecord_ExpectNormalizedName() -> None:
   assert ENCOUNTER_RECORD.name_key() == 'kangaroo'


def Test_ScheduleItemKey_TestRecord_ExpectWildEncounterKey() -> None:
   assert ENCOUNTER_RECORD.schedule_item_key() == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM',
   )


def Test_ScheduleItemKey_TestMissingStartTime_ExpectValueError() -> None:
   record = ItineraryWildEncounterRecord(
      wild_encounter='Kangaroo',
      start_time=None,
      end_time='1:45 PM',
      is_deleted=False,
   )

   with pytest.raises( ValueError, match='Kangaroo' ):
      record.schedule_item_key()
