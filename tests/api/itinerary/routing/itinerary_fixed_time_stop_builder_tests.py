from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.routing.itinerary_fixed_time_stop_builder import ItineraryFixedTimeStopBuilder
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.shared.enums import Position, ScheduleItemKind


FIXED_TIME_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
   item_key='Masai Giraffe',
   walk_node_ids=( 'n-1001', ),
   meeting_spot='Wild Encounter - Africa Meeting Spot',
   is_fixed_time=True,
   start_time='11:00 AM',
   end_time='11:45 AM',
)

UNSCHEDULED_STOP = ItineraryStop(
   schedule_item_kind=ScheduleItemKind.ANIMAL,
   item_key=AnimalScheduleItemKey.wire(
      species='African Lion',
      exhibit='Africa Savanna' ),
   walk_node_ids=( 'n-1002', ),
   start_time=None,
   end_time=None,
)


def Test_FromItineraryStop_TestFixedTimeStop_ExpectParsedScheduleTimes() -> None:
   expected_block = TimeBlockBuilder.from_schedule_times(
      FIXED_TIME_STOP.start_time,
      FIXED_TIME_STOP.end_time )

   fixed_time_stop = ItineraryFixedTimeStopBuilder.from_itinerary_stop(
      FIXED_TIME_STOP )

   assert fixed_time_stop is not None
   assert expected_block is not None
   assert fixed_time_stop.stop is FIXED_TIME_STOP
   assert fixed_time_stop.start_seconds == expected_block.start_seconds
   assert fixed_time_stop.end_seconds == expected_block.end_seconds


def Test_FromItineraryStops_TestMixedStops_ExpectSkipsUnscheduledStops() -> None:
   stops = [ UNSCHEDULED_STOP, FIXED_TIME_STOP ]

   fixed_time_stops = ItineraryFixedTimeStopBuilder.from_itinerary_stops( stops )

   assert len( fixed_time_stops ) == 1
   assert fixed_time_stops[ Position.FIRST ].stop is FIXED_TIME_STOP
   assert fixed_time_stops[ Position.FIRST ].stop.item_key == FIXED_TIME_STOP.item_key
