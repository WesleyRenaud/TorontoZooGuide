from __future__ import annotations

from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_schedule_window_partitioner import ItineraryScheduleWindowPartitioner
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind


ANCHOR_TIME = '9:00 AM'
DAY_END_TIME = '5:00 PM'
ARRIVAL_TIME = '11:00 AM'


def _seconds( schedule_time: str ) -> int:
   seconds = DateValues.time_value_in_seconds( schedule_time )
   assert seconds is not None
   return seconds


def _time_block( stop: ItineraryStop ) -> TimeBlock:
   time_block = TimeBlockBuilder.from_schedule_times( stop.start_time, stop.end_time )
   assert time_block is not None
   return time_block


ANCHOR_SECONDS = _seconds( ANCHOR_TIME )
DAY_END_SECONDS = _seconds( DAY_END_TIME )
ARRIVAL_SECONDS = _seconds( ARRIVAL_TIME )

FIXED_ENCOUNTER_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='Guardians of White Rhinos',
   walk_node_ids=[ 'n-3001' ],
   meeting_spot='Wild Encounter - Penguin Meeting Spot',
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:45 AM',
)

MIDMORNING_RHINO_ENCOUNTER_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='Guardians of White Rhinos',
   walk_node_ids=[ 'n-3001' ],
   meeting_spot='Wild Encounter - Penguin Meeting Spot',
   is_fixed_time=True,
   start_time='9:52 AM',
   end_time='10:37 AM',
)

AFRICAN_LION_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key='African Lion',
   walk_node_ids=[ 'v-0436' ],
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

ZEBRA_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key="Grevy's Zebra",
   walk_node_ids=[ 'v-0018' ],
   is_fixed_time=True,
   start_time='12:00 PM',
   end_time='12:30 PM',
)

CAMEL_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key='Bactrian Camel',
   walk_node_ids=[ 'v-0044' ],
   is_fixed_time=True,
   start_time='12:30 PM',
   end_time='1:00 PM',
)

BACTRIAN_CAMELS_ENCOUNTER_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='Bactrian Camels',
   walk_node_ids=[ 'v-0100' ],
   meeting_spot='Wild Encounter - Eurasia Meeting Spot',
   is_fixed_time=True,
   start_time='3:30 PM',
   end_time='4:00 PM',
)

OTTER_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key='North American River Otter',
   walk_node_ids=[ 'v-0100' ],
   is_fixed_time=True,
   start_time='2:00 PM',
   end_time='2:30 PM',
)

TINY_TOUR_ENCOUNTER_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='The Tiny Tour',
   walk_node_ids=[ 'n-discovery' ],
   meeting_spot='Wild Encounter - Discovery Zone Meeting Spot',
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
)

HYENA_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key='Spotted Hyena',
   walk_node_ids=[ 'v-hyena' ],
   is_fixed_time=True,
   start_time='2:00 PM',
   end_time='2:30 PM',
)


def Test_Partition_TestFixedEncounter_ExpectWindowsBeforeAndAfter() -> None:
   encounter_block = _time_block( FIXED_ENCOUNTER_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ FIXED_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=encounter_block.start_seconds,
         anchor_stop=FIXED_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=encounter_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=FIXED_ENCOUNTER_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestMidMorningRhinoEncounter_ExpectWindowsBeforeAndAfter() -> None:
   encounter_block = _time_block( MIDMORNING_RHINO_ENCOUNTER_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ MIDMORNING_RHINO_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=encounter_block.start_seconds,
         anchor_stop=MIDMORNING_RHINO_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=encounter_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=MIDMORNING_RHINO_ENCOUNTER_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestGuardiansTalk_ExpectWindowsBeforeAndAfter() -> None:
   talk_block = _time_block( AFRICAN_LION_TALK_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ AFRICAN_LION_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=talk_block.start_seconds,
         anchor_stop=AFRICAN_LION_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=talk_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=AFRICAN_LION_TALK_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestAdjacentGuardiansTalks_ExpectWindowsBeforeZebraAndAfterCamel() -> None:
   zebra_block = _time_block( ZEBRA_TALK_STOP )
   camel_block = _time_block( CAMEL_TALK_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ ZEBRA_TALK_STOP, CAMEL_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=zebra_block.start_seconds,
         anchor_stop=ZEBRA_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=camel_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=CAMEL_TALK_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestUnpinnedAfternoonEncounter_ExpectWindowBeforeEncounter() -> None:
   encounter_block = _time_block( BACTRIAN_CAMELS_ENCOUNTER_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ BACTRIAN_CAMELS_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=encounter_block.start_seconds,
         anchor_stop=BACTRIAN_CAMELS_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=encounter_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=BACTRIAN_CAMELS_ENCOUNTER_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestOtterTalk_ExpectWindowsBeforeAndAfter() -> None:
   talk_block = _time_block( OTTER_TALK_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ OTTER_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=talk_block.start_seconds,
         anchor_stop=OTTER_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=talk_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=OTTER_TALK_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestTinyTourAndHyenaTalk_ExpectMiddleWindowForZoomobile() -> None:
   tiny_tour_block = _time_block( TINY_TOUR_ENCOUNTER_STOP )
   hyena_block = _time_block( HYENA_TALK_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ TINY_TOUR_ENCOUNTER_STOP, HYENA_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=tiny_tour_block.start_seconds,
         anchor_stop=TINY_TOUR_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=tiny_tour_block.end_seconds,
         end_seconds=hyena_block.start_seconds,
         anchor_stop=HYENA_TALK_STOP,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=TINY_TOUR_ENCOUNTER_STOP.primary_walk_node_id() ),
      ItineraryScheduleWindow(
         start_seconds=hyena_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=HYENA_TALK_STOP.primary_walk_node_id() ),
   ]


def Test_Partition_TestCamelTalkAndEncounter_ExpectAfternoonWindowBetweenTalkAndEncounter() -> None:
   camel_block = _time_block( CAMEL_TALK_STOP )
   encounter_block = _time_block( BACTRIAN_CAMELS_ENCOUNTER_STOP )

   windows = ItineraryScheduleWindowPartitioner.partition(
      ARRIVAL_SECONDS,
      DAY_END_SECONDS,
      [ CAMEL_TALK_STOP, BACTRIAN_CAMELS_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ARRIVAL_SECONDS,
         end_seconds=camel_block.start_seconds,
         anchor_stop=CAMEL_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=camel_block.end_seconds,
         end_seconds=encounter_block.start_seconds,
         anchor_stop=BACTRIAN_CAMELS_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=CAMEL_TALK_STOP.primary_walk_node_id() ),
      ItineraryScheduleWindow(
         start_seconds=encounter_block.end_seconds,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id=BACTRIAN_CAMELS_ENCOUNTER_STOP.primary_walk_node_id() ),
   ]
