from __future__ import annotations

from api.itinerary.routing.itinerary_fixed_time_stop import itinerary_fixed_time_stop_from_itinerary_stop
from api.itinerary.routing.itinerary_fixed_time_stop import itinerary_fixed_time_stops_from_itinerary_stops
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.shared.enums import ScheduleItemKind


def test_itinerary_fixed_time_stop_from_itinerary_stop_parses_schedule_times() -> None:
   stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key='Masai Giraffe',
      walk_node_ids=( 'v-0304', ),
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      is_fixed_time=True,
      start_time='11:00 AM',
      end_time='11:45 AM',
   )

   fixed_time_stop = itinerary_fixed_time_stop_from_itinerary_stop( stop )

   assert fixed_time_stop is not None
   assert fixed_time_stop.stop is stop
   assert fixed_time_stop.start_seconds == 11 * 60 * 60
   assert fixed_time_stop.end_seconds == ( 11 * 60 + 45 ) * 60


def test_itinerary_fixed_time_stops_from_itinerary_stops_skips_unscheduled_stops() -> None:
   fixed_time_stops = itinerary_fixed_time_stops_from_itinerary_stops(
      [
         ItineraryStop(
            schedule_item_kind=ScheduleItemKind.ANIMAL,
            item_key='African Lion||Africa Savanna',
            walk_node_ids=( 'v-0647', ),
            start_time=None,
            end_time=None,
         ),
         ItineraryStop(
            schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
            item_key='Masai Giraffe',
            walk_node_ids=( 'v-0304', ),
            is_fixed_time=True,
            start_time='11:00 AM',
            end_time='11:45 AM',
         ),
      ],
   )

   assert len( fixed_time_stops ) == 1
   assert fixed_time_stops[ 0 ].stop.item_key == 'Masai Giraffe'
