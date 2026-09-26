from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.calendar_dates import DateValues


def Test_FromWire_TestMissingTime_ExpectNone() -> None:
   wire = 'African Rainforest'

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptyTime_ExpectNone() -> None:
   name = 'African Rainforest'
   wire = f'{ name }{ ScheduleItemKeySeparator.VALUE }'

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptyEndTime_ExpectNone() -> None:
   name = 'Kangaroo'
   start_time = '1:00 PM'
   wire = ScheduleItemKeySeparator.VALUE.join( [ name, start_time, '' ] )

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestInvalidEndTime_ExpectNone() -> None:
   name = 'Kangaroo'
   start_time = '1:00 PM'
   end_time = 'bad'
   wire = ScheduleItemKeySeparator.VALUE.join( [ name, start_time, end_time ] )

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestStartTime_ExpectNormalizedKey() -> None:
   name = 'Masai Giraffe'
   start_time = '14:00'
   wire = ScheduleItemKeySeparator.VALUE.join( [ name, start_time ] )
   normalized_start = DateValues.normalize_schedule_time( start_time )

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key == WildEncounterScheduleItemKey(
      name=name,
      start_time=normalized_start )
   assert key.to_wire() == ScheduleItemKeySeparator.VALUE.join(
      [ name, normalized_start ] )


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   name = 'Kangaroo'
   start_time = '13:00'
   end_time = '13:45'
   wire = ScheduleItemKeySeparator.VALUE.join( [ name, start_time, end_time ] )
   normalized_start = DateValues.normalize_schedule_time( start_time )
   normalized_end = DateValues.normalize_schedule_time( end_time )

   key = WildEncounterScheduleItemKey.from_wire( wire )

   assert key == WildEncounterScheduleItemKey(
      name=name,
      start_time=normalized_start,
      end_time=normalized_end )
   assert key.to_wire() == ScheduleItemKeySeparator.VALUE.join(
      [ name, normalized_start, normalized_end ] )


def Test_FromWires_TestMixedEntries_ExpectValidKeysOnly() -> None:
   name = 'Kangaroo'
   start_time = '13:00'
   end_time = '13:45'
   other_name = 'Capybara'
   other_start = '11:00'
   wires = [
      ScheduleItemKeySeparator.VALUE.join( [ name, start_time, end_time ] ),
      '',
      other_name,
      ScheduleItemKeySeparator.VALUE.join( [ other_name, other_start ] ),
   ]

   keys = WildEncounterScheduleItemKey.from_wires( wires )

   assert keys == [
      WildEncounterScheduleItemKey(
         name=name,
         start_time=DateValues.normalize_schedule_time( start_time ),
         end_time=DateValues.normalize_schedule_time( end_time ) ),
      WildEncounterScheduleItemKey(
         name=other_name,
         start_time=DateValues.normalize_schedule_time( other_start ) ),
   ]


def Test_FromRow_TestWildEncounterRecord_ExpectScheduleItemKey() -> None:
   start_time = '13:00'
   end_time = '13:45'
   record = ItineraryWildEncounterRecord(
      wild_encounter='Kangaroo',
      start_time=start_time,
      end_time=end_time,
      is_deleted=False )

   key = record.schedule_item_key()

   assert key == WildEncounterScheduleItemKey(
      name=record.wild_encounter,
      start_time=DateValues.normalize_schedule_time( record.start_time ),
      end_time=DateValues.normalize_schedule_time( record.end_time ) )
   assert key.to_wire() == ScheduleItemKeySeparator.VALUE.join(
      [ record.wild_encounter, key.start_time, key.end_time ] )


def Test_Equality_TestEndTimeDifference_ExpectIgnored() -> None:
   name = 'African Rainforest'
   start_time = '15:30'
   start_only = WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time )
   with_end = WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time='16:15' )
   different_start = WildEncounterScheduleItemKey(
      name=name,
      start_time='14:00',
      end_time='16:15' )

   assert start_only == with_end
   assert hash( start_only ) == hash( with_end )
   assert start_only != different_start
   assert start_only != None


def Test_PostInit_TestInvalidStartTime_ExpectValueError() -> None:
   name = 'African Rainforest'
   start_time = 'not-a-time'

   with pytest.raises( ValueError, match='Invalid wild encounter start time' ):
      WildEncounterScheduleItemKey(
         name=name,
         start_time=start_time )


def Test_PostInit_TestInvalidEndTime_ExpectValueError() -> None:
   name = 'African Rainforest'
   start_time = '15:30'
   end_time = 'not-a-time'

   with pytest.raises( ValueError, match='Invalid wild encounter end time' ):
      WildEncounterScheduleItemKey(
         name=name,
         start_time=start_time,
         end_time=end_time )


def Test_FromRow_TestDictSource_ExpectScheduleItemKey() -> None:
   name = 'Kangaroo'
   start_time = '13:00'
   end_time = '13:45'
   row = {
      'wild_encounter': name,
      'start_time': start_time,
      'end_time': end_time,
   }

   key = WildEncounterScheduleItemKey.from_row( row )

   assert key == WildEncounterScheduleItemKey(
      name=name,
      start_time=DateValues.normalize_schedule_time( start_time ),
      end_time=DateValues.normalize_schedule_time( end_time ) )


def Test_FromRow_TestInvalidProvidedEndTime_ExpectNone() -> None:
   row = {
      'name': 'Kangaroo',
      'start_time': '13:00',
      'end_time': 'bad',
   }

   key = WildEncounterScheduleItemKey.from_row( row )

   assert key is None


def Test_FromRow_TestMissingName_ExpectNone() -> None:
   row = {
      'start_time': '13:00',
   }

   key = WildEncounterScheduleItemKey.from_row( row )

   assert key is None


def Test_Equality_TestNonKey_ExpectNotImplemented() -> None:
   key = WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM' )
   other = 'not-a-key'

   result = key.__eq__( other )

   assert result is NotImplemented


def Test_ToWire_TestWithEndTime_ExpectEndIncluded() -> None:
   name = 'Kangaroo'
   start_time = '1:00 PM'
   end_time = '1:45 PM'
   key = WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time )

   wire = key.to_wire()

   assert wire == ScheduleItemKeySeparator.VALUE.join(
      [ key.name, key.start_time, key.end_time ] )
