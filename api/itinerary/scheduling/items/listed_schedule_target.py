from __future__ import annotations

from dataclasses import dataclass

from ...data_access.itinerary_default_duration import fetch_attraction_default_duration_seconds
from ...data_access.itinerary_default_duration import fetch_enclosure_default_duration_seconds
from ...data_access.schedule_itinerary_item import insert_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import insert_itinerary_attraction_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...data_access.schedule_itinerary_item import update_itinerary_attraction_schedule
from .parse_schedule_item_request import ParsedScheduleItemRequest
from ....shared.enums import ScheduleItemKind
from ....types import Connection
from ....types import Cursor
from ....types import ScheduleTimeKey


@dataclass( frozen=True )
class ListedScheduleTarget:
   default_duration_seconds: int | None


def resolve_listed_schedule_target(
      conn: Connection,
      parsed: ParsedScheduleItemRequest ) -> ListedScheduleTarget:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      return ListedScheduleTarget(
         default_duration_seconds=fetch_enclosure_default_duration_seconds(
            conn,
            parsed.species,
            parsed.exhibit ) )

   return ListedScheduleTarget(
      default_duration_seconds=fetch_attraction_default_duration_seconds(
         conn,
         parsed.attraction_name ) )


def apply_listed_schedule(
      cur: Cursor,
      parsed: ParsedScheduleItemRequest,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      insert_if_missing: bool ) -> bool:
   if parsed.kind == ScheduleItemKind.ANIMAL:
      if insert_if_missing:
         inserted = insert_itinerary_animal_schedule(
            cur,
            species=parsed.species,
            exhibit=parsed.exhibit,
            start_time=start_time,
            end_time=end_time )

         if inserted:
            return True

      return update_itinerary_animal_schedule(
         cur,
         species=parsed.species,
         exhibit=parsed.exhibit,
         start_time=start_time,
         end_time=end_time )

   if insert_if_missing:
      inserted = insert_itinerary_attraction_schedule(
         cur,
         name=parsed.attraction_name,
         start_time=start_time,
         end_time=end_time )

      if inserted:
         return True

   return update_itinerary_attraction_schedule(
      cur,
      name=parsed.attraction_name,
      start_time=start_time,
      end_time=end_time )
