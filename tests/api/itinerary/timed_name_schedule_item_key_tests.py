from __future__ import annotations

import pytest

from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator
from api.itinerary.timed_name_schedule_item_key import TimedNameScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.shared.calendar_dates import DateValues


OTTER_FEED = 'Otter Feed'


def Test_FromWire_TestStartAndEndTime_ExpectNormalizedKey() -> None:
   start_time = '13:00'
   end_time = '13:45'
   wire = ScheduleItemKeySeparator.VALUE.join(
      [ OTTER_FEED, start_time, end_time ] )
   normalized_start = DateValues.normalize_schedule_time( start_time )
   normalized_end = DateValues.normalize_schedule_time( end_time )

   key = TimedNameScheduleItemKey.from_wire( wire )

   assert key == TimedNameScheduleItemKey(
      name=OTTER_FEED,
      start_time=normalized_start,
      end_time=normalized_end )
   assert key.to_wire() == ScheduleItemKeySeparator.VALUE.join(
      [ OTTER_FEED, normalized_start, normalized_end ] )


def Test_FromRow_TestDefaultNameField_ExpectScheduleItemKey() -> None:
   start_time = '13:00'
   row = {
      'name': OTTER_FEED,
      'start_time': start_time,
   }
   normalized_start = DateValues.normalize_schedule_time( start_time )

   key = TimedNameScheduleItemKey.from_row( row )

   assert key == TimedNameScheduleItemKey(
      name=OTTER_FEED,
      start_time=normalized_start )


def Test_PostInit_TestInvalidStartTime_ExpectDefaultLabel() -> None:
   start_time = 'not-a-time'

   with pytest.raises( ValueError, match='Invalid schedule item start time' ):
      TimedNameScheduleItemKey( name=OTTER_FEED, start_time=start_time )


def Test_FromRow_TestSubclassNameFieldOrder_ExpectPrimaryFieldPreferred() -> None:
   name = 'Kangaroo'
   ignored_name = 'Ignored'
   start_time = '13:00'
   row = {
      'wild_encounter': name,
      'name': ignored_name,
      'start_time': start_time,
   }

   key = WildEncounterScheduleItemKey.from_row( row )

   assert key.name == name


def Test_Equality_TestSiblingSubclasses_ExpectNotEqual() -> None:
   start_time = '1:00 PM'
   guardians_talk = GuardiansTalkScheduleItemKey(
      name=OTTER_FEED,
      start_time=start_time )
   wild_encounter = WildEncounterScheduleItemKey(
      name=OTTER_FEED,
      start_time=start_time )

   assert guardians_talk != wild_encounter
   assert wild_encounter != guardians_talk
