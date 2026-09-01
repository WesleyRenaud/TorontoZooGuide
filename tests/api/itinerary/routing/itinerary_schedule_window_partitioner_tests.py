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

AFRICAN_LION_TALK_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
   item_key='African Lion',
   walk_node_ids=[ 'v-0436' ],
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:30 AM',
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
