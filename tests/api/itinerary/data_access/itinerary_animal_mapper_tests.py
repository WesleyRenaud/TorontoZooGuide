from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_mapper import ItineraryAnimalMapper
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName
from api.shared.value_conversion import ValueConversion


def Test_MapRecord_TestRow_ExpectAnimalRecord() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   enclosure_name = None
   old_likelihood = 80
   new_likelihood = 100
   is_added = 1
   covered_by_talk = 0
   added_by_transportation = 0
   transportation = None
   start_time = '10:00 AM'
   duration_minutes = 8
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'SPECIES': species,
      'EXHIBIT': exhibit,
      'ENCLOSURE_NAME': enclosure_name,
      'OLD_LIKELIHOOD': old_likelihood,
      'NEW_LIKELIHOOD': new_likelihood,
      'IS_ADDED': is_added,
      'COVERED_BY_TALK': covered_by_talk,
      'ADDED_BY_TRANSPORTATION': added_by_transportation,
      'TRANSPORTATION': transportation,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }

   record = ItineraryAnimalMapper.map_record( row )

   assert record == ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=old_likelihood,
      new_likelihood=new_likelihood,
      is_added=ValueConversion.as_boolean( is_added ),
      covered_by_talk=ValueConversion.as_boolean( covered_by_talk ),
      added_by_transportation=ValueConversion.as_boolean( added_by_transportation ),
      transportation=transportation,
      start_time=start_time,
      end_time=end_time )


def Test_MapRecords_TestRows_ExpectMappedRecords() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   enclosure_name = None
   old_likelihood = 80
   new_likelihood = 100
   is_added = 1
   covered_by_talk = 0
   added_by_transportation = 0
   transportation = None
   start_time = '10:00 AM'
   duration_minutes = 8
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'SPECIES': species,
      'EXHIBIT': exhibit,
      'ENCLOSURE_NAME': enclosure_name,
      'OLD_LIKELIHOOD': old_likelihood,
      'NEW_LIKELIHOOD': new_likelihood,
      'IS_ADDED': is_added,
      'COVERED_BY_TALK': covered_by_talk,
      'ADDED_BY_TRANSPORTATION': added_by_transportation,
      'TRANSPORTATION': transportation,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }
   rows = [ row ]

   records = ItineraryAnimalMapper.map_records( rows )

   assert len( records ) == len( rows )
   assert records[ Position.FIRST ].species == species


def Test_MapRecord_TestAddedByTransportation_ExpectTransportationName() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   enclosure_name = None
   old_likelihood = 80
   new_likelihood = 100
   is_added = 1
   covered_by_talk = 0
   added_by_transportation = 1
   transportation = TransportationName.ZOOMOBILE
   start_time = '10:00 AM'
   duration_minutes = 8
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   row = {
      'SPECIES': species,
      'EXHIBIT': exhibit,
      'ENCLOSURE_NAME': enclosure_name,
      'OLD_LIKELIHOOD': old_likelihood,
      'NEW_LIKELIHOOD': new_likelihood,
      'IS_ADDED': is_added,
      'COVERED_BY_TALK': covered_by_talk,
      'ADDED_BY_TRANSPORTATION': added_by_transportation,
      'TRANSPORTATION': transportation,
      'START_TIME': start_time,
      'END_TIME': end_time,
   }

   record = ItineraryAnimalMapper.map_record( row )

   assert record.added_by_transportation is ValueConversion.as_boolean(
      added_by_transportation )
   assert record.transportation == transportation
