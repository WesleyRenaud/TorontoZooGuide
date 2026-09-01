from __future__ import annotations

from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_schedule_window_partitioner import ItineraryScheduleWindowPartitioner
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.shared.enums import ScheduleItemKind


ANCHOR_SECONDS = 9 * 60 * 60
DAY_END_SECONDS = 17 * 60 * 60

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
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ FIXED_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=11 * 60 * 60,
         anchor_stop=FIXED_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=( 11 * 60 + 45 ) * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='n-3001' ),
   ]


def Test_Partition_TestMidMorningRhinoEncounter_ExpectWindowsBeforeAndAfter() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ MIDMORNING_RHINO_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=9 * 60 * 60 + 52 * 60,
         anchor_stop=MIDMORNING_RHINO_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=( 10 * 60 + 37 ) * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='n-3001' ),
   ]


def Test_Partition_TestGuardiansTalk_ExpectWindowsBeforeAndAfter() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ AFRICAN_LION_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=11 * 60 * 60,
         anchor_stop=AFRICAN_LION_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=( 11 * 60 + 30 ) * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-0436' ),
   ]


def Test_Partition_TestAdjacentGuardiansTalks_ExpectWindowsBeforeZebraAndAfterCamel() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ ZEBRA_TALK_STOP, CAMEL_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=12 * 60 * 60,
         anchor_stop=ZEBRA_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=13 * 60 * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-0044' ),
   ]


def Test_Partition_TestUnpinnedAfternoonEncounter_ExpectWindowBeforeEncounter() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ BACTRIAN_CAMELS_ENCOUNTER_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=15 * 60 * 60 + 30 * 60,
         anchor_stop=BACTRIAN_CAMELS_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=16 * 60 * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-0100' ),
   ]


def Test_Partition_TestOtterTalk_ExpectWindowsBeforeAndAfter() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ OTTER_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=14 * 60 * 60,
         anchor_stop=OTTER_TALK_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=14 * 60 * 60 + 30 * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-0100' ),
   ]


def Test_Partition_TestTinyTourAndHyenaTalk_ExpectMiddleWindowForZoomobile() -> None:
   windows = ItineraryScheduleWindowPartitioner.partition(
      ANCHOR_SECONDS,
      DAY_END_SECONDS,
      [ TINY_TOUR_ENCOUNTER_STOP, HYENA_TALK_STOP ] )

   assert windows == [
      ItineraryScheduleWindow(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=11 * 60 * 60,
         anchor_stop=TINY_TOUR_ENCOUNTER_STOP,
         opens_after_fixed_time_stop=False,
         start_walk_node_id=None ),
      ItineraryScheduleWindow(
         start_seconds=11 * 60 * 60 + 30 * 60,
         end_seconds=14 * 60 * 60,
         anchor_stop=HYENA_TALK_STOP,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='n-discovery' ),
      ItineraryScheduleWindow(
         start_seconds=14 * 60 * 60 + 30 * 60,
         end_seconds=DAY_END_SECONDS,
         anchor_stop=None,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-hyena' ),
   ]
