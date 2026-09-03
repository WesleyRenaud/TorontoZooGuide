from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


def Test_FromWire_TestMissingOrInvalidTime_ExpectNone() -> None:
   assert WildEncounterScheduleItemKey.from_wire( 'African Rainforest' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'African Rainforest||' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'Kangaroo||1:00 PM||' ) is None
   assert WildEncounterScheduleItemKey.from_wire( 'Kangaroo||1:00 PM||bad' ) is None


def Test_FromWire_TestStartTime_ExpectNormalizedKey() -> None:
   key = WildEncounterScheduleItemKey.from_wire( 'Masai Giraffe||14:00' )

   assert key == WildEncounterScheduleItemKey(
      name='Masai Giraffe',
      start_time='2:00 PM' )
   assert key.to_wire() == 'Masai Giraffe||2:00 PM'


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   key = WildEncounterScheduleItemKey.from_wire( 'Kangaroo||13:00||13:45' )

   assert key == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )
   assert key.to_wire() == 'Kangaroo||1:00 PM||1:45 PM'


def Test_FromWires_TestMixedEntries_ExpectValidKeysOnly() -> None:
   keys = WildEncounterScheduleItemKey.from_wires( [
      'Kangaroo||13:00||13:45',
      '',
      'Capybara',
      'Capybara||11:00',
   ] )

   assert keys == [
      WildEncounterScheduleItemKey(
         name='Kangaroo',
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      WildEncounterScheduleItemKey(
         name='Capybara',
         start_time='11:00 AM' ),
   ]


def Test_FromRow_TestWildEncounterRecord_ExpectScheduleItemKey() -> None:
   record = ItineraryWildEncounterRecord(
      wild_encounter='Kangaroo',
      start_time='13:00',
      end_time='13:45',
      is_deleted=False,
   )

   assert record.schedule_item_key() == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )
   assert record.schedule_item_key().to_wire() == 'Kangaroo||1:00 PM||1:45 PM'


def Test_Equality_TestEndTimeDifference_ExpectIgnored() -> None:
   start_only = WildEncounterScheduleItemKey(
      name='African Rainforest',
      start_time='15:30' )
   with_end = WildEncounterScheduleItemKey(
      name='African Rainforest',
      start_time='15:30',
      end_time='16:15' )
   different_start = WildEncounterScheduleItemKey(
      name='African Rainforest',
      start_time='14:00',
      end_time='16:15' )

   assert start_only == with_end
   assert hash( start_only ) == hash( with_end )
   assert start_only != different_start
   assert start_only != None


def Test_PostInit_TestInvalidStartTime_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='Invalid wild encounter start time' ):
      WildEncounterScheduleItemKey(
         name='African Rainforest',
         start_time='not-a-time' )


def Test_PostInit_TestInvalidEndTime_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='Invalid wild encounter end time' ):
      WildEncounterScheduleItemKey(
         name='African Rainforest',
         start_time='15:30',
         end_time='not-a-time' )


def Test_FromRow_TestDictSource_ExpectScheduleItemKey() -> None:
   key = WildEncounterScheduleItemKey.from_row( {
      'wild_encounter': 'Kangaroo',
      'start_time': '13:00',
      'end_time': '13:45',
   } )

   assert key == WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )


def Test_FromRow_TestInvalidProvidedEndTime_ExpectNone() -> None:
   assert WildEncounterScheduleItemKey.from_row( {
      'name': 'Kangaroo',
      'start_time': '13:00',
      'end_time': 'bad',
   } ) is None


def Test_FromRow_TestMissingName_ExpectNone() -> None:
   assert WildEncounterScheduleItemKey.from_row( {
      'start_time': '13:00',
   } ) is None


def Test_Equality_TestNonKey_ExpectNotImplemented() -> None:
   key = WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM' )

   assert key.__eq__( 'not-a-key' ) is NotImplemented


def Test_ToWire_TestWithEndTime_ExpectEndIncluded() -> None:
   key = WildEncounterScheduleItemKey(
      name='Kangaroo',
      start_time='1:00 PM',
      end_time='1:45 PM' )

   assert key.to_wire() == 'Kangaroo||1:00 PM||1:45 PM'
