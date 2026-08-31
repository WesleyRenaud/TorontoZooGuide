from __future__ import annotations

from api.itinerary.routing.itinerary_fixed_time_stop_builder import ItineraryFixedTimeStopBuilder
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.shared.enums import ScheduleItemKind


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
   item_key='African Lion||Africa Savanna',
   walk_node_ids=( 'n-1002', ),
   start_time=None,
   end_time=None,
)


def Test_FromItineraryStop_TestFixedTimeStop_ExpectParsedScheduleTimes() -> None:
   fixed_time_stop = ItineraryFixedTimeStopBuilder.from_itinerary_stop( FIXED_TIME_STOP )

   assert fixed_time_stop is not None
   assert fixed_time_stop.stop is FIXED_TIME_STOP
   assert fixed_time_stop.start_seconds == 11 * 60 * 60
   assert fixed_time_stop.end_seconds == ( 11 * 60 + 45 ) * 60


def Test_FromItineraryStops_TestMixedStops_ExpectSkipsUnscheduledStops() -> None:
   fixed_time_stops = ItineraryFixedTimeStopBuilder.from_itinerary_stops(
      [ UNSCHEDULED_STOP, FIXED_TIME_STOP ] )

   assert len( fixed_time_stops ) == 1
   assert fixed_time_stops[ 0 ].stop.item_key == 'Masai Giraffe'
