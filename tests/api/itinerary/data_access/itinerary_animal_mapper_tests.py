from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_mapper import ItineraryAnimalMapper
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord


ANIMAL_ROW = {
   'SPECIES': 'African Lion',
   'EXHIBIT': 'Africa Savanna',
   'ENCLOSURE_NAME': None,
   'OLD_LIKELIHOOD': 80,
   'NEW_LIKELIHOOD': 100,
   'IS_ADDED': 1,
   'COVERED_BY_TALK': 0,
   'START_TIME': '10:00 AM',
   'END_TIME': '10:08 AM',
}


def Test_MapRecord_TestRow_ExpectAnimalRecord() -> None:
   assert ItineraryAnimalMapper.map_record( ANIMAL_ROW ) == ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name=None,
      old_likelihood=80,
      new_likelihood=100,
      is_added=True,
      covered_by_talk=False,
      start_time='10:00 AM',
      end_time='10:08 AM',
   )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   records = ItineraryAnimalMapper.map_records( [ ANIMAL_ROW ] )

   assert len( records ) == 1
   assert records[ 0 ].species == 'African Lion'
