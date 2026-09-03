from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey


GORILLA_TALK = 'Gorilla Guardians'


def Test_FromWire_TestStartTime_ExpectNormalizedKey() -> None:
   key = GuardiansTalkScheduleItemKey.from_wire( f'{ GORILLA_TALK }||10:00' )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM' )
   assert key.to_wire() == f'{ GORILLA_TALK }||10:00 AM'


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   key = GuardiansTalkScheduleItemKey.from_wire(
      f'{ GORILLA_TALK }||10:00||10:30' )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM',
      end_time='10:30 AM' )


def Test_FromWire_TestMissingOrInvalidTime_ExpectNone() -> None:
   assert GuardiansTalkScheduleItemKey.from_wire( GORILLA_TALK ) is None
   assert GuardiansTalkScheduleItemKey.from_wire( f'{ GORILLA_TALK }||' ) is None
   assert GuardiansTalkScheduleItemKey.from_wire(
      f'{ GORILLA_TALK }||10:00||bad' ) is None


def Test_FromWires_TestMixedEntries_ExpectValidKeysOnly() -> None:
   keys = GuardiansTalkScheduleItemKey.from_wires( [
      f'{ GORILLA_TALK }||10:00',
      '',
      'Rhino Talk',
      'Rhino Talk||11:00',
   ] )

   assert keys == [
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time='10:00 AM' ),
      GuardiansTalkScheduleItemKey(
         name='Rhino Talk',
         start_time='11:00 AM' ),
   ]


def Test_FromRow_TestGuardiansTalkRecord_ExpectScheduleItemKey() -> None:
   record = ItineraryGuardiansTalkRecord(
      talk_name=GORILLA_TALK,
      start_time='10:00',
      end_time='10:30',
      is_deleted=False,
   )

   assert GuardiansTalkScheduleItemKey.from_row( record ) == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM',
      end_time='10:30 AM' )


def Test_Equality_TestEndTimeDifference_ExpectIgnored() -> None:
   start_only = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM' )
   with_end = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   different_start = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='11:00 AM',
      end_time='10:30 AM' )

   assert start_only == with_end
   assert hash( start_only ) == hash( with_end )
   assert start_only != different_start


def Test_PostInit_TestInvalidStartTime_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='Invalid guardians talk start time' ):
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time='not-a-time' )


def Test_PostInit_TestInvalidEndTime_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='Invalid guardians talk end time' ):
      GuardiansTalkScheduleItemKey(
         name=GORILLA_TALK,
         start_time='10:00 AM',
         end_time='not-a-time' )


def Test_FromRow_TestDictSource_ExpectScheduleItemKey() -> None:
   key = GuardiansTalkScheduleItemKey.from_row( {
      'talk_name': GORILLA_TALK,
      'start_time': '10:00',
      'end_time': '10:30',
   } )

   assert key == GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM',
      end_time='10:30 AM' )


def Test_FromRow_TestInvalidProvidedEndTime_ExpectNone() -> None:
   assert GuardiansTalkScheduleItemKey.from_row( {
      'name': GORILLA_TALK,
      'start_time': '10:00',
      'end_time': 'bad',
   } ) is None


def Test_FromRow_TestMissingName_ExpectNone() -> None:
   assert GuardiansTalkScheduleItemKey.from_row( {
      'start_time': '10:00',
   } ) is None


def Test_Equality_TestNonKey_ExpectNotImplemented() -> None:
   key = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM' )

   assert key.__eq__( 'not-a-key' ) is NotImplemented


def Test_ToWire_TestWithEndTime_ExpectEndIncluded() -> None:
   key = GuardiansTalkScheduleItemKey(
      name=GORILLA_TALK,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert key.to_wire() == f'{ GORILLA_TALK }||10:00 AM||10:30 AM'
