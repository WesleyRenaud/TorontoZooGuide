from __future__ import annotations

from api.itinerary.data_access.itinerary_wild_encounter_mapper import ItineraryWildEncounterMapper
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord


ENCOUNTER_ROW = {
   'WILD_ENCOUNTER': 'Kangaroo',
   'START_TIME': '1:00 PM',
   'END_TIME': '1:45 PM',
   'IS_DELETED': 0,
}


def Test_MapRecord_TestRow_ExpectWildEncounterRecord() -> None:
   assert ItineraryWildEncounterMapper.map_record( ENCOUNTER_ROW ) == ItineraryWildEncounterRecord(
      wild_encounter='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM',
      is_deleted=False,
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryWildEncounterMapper.map_records( [ ENCOUNTER_ROW ] )

   assert records[ 0 ].wild_encounter == 'Kangaroo'
