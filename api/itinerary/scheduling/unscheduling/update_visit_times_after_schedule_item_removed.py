from __future__ import annotations

from ..core.time_block import earliest_scheduled_start_seconds
from ..core.time_block import latest_scheduled_end_seconds
from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_name_key import itinerary_name_key
from ...data_access.itinerary_time import set_itinerary_arrival_time
from ...data_access.itinerary_time import set_itinerary_departure_time
from ...data_access.saved_itinerary import SavedItinerary
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import Connection


def was_first_scheduled_item(
      itinerary: Itinerary,
      removed_block: TimeBlock | None ) -> bool:
   if removed_block is None:
      return False

   earliest_start_seconds = earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return False

   return removed_block.start_seconds == earliest_start_seconds


def was_last_scheduled_item(
      itinerary: Itinerary,
      removed_block: TimeBlock | None ) -> bool:
   if removed_block is None:
      return False

   latest_end_seconds = latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return False

   return removed_block.end_seconds == latest_end_seconds


def removed_fixed_time_activity_blocks(
      saved_itinerary: SavedItinerary,
      itinerary_after: Itinerary ) -> list[ TimeBlock ]:
   remaining_talk_keys = {
      itinerary_name_key( talk.name )
      for talk in itinerary_after.guardians_talks
   }
   remaining_encounter_keys = {
      itinerary_name_key( encounter.name )
      for encounter in itinerary_after.wild_encounters
   }
   removed_blocks: list[ TimeBlock ] = []

   for talk in saved_itinerary.guardians_talk_rows:
      if talk.is_deleted or talk.name_key() in remaining_talk_keys:
         continue

      block = time_block_from_schedule_times( talk.start_time, talk.end_time )

      if block is not None:
         removed_blocks.append( block )

   for encounter in saved_itinerary.wild_encounter_rows:
      if encounter.is_deleted or encounter.name_key() in remaining_encounter_keys:
         continue

      block = time_block_from_schedule_times(
         encounter.start_time,
         encounter.end_time )

      if block is not None:
         removed_blocks.append( block )

   return removed_blocks


def removed_schedule_item_was_first_or_last(
      itinerary_before: Itinerary,
      removed_blocks: list[ TimeBlock ] ) -> tuple[ bool, bool ]:
   removed_first_item = any(
      was_first_scheduled_item( itinerary_before, block )
      for block in removed_blocks )
   removed_last_item = any(
      was_last_scheduled_item( itinerary_before, block )
      for block in removed_blocks )

   return removed_first_item, removed_last_item


def update_arrival_to_earliest_scheduled_start(
      conn: Connection,
      itinerary: Itinerary,
      *,
      previous_arrival_time: str | None ) -> None:
   earliest_start_seconds = earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return

   adjusted_arrival_time = DateValues.schedule_time_key_from_seconds(
      earliest_start_seconds )

   if adjusted_arrival_time == previous_arrival_time:
      return

   set_itinerary_arrival_time( conn, adjusted_arrival_time )


def update_departure_to_latest_scheduled_end(
      conn: Connection,
      itinerary: Itinerary,
      *,
      previous_departure_time: str | None ) -> None:
   latest_end_seconds = latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return

   adjusted_departure_time = DateValues.schedule_time_key_from_seconds(
      latest_end_seconds )

   if adjusted_departure_time == previous_departure_time:
      return

   set_itinerary_departure_time( conn, adjusted_departure_time )


def update_visit_times_after_schedule_item_removed(
      conn: Connection,
      itinerary_before: Itinerary,
      itinerary_after: Itinerary,
      *,
      removed_first_item: bool,
      removed_last_item: bool ) -> None:
   previous_latest_end_seconds = latest_scheduled_end_seconds( itinerary_before )
   previous_departure_seconds = DateValues.time_value_in_seconds(
      itinerary_before.departure_time )
   departure_pinned_to_latest = (
      previous_latest_end_seconds is not None
      and previous_departure_seconds is not None
      and previous_departure_seconds == previous_latest_end_seconds )

   if removed_first_item:
      update_arrival_to_earliest_scheduled_start(
         conn,
         itinerary_after,
         previous_arrival_time=itinerary_before.arrival_time )

   should_update_departure = removed_last_item

   if (
         not should_update_departure
         and departure_pinned_to_latest
         and previous_latest_end_seconds is not None ):
      latest_end_after = latest_scheduled_end_seconds( itinerary_after )

      if (
            latest_end_after is not None
            and latest_end_after < previous_latest_end_seconds ):
         should_update_departure = True

   if should_update_departure:
      update_departure_to_latest_scheduled_end(
         conn,
         itinerary_after,
         previous_departure_time=itinerary_before.departure_time )


def update_visit_times_after_removed_fixed_time_activities(
      conn: Connection,
      saved_itinerary: SavedItinerary,
      itinerary_before: Itinerary,
      itinerary_after: Itinerary ) -> None:
   removed_blocks = removed_fixed_time_activity_blocks(
      saved_itinerary,
      itinerary_after )

   if not removed_blocks:
      return

   removed_first_item, removed_last_item = removed_schedule_item_was_first_or_last(
      itinerary_before,
      removed_blocks )

   update_visit_times_after_schedule_item_removed(
      conn,
      itinerary_before,
      itinerary_after,
      removed_first_item=removed_first_item,
      removed_last_item=removed_last_item )
