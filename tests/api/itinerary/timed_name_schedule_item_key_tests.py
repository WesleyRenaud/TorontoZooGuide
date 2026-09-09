from __future__ import annotations

import pytest

from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.timed_name_schedule_item_key import TimedNameScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


OTTER_FEED = 'Otter Feed'


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   key = TimedNameScheduleItemKey.from_wire( f'{ OTTER_FEED }||13:00||13:45' )

   assert key == TimedNameScheduleItemKey(
      name=OTTER_FEED,
      start_time='1:00 PM',
      end_time='1:45 PM' )
   assert key.to_wire() == f'{ OTTER_FEED }||1:00 PM||1:45 PM'


def Test_FromRow_TestDefaultNameField_ExpectScheduleItemKey() -> None:
   key = TimedNameScheduleItemKey.from_row( {
      'name': OTTER_FEED,
      'start_time': '13:00',
   } )

   assert key == TimedNameScheduleItemKey(
      name=OTTER_FEED,
      start_time='1:00 PM' )


def Test_PostInit_TestInvalidStartTime_ExpectDefaultLabel() -> None:
   with pytest.raises( ValueError, match='Invalid schedule item start time' ):
      TimedNameScheduleItemKey( name=OTTER_FEED, start_time='not-a-time' )


def Test_FromRow_TestSubclassNameFieldOrder_ExpectPrimaryFieldPreferred() -> None:
   key = WildEncounterScheduleItemKey.from_row( {
      'wild_encounter': 'Kangaroo',
      'name': 'Ignored',
      'start_time': '13:00',
   } )

   assert key.name == 'Kangaroo'


def Test_Equality_TestSiblingSubclasses_ExpectNotEqual() -> None:
   guardians_talk = GuardiansTalkScheduleItemKey(
      name=OTTER_FEED,
      start_time='1:00 PM' )
   wild_encounter = WildEncounterScheduleItemKey(
      name=OTTER_FEED,
      start_time='1:00 PM' )

   assert guardians_talk != wild_encounter
   assert wild_encounter != guardians_talk
