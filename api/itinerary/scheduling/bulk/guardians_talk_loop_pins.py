from __future__ import annotations

from dataclasses import replace

from ....models import GuardiansTalk
from ....models import Itinerary
from ...routing.itinerary_stop import ItineraryStop
from ...routing.loop_schedule_pin import LoopSchedulePin
from ...routing.partition_itinerary_schedule_windows import ItineraryScheduleWindow
from ....shared.calendar_dates import DateValues
from ....shared.enums import ScheduleItemKind
from ....walk_graph.domain.master_route_loop import MasterRouteLoop
from ....walk_graph.master_route import default_master_route_loop_by_id


def separate_schedule_boundaries_and_loop_pins(
      itinerary: Itinerary,
      fixed_time_stops: list[ ItineraryStop ],
   ) -> tuple[ list[ ItineraryStop ], list[ LoopSchedulePin ] ]:
   fixed_guardians_talk_stops = {
      fixed_time_stop.item_key: fixed_time_stop
      for fixed_time_stop in fixed_time_stops
      if fixed_time_stop.schedule_item_kind == ScheduleItemKind.GUARDIANS_TALK
   }
   loop_pins: list[ LoopSchedulePin ] = []

   for guardians_talk in itinerary.guardians_talks:
      if guardians_talk.is_deleted:
         continue

      fixed_time_stop = fixed_guardians_talk_stops.get( guardians_talk.name )

      if fixed_time_stop is None:
         continue

      loop_pin = resolve_guardians_talk_loop_pin(
         guardians_talk,
         fixed_time_stop )

      if loop_pin is None:
         continue

      loop_pins.append( loop_pin )

   loop_pins.sort( key=lambda loop_pin: loop_pin.start_seconds )

   return fixed_time_stops, loop_pins


def resolve_guardians_talk_loop_pin(
      guardians_talk: GuardiansTalk,
      itinerary_stop: ItineraryStop ) -> LoopSchedulePin | None:
   start_seconds = DateValues.time_value_in_seconds( itinerary_stop.start_time )
   end_seconds = DateValues.time_value_in_seconds( itinerary_stop.end_time )

   if start_seconds is None or end_seconds is None:
      return None

   loops_by_id = default_master_route_loop_by_id()

   for loop_id, master_route_loop in loops_by_id.items():
      viewing_spot_index = viewing_spot_index_for_talk_in_loop(
         master_route_loop,
         talk_name=guardians_talk.name,
         talk_location=guardians_talk.location )

      if viewing_spot_index is not None:
         return LoopSchedulePin(
            loop_id=loop_id,
            viewing_spot_index=viewing_spot_index,
            stop=itinerary_stop,
            start_seconds=start_seconds,
            end_seconds=end_seconds )

   return None


def viewing_spot_index_for_talk_in_loop(
      master_route_loop: MasterRouteLoop,
      *,
      talk_name: str,
      talk_location: str ) -> int | None:
   for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
      if (
            viewing_spot.species == talk_name
            and viewing_spot.exhibit == talk_location ):
         return index

   return None


def attach_loop_pins_to_schedule_windows(
      schedule_windows: list[ ItineraryScheduleWindow ],
      loop_pins: list[ LoopSchedulePin ],
   ) -> list[ ItineraryScheduleWindow ]:
   if not loop_pins:
      return schedule_windows

   return [
      replace(
         schedule_window,
         loop_pins=[
            loop_pin
            for loop_pin in loop_pins
            if _loop_pin_applies_to_schedule_window(
               loop_pin,
               schedule_window )
         ] )
      for schedule_window in schedule_windows
   ]


def _loop_pin_applies_to_schedule_window(
      loop_pin: LoopSchedulePin,
      schedule_window: ItineraryScheduleWindow ) -> bool:
   return (
      loop_pin.start_seconds <= schedule_window.end_seconds
      and loop_pin.end_seconds >= schedule_window.start_seconds
   )
