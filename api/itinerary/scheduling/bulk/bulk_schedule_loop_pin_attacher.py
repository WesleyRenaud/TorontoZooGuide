from __future__ import annotations

from dataclasses import replace

from ....guardians.scheduling.guardians_talk_loop_schedule_pin import resolve_guardians_talk_loop_pin
from ....models import Itinerary
from ...routing.itinerary_schedule_window import ItineraryScheduleWindow
from ...routing.itinerary_stop import ItineraryStop
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....shared.enums import ScheduleItemKind
from ....types import Connection
from ....wild_encounters.data_access.wild_encounter_meeting_spot_loop_pin_provider import WildEncounterMeetingSpotLoopPinProvider
from ....wild_encounters.scheduling.wild_encounter_loop_schedule_pin import resolve_wild_encounter_loop_pin


class BulkScheduleLoopPinAttacher():
   @classmethod
   def separate_boundaries_and_pins(
         cls,
         conn: Connection,
         itinerary: Itinerary,
         fixed_time_stops: list[ ItineraryStop ],
      ) -> tuple[ list[ ItineraryStop ], list[ LoopSchedulePin ] ]:
      fixed_guardians_talk_stops = {
         fixed_time_stop.item_key: fixed_time_stop
         for fixed_time_stop in fixed_time_stops
         if fixed_time_stop.schedule_item_kind == ScheduleItemKind.GUARDIANS_TALK
      }
      fixed_wild_encounter_stops = {
         fixed_time_stop.item_key: fixed_time_stop
         for fixed_time_stop in fixed_time_stops
         if fixed_time_stop.schedule_item_kind == ScheduleItemKind.WILD_ENCOUNTER
      }
      meeting_spot_loop_pins_by_name = WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name(
         conn )
      loop_pins: list[ LoopSchedulePin ] = []

      for guardians_talk in itinerary.guardians_talks:
         if guardians_talk.is_deleted:
            continue

         fixed_time_stop = fixed_guardians_talk_stops.get( guardians_talk.name )

         if fixed_time_stop is None:
            continue

         loop_pin = resolve_guardians_talk_loop_pin(
            conn,
            guardians_talk,
            fixed_time_stop )

         if loop_pin is None:
            continue

         loop_pins.append( loop_pin )

      for wild_encounter in itinerary.wild_encounters:
         if wild_encounter.is_deleted:
            continue

         fixed_time_stop = fixed_wild_encounter_stops.get( wild_encounter.name )

         if fixed_time_stop is None:
            continue

         loop_pin = resolve_wild_encounter_loop_pin(
            wild_encounter,
            fixed_time_stop,
            meeting_spot_loop_pins_by_name=meeting_spot_loop_pins_by_name )

         if loop_pin is None:
            continue

         loop_pins.append( loop_pin )

      loop_pins.sort( key=lambda loop_pin: loop_pin.start_seconds )

      return fixed_time_stops, loop_pins


   @classmethod
   def attach_to_windows(
         cls,
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
               if cls._applies_to_window( loop_pin, schedule_window )
            ] )
         for schedule_window in schedule_windows
      ]


   @classmethod
   def keep_completable(
         cls,
         schedule_windows: list[ ItineraryScheduleWindow ],
         loop_pins: list[ LoopSchedulePin ],
      ) -> list[ LoopSchedulePin ]:
      """Drop pins that cannot finish weaving after the talk.

      Those talks remain schedule boundaries/anchors so the whole loop can pack
      against them instead of splitting across a later adjacent fixed-time stop.
      """
      return [
         loop_pin
         for loop_pin in loop_pins
         if cls._weave_is_completable( loop_pin, schedule_windows )
      ]


   @classmethod
   def _weave_is_completable(
         cls,
         loop_pin: LoopSchedulePin,
         schedule_windows: list[ ItineraryScheduleWindow ],
      ) -> bool:
      return any(
         cls._applies_to_window( loop_pin, schedule_window )
         and schedule_window.end_seconds > loop_pin.end_seconds
         for schedule_window in schedule_windows
      )


   @classmethod
   def _applies_to_window(
         cls,
         loop_pin: LoopSchedulePin,
         schedule_window: ItineraryScheduleWindow ) -> bool:
      return (
         loop_pin.start_seconds <= schedule_window.end_seconds
         and loop_pin.end_seconds >= schedule_window.start_seconds
      )
