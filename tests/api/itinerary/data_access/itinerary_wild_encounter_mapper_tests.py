from __future__ import annotations

from api.itinerary.data_access.itinerary_wild_encounter_mapper import ItineraryWildEncounterMapper
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.value_conversion import ValueConversion


def Test_MapRecord_TestRow_ExpectWildEncounterRecord() -> None:
   wild_encounter = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   is_deleted = 0
   row = {
      'WILD_ENCOUNTER': wild_encounter,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'IS_DELETED': is_deleted,
   }

   record = ItineraryWildEncounterMapper.map_record( row )

   assert record == ItineraryWildEncounterRecord(
      wild_encounter=wild_encounter,
      start_time=start_time,
      end_time=end_time,
      is_deleted=ValueConversion.as_boolean( is_deleted ) )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   wild_encounter = 'Kangaroo'
   start_time = '1:00 PM'
   duration_minutes = 45
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   is_deleted = 0
   row = {
      'WILD_ENCOUNTER': wild_encounter,
      'START_TIME': start_time,
      'END_TIME': end_time,
      'IS_DELETED': is_deleted,
   }
   rows = [ row ]

   records = ItineraryWildEncounterMapper.map_records( rows )

   assert records[ Position.FIRST ].wild_encounter == wild_encounter
