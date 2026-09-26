from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator
from api.shared.calendar_dates import DateValues


GORILLA_TALK = 'Gorilla Guardians'


def Test_FromWire_TestStartTime_ExpectNormalizedKey() -> None:
   start_time = '10:00'
   wire = ScheduleItemKeySeparator.VALUE.join( [ GORILLA_TALK, start_time ] )
   normalized_start = DateValues.normalize_schedule_time( start_time )

   key = GuardiansTalkScheduleItemKey.from_wire( wire )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=normalized_start )
   assert key.to_wire() == ScheduleItemKeySeparator.VALUE.join(
      [ GORILLA_TALK, normalized_start ] )


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   start_time = '10:00'
   end_time = '10:30'
   wire = ScheduleItemKeySeparator.VALUE.join(
      [ GORILLA_TALK, start_time, end_time ] )
   normalized_start = DateValues.normalize_schedule_time( start_time )
   normalized_end = DateValues.normalize_schedule_time( end_time )

   key = GuardiansTalkScheduleItemKey.from_wire( wire )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=normalized_start,
      end_time=normalized_end )


def Test_FromWire_TestMissingTime_ExpectNone() -> None:
   wire = GORILLA_TALK

   key = GuardiansTalkScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptyTime_ExpectNone() -> None:
   wire = f'{ GORILLA_TALK }{ ScheduleItemKeySeparator.VALUE }'

   key = GuardiansTalkScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestInvalidEndTime_ExpectNone() -> None:
   start_time = '10:00'
   end_time = 'bad'
   wire = ScheduleItemKeySeparator.VALUE.join(
      [ GORILLA_TALK, start_time, end_time ] )

   key = GuardiansTalkScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWires_TestMixedEntries_ExpectValidKeysOnly() -> None:
   start_time = '10:00'
   other_name = 'Rhino Talk'
   other_start = '11:00'
   wires = [
      ScheduleItemKeySeparator.VALUE.join( [ GORILLA_TALK, start_time ] ),
      '',
      other_name,
      ScheduleItemKeySeparator.VALUE.join( [ other_name, other_start ] ),
   ]

   keys = GuardiansTalkScheduleItemKey.from_wires( wires )

   assert keys == [
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time=DateValues.normalize_schedule_time( start_time ) ),
      GuardiansTalkScheduleItemKey(
         name=other_name,
         start_time=DateValues.normalize_schedule_time( other_start ) ),
   ]


def Test_FromRow_TestGuardiansTalkRecord_ExpectScheduleItemKey() -> None:
   start_time = '10:00'
   end_time = '10:30'
   record = ItineraryGuardiansTalkRecord(
      talk_name=GORILLA_TALK,
      start_time=start_time,
      end_time=end_time,
      is_deleted=False )

   key = GuardiansTalkScheduleItemKey.from_row( record )

   assert key == GuardiansTalkScheduleItemKey(
      name=record.talk_name,
      start_time=DateValues.normalize_schedule_time( record.start_time ),
      end_time=DateValues.normalize_schedule_time( record.end_time ) )


def Test_Equality_TestEndTimeDifference_ExpectIgnored() -> None:
   start_time = '10:00 AM'
   start_only = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=start_time )
   with_end = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=start_time,
      end_time='10:30 AM' )
   different_start = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='11:00 AM',
      end_time='10:30 AM' )

   assert start_only == with_end
   assert hash( start_only ) == hash( with_end )
   assert start_only != different_start


def Test_PostInit_TestInvalidStartTime_ExpectValueError() -> None:
   start_time = 'not-a-time'

   with pytest.raises( ValueError, match='Invalid guardians talk start time' ):
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time=start_time )


def Test_PostInit_TestInvalidEndTime_ExpectValueError() -> None:
   start_time = '10:00 AM'
   end_time = 'not-a-time'

   with pytest.raises( ValueError, match='Invalid guardians talk end time' ):
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time=start_time,
         end_time=end_time )


def Test_FromRow_TestDictSource_ExpectScheduleItemKey() -> None:
   start_time = '10:00'
   end_time = '10:30'
   row = {
      'talk_name': GORILLA_TALK,
      'start_time': start_time,
      'end_time': end_time,
   }

   key = GuardiansTalkScheduleItemKey.from_row( row )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=DateValues.normalize_schedule_time( start_time ),
      end_time=DateValues.normalize_schedule_time( end_time ) )


def Test_FromRow_TestInvalidProvidedEndTime_ExpectNone() -> None:
   row = {
      'name': GORILLA_TALK,
      'start_time': '10:00',
      'end_time': 'bad',
   }

   key = GuardiansTalkScheduleItemKey.from_row( row )

   assert key is None


def Test_FromRow_TestMissingName_ExpectNone() -> None:
   row = {
      'start_time': '10:00',
   }

   key = GuardiansTalkScheduleItemKey.from_row( row )

   assert key is None


def Test_Equality_TestNonKey_ExpectNotImplemented() -> None:
   key = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM' )
   other = 'not-a-key'

   result = key.__eq__( other )

   assert result is NotImplemented


def Test_ToWire_TestWithEndTime_ExpectEndIncluded() -> None:
   start_time = '10:00 AM'
   end_time = '10:30 AM'
   key = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time=start_time,
      end_time=end_time )

   wire = key.to_wire()

   assert wire == ScheduleItemKeySeparator.VALUE.join(
      [ key.name, key.start_time, key.end_time ] )
