from __future__ import annotations

from ..core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from ..core.time_block import TimeBlock
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_transportation_provider import ItineraryTransportationProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ...data_access.schedule_itinerary_transportation_provider import ScheduleItineraryTransportationProvider
from ..items.schedule_item_key import ScheduleItemKey
from ....models.itinerary_transportation_leg import ItineraryTransportationLeg
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryEventType
from ....types import Types


class GuestScheduleShiftApplier():
   @classmethod
   def shifted_schedule_times(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         delta_seconds: int ) -> tuple[ Types.ScheduleTimeKey, Types.ScheduleTimeKey ] | None:
      block = TimeBlockBuilder.from_schedule_times( start_time, end_time )

      if block is None:
         return None

      shifted_block = TimeBlockBuilder.from_seconds(
         block.start_seconds + delta_seconds,
         block.end_seconds + delta_seconds )

      if shifted_block is None:
         return None

      return (
         DateValues.schedule_time_key_from_seconds( shifted_block.start_seconds ),
         DateValues.schedule_time_key_from_seconds( shifted_block.end_seconds ),
      )


   @classmethod
   def resolve_unscheduled_item_time_block(
         cls,
         saved_itinerary: SavedItinerary,
         schedule_item_key: ScheduleItemKey.Key,
         ) -> TimeBlock | None:
      row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
         saved_itinerary,
         schedule_item_key )

      if row is None:
         return None

      return TimeBlockBuilder.from_schedule_times(
         row.start_time,
         row.end_time )


   @classmethod
   def _should_shift_guest_scheduled_event(
         cls,
         event_type: ItineraryEventType ) -> bool:
      return event_type not in (
         ItineraryEventType.ARRIVAL,
         ItineraryEventType.DEPARTURE,
      )


   @classmethod
   def _collect_fixed_activity_blocks(
         cls,
         conn: Types.Connection,
         *,
         freed_block: TimeBlock | None ) -> list[ TimeBlock ]:
      occupied: list[ TimeBlock ] = []

      for talk_row in ItineraryProvider.fetch_itinerary_guardians_talk_rows( conn ):
         if talk_row.is_deleted:
            continue

         block = TimeBlockBuilder.from_schedule_times(
            talk_row.start_time,
            talk_row.end_time )

         if block is not None:
            occupied.append( block )

      for encounter_row in ItineraryProvider.fetch_itinerary_wild_encounter_rows( conn ):
         if encounter_row.is_deleted:
            continue

         block = TimeBlockBuilder.from_schedule_times(
            encounter_row.start_time,
            encounter_row.end_time )

         if block is not None:
            occupied.append( block )

      if freed_block is None:
         return occupied

      return [
         block
         for block in occupied
         if block != freed_block
      ]


   @classmethod
   def _shifted_block_overlaps_occupied(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         delta_seconds: int,
         occupied_blocks: list[ TimeBlock ] ) -> bool:
      shifted_times = cls.shifted_schedule_times( start_time, end_time, delta_seconds )

      if shifted_times is None:
         return True

      shifted_block = TimeBlockBuilder.from_schedule_times(
         shifted_times[ 0 ],
         shifted_times[ 1 ] )

      if shifted_block is None:
         return True

      return any(
         TimeBlockBuilder.overlap( shifted_block, occupied_block )
         for occupied_block in occupied_blocks
      )


   @classmethod
   def _guest_shift_would_overlap_fixed_activity(
         cls,
         conn: Types.Connection,
         *,
         anchor_end_time: Types.ScheduleTimeKey,
         delta_seconds: int,
         occupied_blocks: list[ TimeBlock ] ) -> bool:
      for animal_row in ItineraryProvider.fetch_itinerary_animal_rows( conn ):
         if animal_row.covered_by_talk:
            continue

         if not GuestItemScheduleStatusChecker.has_schedule_times(
               animal_row.start_time,
               animal_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               animal_row.start_time,
               anchor_end_time ):
            continue

         if cls._shifted_block_overlaps_occupied(
               animal_row.start_time,
               animal_row.end_time,
               delta_seconds,
               occupied_blocks ):
            return True

      for attraction_row in ItineraryProvider.fetch_itinerary_attraction_rows( conn ):
         if not GuestItemScheduleStatusChecker.has_schedule_times(
               attraction_row.start_time,
               attraction_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               attraction_row.start_time,
               anchor_end_time ):
            continue

         if cls._shifted_block_overlaps_occupied(
               attraction_row.start_time,
               attraction_row.end_time,
               delta_seconds,
               occupied_blocks ):
            return True

      for transportation_row in ItineraryProvider.fetch_itinerary_transportation_rows( conn ):
         if not GuestItemScheduleStatusChecker.has_schedule_times(
               transportation_row.start_time,
               transportation_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               transportation_row.start_time,
               anchor_end_time ):
            continue

         if cls._shifted_block_overlaps_occupied(
               transportation_row.start_time,
               transportation_row.end_time,
               delta_seconds,
               occupied_blocks ):
            return True

      for event_row in ItineraryProvider.fetch_itinerary_event_rows( conn ):
         if not cls._should_shift_guest_scheduled_event( event_row.event_type ):
            continue

         if not GuestItemScheduleStatusChecker.has_schedule_times(
               event_row.start_time,
               event_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               event_row.start_time,
               anchor_end_time ):
            continue

         if cls._shifted_block_overlaps_occupied(
               event_row.start_time,
               event_row.end_time,
               delta_seconds,
               occupied_blocks ):
            return True

      return False


   @classmethod
   def _shift_guest_scheduled_animal_rows(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         anchor_end_time: Types.ScheduleTimeKey,
         delta_seconds: int ) -> None:
      for animal_row in ItineraryProvider.fetch_itinerary_animal_rows( conn ):
         if animal_row.covered_by_talk:
            continue

         if not GuestItemScheduleStatusChecker.has_schedule_times(
               animal_row.start_time,
               animal_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               animal_row.start_time,
               anchor_end_time ):
            continue

         shifted_times = cls.shifted_schedule_times(
            animal_row.start_time,
            animal_row.end_time,
            delta_seconds )

         if shifted_times is None:
            continue

         ScheduleItineraryItemProvider.update_itinerary_animal_schedule(
            cur,
            species=animal_row.species,
            exhibit=animal_row.exhibit,
            enclosure_name=animal_row.enclosure_name,
            start_time=shifted_times[ 0 ],
            end_time=shifted_times[ 1 ],
         )


   @classmethod
   def _shift_guest_scheduled_attraction_rows(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         anchor_end_time: Types.ScheduleTimeKey,
         delta_seconds: int ) -> None:
      for attraction_row in ItineraryProvider.fetch_itinerary_attraction_rows( conn ):
         if not GuestItemScheduleStatusChecker.has_schedule_times(
               attraction_row.start_time,
               attraction_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               attraction_row.start_time,
               anchor_end_time ):
            continue

         shifted_times = cls.shifted_schedule_times(
            attraction_row.start_time,
            attraction_row.end_time,
            delta_seconds )

         if shifted_times is None:
            continue

         ScheduleItineraryItemProvider.update_itinerary_attraction_schedule(
            cur,
            name=attraction_row.attraction,
            start_time=shifted_times[ 0 ],
            end_time=shifted_times[ 1 ],
         )


   @classmethod
   def _shift_guest_scheduled_transportation_rows(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         anchor_end_time: Types.ScheduleTimeKey,
         delta_seconds: int ) -> None:
      for transportation_row in ItineraryProvider.fetch_itinerary_transportation_rows( conn ):
         if not GuestItemScheduleStatusChecker.has_schedule_times(
               transportation_row.start_time,
               transportation_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               transportation_row.start_time,
               anchor_end_time ):
            continue

         if transportation_row.route is None:
            continue

         shifted_times = cls.shifted_schedule_times(
            transportation_row.start_time,
            transportation_row.end_time,
            delta_seconds )

         if shifted_times is None:
            continue

         shifted_legs: list[ ItineraryTransportationLeg ] = []

         for leg in transportation_row.legs:
            leg_times = cls.shifted_schedule_times(
               leg.start_time,
               leg.end_time,
               delta_seconds )

            if leg_times is None:
               shifted_legs = []
               break

            start_time, end_time = leg_times
            shifted_legs.append(
               ItineraryTransportationLeg(
                  from_station=leg.from_station,
                  to_station=leg.to_station,
                  start_time=start_time,
                  end_time=end_time,
                  transportation=leg.transportation,
                  added_as_attraction=leg.added_as_attraction ) )

         if not shifted_legs:
            continue

         ItineraryTransportationProvider.delete_itinerary_transportation_legs(
            cur,
            transportation=transportation_row.transportation,
            added_as_attraction=transportation_row.added_as_attraction )
         ItineraryTransportationProvider.insert_itinerary_transportation_legs(
            cur,
            transportation=transportation_row.transportation,
            added_as_attraction=transportation_row.added_as_attraction,
            legs=shifted_legs )
         ScheduleItineraryTransportationProvider.update_itinerary_transportation_schedule(
            cur,
            name=transportation_row.transportation,
            added_as_attraction=transportation_row.added_as_attraction,
            start_time=shifted_times[ 0 ],
            end_time=shifted_times[ 1 ],
            route=transportation_row.route )


   @classmethod
   def _shift_guest_scheduled_event_rows(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         anchor_end_time: Types.ScheduleTimeKey,
         delta_seconds: int ) -> None:
      for event_row in ItineraryProvider.fetch_itinerary_event_rows( conn ):
         if not cls._should_shift_guest_scheduled_event( event_row.event_type ):
            continue

         if not GuestItemScheduleStatusChecker.has_schedule_times(
               event_row.start_time,
               event_row.end_time ):
            continue

         if not DateValues.time_value_is_at_or_after(
               event_row.start_time,
               anchor_end_time ):
            continue

         shifted_times = cls.shifted_schedule_times(
            event_row.start_time,
            event_row.end_time,
            delta_seconds )

         if shifted_times is None:
            continue

         ScheduleItineraryItemProvider.update_itinerary_event_schedule(
            cur,
            event_type=event_row.event_type,
            start_time=shifted_times[ 0 ],
            end_time=shifted_times[ 1 ],
         )


   @classmethod
   def shift_items_after_unschedule(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         anchor_end_seconds: int,
         shift_seconds: int,
         freed_block: TimeBlock | None = None ) -> None:
      if shift_seconds == 0:
         return

      anchor_end_time = DateValues.schedule_time_key_from_seconds( anchor_end_seconds )
      occupied_blocks = cls._collect_fixed_activity_blocks(
         conn,
         freed_block=freed_block )

      if cls._guest_shift_would_overlap_fixed_activity(
            conn,
            anchor_end_time=anchor_end_time,
            delta_seconds=shift_seconds,
            occupied_blocks=occupied_blocks ):
         return

      cls._shift_guest_scheduled_animal_rows(
         conn,
         cur,
         anchor_end_time=anchor_end_time,
         delta_seconds=shift_seconds )
      cls._shift_guest_scheduled_attraction_rows(
         conn,
         cur,
         anchor_end_time=anchor_end_time,
         delta_seconds=shift_seconds )
      cls._shift_guest_scheduled_transportation_rows(
         conn,
         cur,
         anchor_end_time=anchor_end_time,
         delta_seconds=shift_seconds )
      cls._shift_guest_scheduled_event_rows(
         conn,
         cur,
         anchor_end_time=anchor_end_time,
         delta_seconds=shift_seconds )


   @classmethod
   def apply_for_unschedule(
         cls,
         conn: Types.Connection,
         cur: Types.Cursor,
         *,
         saved_itinerary: SavedItinerary,
         schedule_item_key: ScheduleItemKey.Key,
         ) -> None:
      removed_block = cls.resolve_unscheduled_item_time_block(
         saved_itinerary,
         schedule_item_key )

      if removed_block is None:
         return

      shift_seconds = removed_block.start_seconds - removed_block.end_seconds

      cls.shift_items_after_unschedule(
         conn,
         cur,
         anchor_end_seconds=removed_block.end_seconds,
         shift_seconds=shift_seconds,
         freed_block=removed_block )
